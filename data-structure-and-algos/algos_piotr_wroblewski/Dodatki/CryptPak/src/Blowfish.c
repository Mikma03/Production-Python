

#include "Blowfish.h"

// include the boxes init. data
#include "BlowfishBoxes.h"


// Blowfish work context


typedef struct 
{
  // the boxes
  WORD32 boxes[BOXES_SIZE];
  
  // session CBC IV
  WORD32 lCBCLo;
  WORD32 lCBCHi;
} 
BLOWFISHCTX;



// prototypes of the support routines
void _keySetup(BLOWFISHCTX*, const WORD8*, WORD32);
void _blowfishEncipher(BLOWFISHCTX*, WORD32*, WORD32*);
void _blowfishDecipher(BLOWFISHCTX*, WORD32*, WORD32*);
BYTEBOOL _isWeakKey(BLOWFISHCTX*);


// box access constants
#define PBOX_POS    0
#define SBOX1_POS   PBOX_SIZE
#define SBOX2_POS   (PBOX_SIZE + SBOX_SIZE)
#define SBOX3_POS   (PBOX_SIZE + 2 * SBOX_SIZE)
#define SBOX4_POS   (PBOX_SIZE + 3 * SBOX_SIZE)



WORD32 Blowfish_GetCipherInfo
  (CIPHERINFOBLOCK* pInfo) 
{
  WORD32 lI;
  WORD8* pSrc;
  WORD8* pDst;
  CIPHERINFOBLOCK tempinfo;

  // prepare the information context
  tempinfo.lSizeOf = pInfo->lSizeOf;
  tempinfo.lBlockSize = BLOWFISH_BLOCKSIZE;
  tempinfo.lKeySize = BLOWFISH_KEYSIZE; 
  tempinfo.blOwnHasher = BOOL_FALSE;
  tempinfo.lInitDataSize = BLOWFISH_BLOCKSIZE;
  tempinfo.lContextSize = sizeof(BLOWFISHCTX);
  tempinfo.bCipherIs = CIPHER_IS_BLOCKLINK;

  // copy as many bytes of the information block as possible
  pSrc = (WORD8*) &tempinfo;
  pDst = (WORD8*) pInfo;
  
  for (lI = 0; lI < tempinfo.lSizeOf; lI++)
    *pDst++ = *pSrc++;

  return CIPHER_ERROR_NOERROR;
}



WORD32 Blowfish_SelfTest 
  (void* pTestContext) 
{
  WORD8 testKey1[8] = { 0x1c, 0x58, 0x7f, 0x1c, 0x13, 0x92, 0x4f, 0xef };
  WORD8* testKey2 = (WORD8*) "Who is John Galt?";

  // test the cipher for correct encryption and decryption
  BLOWFISHCTX* testCtx = (BLOWFISHCTX*) pTestContext;

  // test vector #1 (check for the signed bug)
  WORD32 tv_p1[2] = { 0x30553228, 0x6d6f295a };
  WORD32 tv_c1[2] = { 0x55cb3774, 0xd13ef201 };
  WORD32 tv_t1[2] = { 0x00000000, 0x00000000 };

  // test vector #2 (offical vector by Bruce Schneier)
  WORD32 tv_p2[2] = { 0xfedcba98, 0x76543210 };
  WORD32 tv_c2[2] = { 0xcc91732b, 0x8022f684 };
  WORD32 tv_t2[2] = { 0x00000000, 0x00000000 };

  // test pass #1
  _keySetup(testCtx, testKey1, 8);
  _blowfishEncipher(testCtx, tv_p1, tv_t1);
  if ((tv_c1[0] != tv_t1[0]) || (tv_c1[1] != tv_t1[1])) 
    return CIPHER_ERROR_INVALID;
  _blowfishDecipher(testCtx, tv_t1, tv_t1);
  if ((tv_p1[0] != tv_t1[0]) || (tv_p1[1] != tv_t1[1]))
    return CIPHER_ERROR_INVALID;

  // test pass #2
  _keySetup(testCtx, testKey2, 17);
  _blowfishEncipher(testCtx, tv_p2, tv_t2);
  if ((tv_c2[0] != tv_t2[0]) || (tv_c2[1] != tv_t2[1]))
    return CIPHER_ERROR_INVALID;
  _blowfishDecipher(testCtx, tv_t2, tv_t2);
  if ((tv_p2[0] != tv_t2[0]) || (tv_p2[1] != tv_t2[1])) 
    return CIPHER_ERROR_INVALID;

  // all tests passed
  return CIPHER_ERROR_NOERROR;
}



WORD32 Blowfish_CreateWorkContext
  (void* pContext,
   const WORD8* pKey,
   WORD32 lKeyLen,
   WORD32 lMode,
   void* pInitData,
   Cipher_RandomGenerator GetRndBytes,
   const void* pRndGenData) 
{
  BLOWFISHCTX* pCtx = (BLOWFISHCTX*) pContext;
  WORD32* pCBCIV;

  // do the key setup (we ignore the passed key length now)
  _keySetup(pCtx, pKey, BLOWFISH_KEYSIZE);

  // for encryption create a CBC IV
  pCBCIV = (WORD32*) pInitData;
  if (lMode == CIPHER_MODE_ENCRYPT)
  {
    GetRndBytes((WORD8*) pCBCIV, BLOWFISH_BLOCKSIZE, pRndGenData);
  }

  // set the CBC IV
  pCtx->lCBCLo = pCBCIV[0];
  pCtx->lCBCHi = pCBCIV[1];
  
  // check for weak keys and quit
  return (_isWeakKey(pCtx) == BOOL_TRUE) ? 
    CIPHER_ERROR_WEAKKEY : CIPHER_ERROR_NOERROR;
}


void Blowfish_ResetWorkContext
  (void* pContext,
   WORD32 lMode,
   void* pInitData,
   Cipher_RandomGenerator GetRndBytes,
   const void* pRndGenData) 
{
  BLOWFISHCTX* pCtx = (BLOWFISHCTX*) pContext;

  // just reset the CBC IV 
  WORD32* pCBCIV = (WORD32*) pInitData;
  if (lMode == CIPHER_MODE_ENCRYPT) 
  GetRndBytes((WORD8*) pCBCIV, 8, pRndGenData);
  pCtx->lCBCLo = pCBCIV[0];
  pCtx->lCBCHi = pCBCIV[1];
}



WORD32 Blowfish_DestroyWorkContext
  (void* pContext) 
{
  // clear the context
  int nI;
  WORD8* clearIt = (WORD8*) pContext;
  for (nI = 0; nI < sizeof(BLOWFISHCTX); nI++) clearIt[nI] = 0x00;
  return CIPHER_ERROR_NOERROR;
}



void Blowfish_EncryptBuffer
  (void* pContext,
   const void* pSource,
   void* pTarget,
   WORD32 lNumOfBytes) 
{
  WORD32 lNumOfInts;
  WORD32 lI;
  WORD32* pInBuf = (WORD32*) pSource;
  WORD32* pOutBuf = (WORD32*) pTarget;
  BLOWFISHCTX* pCtx = (BLOWFISHCTX*) pContext;

  // calculate the number of (32bit) words
  lNumOfInts = lNumOfBytes >> 2;

  // anything to encrypt?
  if (lNumOfInts < 2) return;

  // work through all blocks... 
  for (lI = 0; lI < lNumOfInts; lI+=2) 
  {
     // copy and chain the recent block 
     pOutBuf[lI]     = pInBuf[lI]     ^ pCtx->lCBCLo;
     pOutBuf[lI + 1] = pInBuf[lI + 1] ^ pCtx->lCBCHi;

     // encrypt the block
     _blowfishEncipher(pCtx, &pOutBuf[lI], &pOutBuf[lI]);

     // set the new CBC iv
     pCtx->lCBCLo = pOutBuf[lI];
     pCtx->lCBCHi = pOutBuf[lI + 1];
  }
}



void Blowfish_DecryptBuffer
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
  BLOWFISHCTX* pCtx = (BLOWFISHCTX*) pContext;

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
     _blowfishDecipher(pCtx, &pInBuf[lI], &pOutBuf[lI]);

     // dechain the recent block
     pOutBuf[lI]     = pOutBuf[lI]     ^ pCtx->lCBCLo;
     pOutBuf[lI + 1] = pOutBuf[lI + 1] ^ pCtx->lCBCHi;

     // set the new CBC iv
     pCtx->lCBCLo = lSaveCBCLo;
     pCtx->lCBCHi = lSaveCBCHi;
  }
}




// support routines...


// to setup a key (was extracted for an easier selftest implementation)
void _keySetup
  (BLOWFISHCTX* pCtx,
   const WORD8* pKey,
   WORD32 lKeyLen) 
{ 
  int nI;
  int nJ;
  WORD32 lKeyPos = 0;
  WORD32 lBuf = 0;
  WORD32 zerostr[2];

  // copy the init. data to the context
  for (nI = 0; nI < BOXES_SIZE; nI++) pCtx->boxes[nI] = boxes_init[nI];

  // we accept zero keys 
  if (lKeyLen == 0) return;

  // xor the key over the p-boxes, warp around
  for (nI = 0; nI < PBOX_SIZE; nI++) 
  {
    for (nJ = 0; nJ < 4; nJ++) 
    {
      if (lKeyPos == lKeyLen) lKeyPos = 0;
      lBuf <<= 8;
      lBuf |= (WORD32)(pKey[lKeyPos++] & 0x0ff);
    }
    pCtx->boxes[nI] ^= lBuf;
  }

  // now encrypt the all zero string and replace all boxes...
  zerostr[0] = zerostr[1] = 0x00000000;

  // encrypt the p- and the s-boxes (all together using the base pointer)
  for (nI = 0; nI < BOXES_SIZE; nI += 2) 
  {
    _blowfishEncipher(pCtx, zerostr, zerostr);
    pCtx->boxes[nI]   = zerostr[0];
    pCtx->boxes[nI+1] = zerostr[1];
  }
}



// one encryption loop (swapable)
#define ENC_LOOP(LOOPNUM, LEFT, RIGHT) LEFT ^= pbox[LOOPNUM];\
                                       RIGHT ^= ((sbox1[LEFT >> 24] +\
                                                sbox2[(LEFT >> 16) & 0x0ff]) ^\
                                                sbox3[(LEFT >> 8) & 0x0ff]) +\
                                                sbox4[LEFT & 0x0ff];

// the encryption routine
void _blowfishEncipher
  (BLOWFISHCTX* pCtx,
   WORD32* srcbuf,
   WORD32* targetbuf) 
{
  // create box pointers for faster access   
  WORD32* pbox = &pCtx->boxes[PBOX_POS];
  WORD32* sbox1 = &pCtx->boxes[SBOX1_POS];
  WORD32* sbox2 = &pCtx->boxes[SBOX2_POS];
  WORD32* sbox3 = &pCtx->boxes[SBOX3_POS];
  WORD32* sbox4 = &pCtx->boxes[SBOX4_POS];

  // get the block
  register WORD32 lLeft = srcbuf[0];
  register WORD32 lRight = srcbuf[1];

  // the encryption loop (unrolled) */
  ENC_LOOP(0, lLeft, lRight)  
  ENC_LOOP(1, lRight, lLeft)  
  ENC_LOOP(2, lLeft, lRight)  
  ENC_LOOP(3, lRight, lLeft)  
  ENC_LOOP(4, lLeft, lRight)  
  ENC_LOOP(5, lRight, lLeft)  
  ENC_LOOP(6, lLeft, lRight)  
  ENC_LOOP(7, lRight, lLeft)  
  ENC_LOOP(8, lLeft, lRight)  
  ENC_LOOP(9, lRight, lLeft)  
  ENC_LOOP(10, lLeft, lRight)  
  ENC_LOOP(11, lRight, lLeft)  
  ENC_LOOP(12, lLeft, lRight)  
  ENC_LOOP(13, lRight, lLeft)  
  ENC_LOOP(14, lLeft, lRight)  
  ENC_LOOP(15, lRight, lLeft)  

  // swap, finalize and store the block back
  targetbuf[1] = lLeft ^ pbox[16];
  targetbuf[0] = lRight ^ pbox[17];
}


// the decryption routine
void _blowfishDecipher
  (BLOWFISHCTX* pCtx,
   WORD32* srcbuf,
   WORD32* targetbuf) 
{
  // create box pointers for faster access   
  WORD32* pbox = &pCtx->boxes[PBOX_POS];
  WORD32* sbox1 = &pCtx->boxes[SBOX1_POS];
  WORD32* sbox2 = &pCtx->boxes[SBOX2_POS];
  WORD32* sbox3 = &pCtx->boxes[SBOX3_POS];
  WORD32* sbox4 = &pCtx->boxes[SBOX4_POS];

  // get the block
  WORD32 lLeft = srcbuf[0];
  WORD32 lRight = srcbuf[1];

  /* the decryption loop (unrolled) */
  ENC_LOOP(17, lLeft, lRight)  
  ENC_LOOP(16, lRight, lLeft)  
  ENC_LOOP(15, lLeft, lRight)  
  ENC_LOOP(14, lRight, lLeft)  
  ENC_LOOP(13, lLeft, lRight)  
  ENC_LOOP(12, lRight, lLeft)  
  ENC_LOOP(11, lLeft, lRight)  
  ENC_LOOP(10, lRight, lLeft)  
  ENC_LOOP(9, lLeft, lRight)  
  ENC_LOOP(8, lRight, lLeft)  
  ENC_LOOP(7, lLeft, lRight)  
  ENC_LOOP(6, lRight, lLeft)  
  ENC_LOOP(5, lLeft, lRight)  
  ENC_LOOP(4, lRight, lLeft)  
  ENC_LOOP(3, lLeft, lRight)  
  ENC_LOOP(2, lRight, lLeft)
  
  // swap, finalize and store the block back
  targetbuf[1] = lLeft ^ pbox[1];
  targetbuf[0] = lRight ^ pbox[0];
}


// to check for a weak key (equal s-box entries)
BYTEBOOL _isWeakKey
  (BLOWFISHCTX* pCtx) 
{
  int nI, nJ;
  for (nI = 0; nI < 255; nI++) 
  {
    for (nJ = nI + 1; nJ < 256; nJ++) 
    {
      if (pCtx->boxes[SBOX1_POS + nI] == pCtx->boxes[SBOX1_POS + nJ]) return BOOL_TRUE;   
      if (pCtx->boxes[SBOX2_POS + nI] == pCtx->boxes[SBOX2_POS + nJ]) return BOOL_TRUE;   
      if (pCtx->boxes[SBOX3_POS + nI] == pCtx->boxes[SBOX3_POS + nJ]) return BOOL_TRUE;   
      if (pCtx->boxes[SBOX4_POS + nI] == pCtx->boxes[SBOX4_POS + nJ]) return BOOL_TRUE;   
    }
  }

  // no weak key detected
  return BOOL_FALSE;
}
