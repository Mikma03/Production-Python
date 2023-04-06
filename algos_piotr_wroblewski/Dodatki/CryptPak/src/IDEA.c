

#include "IDEA.h"


typedef struct 
{
  WORD16 key[IDEA_KEYLEN];
  WORD32 lCBCHi;
  WORD32 lCBCLo;
} 
IDEACTX;



// forwards
void ideaCipher(WORD8[8], WORD8[8], WORD16*);
void ideaExpandKey(WORD8*, WORD16*);
void ideaInvertKey(WORD16*, WORD16[]);




WORD32 IDEA_GetCipherInfo
  (CIPHERINFOBLOCK* pInfo) 
{
  WORD32 lI;
  WORD8* pSrc;
  WORD8* pDst;
  CIPHERINFOBLOCK tempinfo;

  // prepare the information context
  tempinfo.lSizeOf = pInfo->lSizeOf;
  tempinfo.lBlockSize = IDEA_BLOCKSIZE;
  tempinfo.lKeySize = IDEA_KEYSIZE; 
  tempinfo.blOwnHasher = BOOL_FALSE;
  tempinfo.lInitDataSize = IDEA_BLOCKSIZE;
  tempinfo.lContextSize = sizeof(IDEACTX);
  tempinfo.bCipherIs = CIPHER_IS_BLOCKLINK;

  // copy as many bytes of the information block as possible
  pSrc = (WORD8*) &tempinfo;
  pDst = (WORD8*) pInfo;
  for (lI = 0; lI < tempinfo.lSizeOf; lI++)
    *pDst++ = *pSrc++;

  return CIPHER_ERROR_NOERROR;
}



WORD32 IDEA_SelfTest 
  (void* pTestContext) 
{
  // test the driver for correct encrypting and decrypting 

  static WORD8 testkey[IDEA_KEYSIZE] = { 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16 } ;
  WORD16 key[IDEA_KEYLEN];

  static WORD32 plainBlock[2] = { 0x1234567, 0x89abcdef }; 
  WORD32 cipherBlock[2];

  // setup a dummy key
  ideaExpandKey(testkey, key);

  // encrypt the test block
  ideaCipher((WORD8*) plainBlock, (WORD8*) cipherBlock, key);

  // create a decryption key
  ideaInvertKey(key, key);

  // decrypt the test block
  ideaCipher((WORD8*) cipherBlock, (WORD8*) cipherBlock, key);

  // equal plaintexts?
  return ((plainBlock[0] == cipherBlock[0]) && 
          (plainBlock[1] == cipherBlock[1])) ? 
         CIPHER_ERROR_NOERROR : CIPHER_ERROR_INVALID;
}



WORD32 IDEA_CreateWorkContext
  (void* pContext,
   const WORD8* pKey,
   WORD32 lKeyLen,
   WORD32 lMode,
   void* pInitData,
   Cipher_RandomGenerator GetRndBytes,
   const void* pRndGenData) 
{
  IDEACTX* pCtx = (IDEACTX*) pContext;
  WORD32* pCBCIV = (WORD32*) pInitData;

  // expand the key 
  ideaExpandKey((WORD8*) pKey, 
                (WORD16*) &(pCtx->key));
  
  // for decryption we have to invert the key, too 
  if (lMode == CIPHER_MODE_DECRYPT) 
  {
    ideaInvertKey((WORD16*) &(pCtx->key), 
                  (WORD16*) &(pCtx->key));
  }

  // for encryption create a CBC iv 
  if (lMode == CIPHER_MODE_ENCRYPT) 
  {
    GetRndBytes((WORD8*) pCBCIV, 8, pRndGenData);
  }

  // set the CBC IV, either new or not 
  pCtx->lCBCLo = pCBCIV[0];
  pCtx->lCBCHi = pCBCIV[1];

  // FIXME: weak keys in IDEA? 
  return CIPHER_ERROR_NOERROR;
}




void IDEA_ResetWorkContext
  (void* pContext,
   WORD32 lMode,
   void* pInitData,
   Cipher_RandomGenerator GetRndBytes,
   const void* pRndGenData) 
{
  IDEACTX* pCtx = (IDEACTX*) pContext;

  // just reset the CBC IV 

  WORD32* pCBCIV = (WORD32*) pInitData;

  if (lMode == CIPHER_MODE_ENCRYPT) 
  {
    GetRndBytes((WORD8*) pCBCIV, 8, pRndGenData);
  }

  pCtx->lCBCLo = pCBCIV[0];
  pCtx->lCBCHi = pCBCIV[1];

}



WORD32 IDEA_DestroyWorkContext 
  (void* pContext) 
{
  // clear the context 
  int nI;
  WORD8* clearIt = (WORD8*) pContext;

  for (nI = 0; nI < sizeof(IDEACTX); nI++) 
  {
    clearIt[nI] = 0x00;
  }

  return CIPHER_ERROR_NOERROR;
}



void IDEA_EncryptBuffer
  (void* pContext, 
   const void* pSource, 
   void* pTarget,
   WORD32 lNumOfBytes) 
{
  WORD32 lNumOfInts;
  WORD32 lI;
  WORD32* pInBuf = (WORD32*) pSource;
  WORD32* pOutBuf = (WORD32*) pTarget;
  IDEACTX* pCtx = (IDEACTX*) pContext;

  // calculate the number of (32bit) words 
  lNumOfInts = lNumOfBytes >> 2;

  // anything to encrypt? 
  if (lNumOfInts < 2) return;

  // work through all blocks... 
  for (lI = 0; lI < lNumOfInts; lI += 2) 
  {
     // copy and chain the recent block 
     pOutBuf[lI]     = pInBuf[lI]     ^ pCtx->lCBCLo;
     pOutBuf[lI + 1] = pInBuf[lI + 1] ^ pCtx->lCBCHi;
     
     // encrypt the block 
     ideaCipher((WORD8*) &(pOutBuf[lI]), 
                (WORD8*) &(pOutBuf[lI]), 
                pCtx->key);
     
     // set the new CBC iv 
     pCtx->lCBCLo = pOutBuf[lI];
     pCtx->lCBCHi = pOutBuf[lI + 1];
  }
}


void IDEA_DecryptBuffer
  (void* pContext, 
   const void* pSource, 
   void* pTarget, 
   WORD32 lNumOfBytes, 
   const void* pPreviousBlock) 
{
  WORD32 lNumOfInts;
  WORD32 lI;
  WORD32 lSaveCBCLo;
  WORD32 lSaveCBCHi;
  WORD32* pInBuf = (WORD32*) pSource;
  WORD32* pOutBuf = (WORD32*) pTarget;
  WORD32* pPrevBlock = (WORD32*) pPreviousBlock;
  IDEACTX* pCtx = (IDEACTX*) pContext;

  // calculate the number of (32bit) words 
  lNumOfInts = lNumOfBytes >> 2;

  // anything to decrypt? 
  if (lNumOfInts < 2) return;

  // load a new CBC IV, if necessary 
  if (pPreviousBlock != CIPHER_NULL)  
  {
    pCtx->lCBCLo = pPrevBlock[0];
    pCtx->lCBCHi = pPrevBlock[1];
  }

  // work through all blocks... 
  for (lI = 0; lI < lNumOfInts; lI += 2) 
  {
     // save the recent CBC IV 
     lSaveCBCLo = pInBuf[lI];
     lSaveCBCHi = pInBuf[lI + 1];
  
     // decrypt the block 
     ideaCipher((WORD8*) &(pInBuf[lI]), 
                (WORD8*) &(pOutBuf[lI]), 
                pCtx->key);
     
     // "dechain" the recent block 
     pOutBuf[lI]     = pOutBuf[lI]     ^ pCtx->lCBCLo;
     pOutBuf[lI + 1] = pOutBuf[lI + 1] ^ pCtx->lCBCHi;
     
     // set the new CBC iv 
     pCtx->lCBCLo = lSaveCBCLo;
     pCtx->lCBCHi = lSaveCBCHi;
  }
}



//////////////////////// support routines ////////////////////////

#define low16(x) ((x) & 0x0ffff)

#define MUL(x,y) ( x = low16(x-1), t16 = low16((y)-1), \
                   t32 = (WORD32)x*t16 + x + t16 + 1, x = (WORD16)(low16(t32)), \
                   t16 = (WORD16)(t32>>16), x = (x-t16) + (x<t16) )


void ideaCipher
  (WORD8 inbuf[8], 
   WORD8 outbuf[8], 
   WORD16 *key) 
{
    register WORD16 wX1, wX2, wX3, wX4, wS2, wS3;
    register WORD16 t16;
    register WORD32 t32;    
    WORD16 *in, *out;

    // get the block 
    in = (WORD16*) inbuf;
    wX1 = in[0];  wX2 = in[1];
    wX3 = in[2];  wX4 = in[3];

    // (for speed purposes we don't do any byte ordering here) 

    // unrolled crypt loop (FIXME: macro instead?) ... 
    
    // round #1 
    MUL(wX1, key[0]);
    wX2 += key[1];
    wX3 += key[2];
    MUL(wX4, key[3]);
    wS3 = wX3;
    wX3 ^= wX1;
    MUL(wX3, key[4]);
    wS2 = wX2;
    wX2 ^= wX4;
    wX2 += wX3;
    MUL(wX2, key[5]);
    wX3 += wX2;
    wX1 ^= wX2;  wX4 ^= wX3;
    wX2 ^= wS3;  wX3 ^= wS2;

    // round #2 
    MUL(wX1, key[6]);
    wX2 += key[7];
    wX3 += key[8];
    MUL(wX4, key[9]);
    wS3 = wX3;
    wX3 ^= wX1;
    MUL(wX3, key[10]);
    wS2 = wX2;
    wX2 ^= wX4;
    wX2 += wX3;
    MUL(wX2, key[11]);
    wX3 += wX2;
    wX1 ^= wX2;  wX4 ^= wX3;
    wX2 ^= wS3;  wX3 ^= wS2;

    // round #3 
    MUL(wX1, key[12]);
    wX2 += key[13];
    wX3 += key[14];
    MUL(wX4, key[15]);
    wS3 = wX3;
    wX3 ^= wX1;
    MUL(wX3, key[16]);
    wS2 = wX2;
    wX2 ^= wX4;
    wX2 += wX3;
    MUL(wX2, key[17]);
    wX3 += wX2;
    wX1 ^= wX2;  wX4 ^= wX3;
    wX2 ^= wS3;  wX3 ^= wS2;

    // round #4 
    MUL(wX1, key[18]);
    wX2 += key[19];
    wX3 += key[20];
    MUL(wX4, key[21]);
    wS3 = wX3;
    wX3 ^= wX1;
    MUL(wX3, key[22]);
    wS2 = wX2;
    wX2 ^= wX4;
    wX2 += wX3;
    MUL(wX2, key[23]);
    wX3 += wX2;
    wX1 ^= wX2;  wX4 ^= wX3;
    wX2 ^= wS3;  wX3 ^= wS2;

    // round #5 
    MUL(wX1, key[24]);
    wX2 += key[25];
    wX3 += key[26];
    MUL(wX4, key[27]);
    wS3 = wX3;
    wX3 ^= wX1;
    MUL(wX3, key[28]);
    wS2 = wX2;
    wX2 ^= wX4;
    wX2 += wX3;
    MUL(wX2, key[29]);
    wX3 += wX2;
    wX1 ^= wX2;  wX4 ^= wX3;
    wX2 ^= wS3;  wX3 ^= wS2;

    // round #6 
    MUL(wX1, key[30]);
    wX2 += key[31];
    wX3 += key[32];
    MUL(wX4, key[33]);
    wS3 = wX3;
    wX3 ^= wX1;
    MUL(wX3, key[34]);
    wS2 = wX2;
    wX2 ^= wX4;
    wX2 += wX3;
    MUL(wX2, key[35]);
    wX3 += wX2;
    wX1 ^= wX2;  wX4 ^= wX3;
    wX2 ^= wS3;  wX3 ^= wS2;

    // round #7 
    MUL(wX1, key[36]);
    wX2 += key[37];
    wX3 += key[38];
    MUL(wX4, key[39]);
    wS3 = wX3;
    wX3 ^= wX1;
    MUL(wX3, key[40]);
    wS2 = wX2;
    wX2 ^= wX4;
    wX2 += wX3;
    MUL(wX2, key[41]);
    wX3 += wX2;
    wX1 ^= wX2;  wX4 ^= wX3;
    wX2 ^= wS3;  wX3 ^= wS2;

    // round #8 
    MUL(wX1, key[42]);
    wX2 += key[43];
    wX3 += key[44];
    MUL(wX4, key[45]);
    wS3 = wX3;
    wX3 ^= wX1;
    MUL(wX3, key[46]);
    wS2 = wX2;
    wX2 ^= wX4;
    wX2 += wX3;
    MUL(wX2, key[47]);
    wX3 += wX2;
    wX1 ^= wX2;  wX4 ^= wX3;
    wX2 ^= wS3;  wX3 ^= wS2;

    // final semiround 
    MUL(wX1, key[48]);
    wX3 += key[49];
    wX2 += key[50];
    MUL(wX4, key[51]);

    // write the crypted block 
    out = (WORD16*) outbuf;
    *out++ = wX1;
    *out++ = wX3;
    *out++ = wX2;
    *out = wX4;
} 



WORD16 mulInv
  (WORD16 wX)     
{
    WORD16 wT0, wT1, wQ, wY;

    // 0 and 1 are self-inverse 
    if (wX <= 1) return wX; 

    // since wX >= 2, this fits into 16 bits 
    wT1 = 0x010001L / wX;   
    wY = 0x010001L % wX;
    
    if (wY == 1)
    {
      return (WORD16) low16(1 - wT1);
    } 
    wT0 = 1;

    do {
      wQ = wX / wY;
      wX = wX % wY;
      wT0 += wQ * wT1;
      if (wX == 1)  return wT0;
      wQ = wY / wX;
      wY = wY % wX;
      wT1 += wQ * wT0;
    } 
    while (wY != 1);

    return (WORD16) low16(1 - wT1);
} 



void ideaExpandKey
  (WORD8* userkey, 
   WORD16* ek)
{
    int nI, nJ;

    // expand 128bit key to an encryption key 
    for (nJ = 0; nJ < 8; nJ++) 
    {
      ek[nJ] = (userkey[0] << 8) + userkey[1];
      userkey += 2;
    }
    
    for (nI=0; nJ < IDEA_KEYLEN; nJ++) 
    {
      nI++;
      ek[nI + 7] = (ek[nI & 7] << 9) | (ek[nI + 1 & 7] >> 7);
      ek += nI & 8;
      nI &= 7;
    }
} 



#define NEG(x) (- (int) (x))

void ideaInvertKey
  (WORD16* ek, 
   WORD16 dk[IDEA_KEYLEN]) 
{
    WORD16 temp[IDEA_KEYLEN];
    register int nK, nP, nR;

    // key inversion for decryption 
    nP = IDEA_KEYLEN;
    temp[nP-1] = mulInv(ek[3]);
    temp[nP-2] = NEG(ek[2]);
    temp[nP-3] = NEG(ek[1]);
    temp[nP-4] = mulInv(ek[0]);

    nK = 4;
    nP -= 4;

    for (nR = IDEA_ROUNDS - 1; nR > 0; nR--) 
    {
      temp [nP-1] = ek[nK+1];
      temp [nP-2] = ek[nK];
      temp [nP-3] = mulInv(ek[nK+5]);
      temp [nP-4] = NEG(ek[nK+3]);
      temp [nP-5] = NEG(ek[nK+4]);
      temp [nP-6] = mulInv(ek[nK+2]);
      nK += 6; nP -= 6;
    }

    temp [nP-1] = ek[nK+1];
    temp [nP-2] = ek[nK];
    temp [nP-3] = mulInv(ek[nK+5]);
    temp [nP-4] = NEG(ek [nK+4]);
    temp [nP-5] = NEG(ek [nK+3]);
    temp [nP-6] = mulInv(ek[nK+2]);

    for (nK = 0; nK < IDEA_KEYLEN; nK++) 
    {
      dk[nK] = temp[nK];
      temp[nK] = 0;
    }
}
