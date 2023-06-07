

#include "Cobra128.h"

// here we load init. data for the boxes 
#include "Cobra128_tab.h"



// driver work context 
typedef struct 
{
  // boxes 
  WORD32 pbox[12][3];
  WORD32 sbox1[4][256];
  WORD32 sbox2[4][256];
  WORD32 sbox3[4][256];
  WORD32 wbox[2][4];
  // CBC initalisation vector 
  WORD32 cbc_iv[4];
} 
COBRA128CTX;



// some macros, used to make the code more ledigble and to
// increase the speed by unrolling the loops... 

// 32bit rotations, might be replaced by inline assembly 
#define ROTL32(a, i)    ((a<<i) | (a>>(32-i)))
#define ROTR32(a, i)    ((a>>i) | (a<<(32-i)))

// the F function in a "compressed" form 
#define F(RESULT, Y, PBOX, SBOX) lTemp = Y ^ PBOX;\
                                 RESULT = ( ( SBOX[0][lTemp >> 24] +\
                                          SBOX[1][(lTemp >> 16) & 0x0ff] ) ^\
                                          SBOX[2][(lTemp >> 8) & 0x0ff] ) +\
                                          SBOX[3][lTemp & 0x0ff];       

// one loop for encryption 
#define ENC_LOOP(LOOPNUM) lSaveA = lA;\
                          lSaveB = lB;\
                          lSaveC = lC;\
                          lSaveD = lD;\
                          lD = lSaveA;\
                          F(lC, lD, pCtx->pbox[LOOPNUM][2], pCtx->sbox3)\
                          lC ^= lSaveD;\
                          lC = ROTR32(lC, 1);\
                          F(lB, lC, pCtx->pbox[LOOPNUM][1], pCtx->sbox2)\
                          lB ^= lSaveC;\
                          lB = ROTR32(lB, 1);\
                          F(lA, lB, pCtx->pbox[LOOPNUM][0], pCtx->sbox1)\
                          lA ^= lSaveB;\
                          lA = ROTR32(lA, 1); 

// one loop for decryption 
#define DEC_LOOP(LOOPNUM) lSaveA = lA;\
                          lSaveB = lB;\
                          lSaveC = lC;\
                          lSaveD = lD;\
                          lA = lSaveD;\
                          F(lB, lSaveB, pCtx->pbox[LOOPNUM][0], pCtx->sbox1);\
                          lB ^= ROTL32(lSaveA, 1);\
                          F(lC, lSaveC, pCtx->pbox[LOOPNUM][1], pCtx->sbox2);\
                          lC ^= ROTL32(lSaveB, 1);\
                          F(lD, lSaveD, pCtx->pbox[LOOPNUM][2], pCtx->sbox3);\
                          lD ^= ROTL32(lSaveC, 1);


// the encryption routine 
void _cobra128_encipher
  (COBRA128CTX* pCtx, 
   WORD32* blockToEncrypt) 
{

  // me must use the same variables as in the macros above 
  WORD32 lTemp;
  WORD32 lA, lB, lC, lD;
  WORD32 lSaveA, lSaveB, lSaveC, lSaveD;

  // copy the 128bit block to local variables, to increase the execution speed 
  lA = blockToEncrypt[0];
  lB = blockToEncrypt[1];
  lC = blockToEncrypt[2];
  lD = blockToEncrypt[3];

  // whitening #1 
  lA ^= pCtx->wbox[0][0];
  lB ^= pCtx->wbox[0][1];
  lC ^= pCtx->wbox[0][2];
  lD ^= pCtx->wbox[0][3];

  // the encryption loop (unrolled) 
  
  ENC_LOOP(0)  
  ENC_LOOP(1)  
  ENC_LOOP(2)  
  ENC_LOOP(3)  
  ENC_LOOP(4)  
  ENC_LOOP(5)  
  ENC_LOOP(6)  
  ENC_LOOP(7)  
  ENC_LOOP(8)  
  ENC_LOOP(9)  
  ENC_LOOP(10)  
  ENC_LOOP(11)  
    
  // whitening #2 
  lA ^= pCtx->wbox[1][0];
  lB ^= pCtx->wbox[1][1];
  lC ^= pCtx->wbox[1][2];
  lD ^= pCtx->wbox[1][3];  

  // store the 128bit block back 
  blockToEncrypt[0] = lA;
  blockToEncrypt[1] = lB;
  blockToEncrypt[2] = lC;
  blockToEncrypt[3] = lD;
}


// the decryption routine (nearly the same as above) 
void _cobra128_decipher
  (COBRA128CTX* pCtx, 
   WORD32* blockToEncrypt) 
{
  WORD32 lTemp;
  WORD32 lA, lB, lC, lD;
  WORD32 lSaveA, lSaveB, lSaveC, lSaveD;

  lA = blockToEncrypt[0];
  lB = blockToEncrypt[1];
  lC = blockToEncrypt[2];
  lD = blockToEncrypt[3];

  lA ^= pCtx->wbox[1][0];
  lB ^= pCtx->wbox[1][1];
  lC ^= pCtx->wbox[1][2];
  lD ^= pCtx->wbox[1][3];

  DEC_LOOP(11)
  DEC_LOOP(10)  
  DEC_LOOP(9)  
  DEC_LOOP(8)  
  DEC_LOOP(7)  
  DEC_LOOP(6)  
  DEC_LOOP(5)  
  DEC_LOOP(4)  
  DEC_LOOP(3)  
  DEC_LOOP(2)  
  DEC_LOOP(1)  
  DEC_LOOP(0)  
    
  lA ^= pCtx->wbox[0][0];
  lB ^= pCtx->wbox[0][1];
  lC ^= pCtx->wbox[0][2];
  lD ^= pCtx->wbox[0][3];
  
  blockToEncrypt[0] = lA;
  blockToEncrypt[1] = lB;
  blockToEncrypt[2] = lC;
  blockToEncrypt[3] = lD;
}



WORD32 Cobra128_GetCipherInfo
  (CIPHERINFOBLOCK* pInfo) 
{
  WORD32 lI;
  WORD8* pSrc;
  WORD8* pDst;
  CIPHERINFOBLOCK tempinfo;

  // prepare the information context
  tempinfo.lSizeOf = pInfo->lSizeOf;
  tempinfo.lBlockSize = COBRA128_BLOCKSIZE;
  tempinfo.lKeySize = COBRA128_KEYSIZE; 
  tempinfo.blOwnHasher = BOOL_FALSE;
  tempinfo.lInitDataSize = COBRA128_BLOCKSIZE;
  tempinfo.lContextSize = sizeof(COBRA128CTX);
  tempinfo.bCipherIs = CIPHER_IS_BLOCKLINK;

  // copy as many bytes of the information block as possible
  pSrc = (WORD8*) &tempinfo;
  pDst = (WORD8*) pInfo;
  for (lI = 0; lI < tempinfo.lSizeOf; lI++) 
  { 
    *pDst++ = *pSrc++;
  }

  return CIPHER_ERROR_NOERROR;
}



WORD32 Cobra128_SelfTest 
  (void* pCtxBuf) 
{
  // encrypt, decrypt and check a test vector,
  // mainly implemented to check the boxes init. data

  int nI;

  COBRA128CTX* pCtx = (COBRA128CTX*) pCtxBuf;
  
  WORD8* testkey = (WORD8*) "Hogan's Heros";

  WORD32 plaintext[4] = { 0xBBE8C372,0x16C4AE90,0xDAF9431F,0xA39FFBD6 };

  WORD32 ciphertext[4];
  WORD32 cipher_must[4] = { 0x0712D251,0x3D49CA7D,0x90969E09,0xD9F36687 };

  WORD8 initdata[COBRA128_BLOCKSIZE];

  // create a context (used for en- and decryption,
  // because CBC isn't used and we init. in decryption
  // mode we don't need a random number generator)
  Cobra128_CreateWorkContext(pCtx, 
                             testkey,
                             13,
                             CIPHER_MODE_DECRYPT, 
                             initdata, 
                             0, 
                             0);

  // test the encryption 
  for (nI = 0; nI < 4; nI++) 
  { 
    ciphertext[nI] = plaintext[nI]; 
  }

  _cobra128_encipher(pCtx, ciphertext);

  for (nI = 0; nI < 4; nI++)
  {
    if (ciphertext[nI] != cipher_must[nI]) 
    {
      return CIPHER_ERROR_INVALID;
    }
  }

  // test the decryption 
  _cobra128_decipher(pCtx, ciphertext);

  for (nI = 0; nI < 4; nI++) 
  {
    if (ciphertext[nI] != plaintext[nI]) 
    {
      return CIPHER_ERROR_INVALID;
    }
  }
    
  // tests passed 
  return CIPHER_ERROR_NOERROR;
}




WORD32 Cobra128_CreateWorkContext
  (void* pContext,
   const WORD8* pKey,
   WORD32 lKeyLen,
   WORD32 lMode,
   void* pInitData,
   Cipher_RandomGenerator GetRndBytes,
   const void* pRndGenData) 
{

  int nI, nJ, nK, nLoop;
  WORD32 lKeyPos;
  WORD32 azs[4];
  WORD32 lBuf = 0;
  WORD32* pHelpPtr;
  COBRA128CTX* pCtx = (COBRA128CTX*) pContext;

  // copy the init. data to the context 
  nK = 0;
  for (nJ = 0; nJ < 12; nJ++) 
  {
    for (nI = 0; nI < 3; nI++) pCtx->pbox[nJ][nI] = box_init[nK++];
  }
  for (nJ = 0; nJ < 4; nJ++) 
  {
    for (nI = 0; nI < 256; nI++) pCtx->sbox1[nJ][nI] = box_init[nK++];
  }
  for (nJ = 0; nJ < 4; nJ++) 
  {
    for (nI = 0; nI < 256; nI++) pCtx->sbox2[nJ][nI] = box_init[nK++];    
  }
  for (nJ = 0; nJ < 4; nJ++) 
  {
    for (nI = 0; nI<256; nI++) pCtx->sbox3[nJ][nI] = box_init[nK++];
  }
  for (nJ = 0; nJ < 2; nJ++) 
  {
    for (nI = 0; nI < 4; nI++) pCtx->wbox[nJ][nI] = box_init[nK++];
  }

  // xor the key over the boxes, warp arowd 
  lKeyPos = 0;
  
  // xor the p-boxes 
  for (nJ = 0; nJ < 12; nJ++) 
  {
    for (nI = 0; nI < 3; nI++) 
    {
      for (nK = 0, lBuf = 0; nK < 4; nK++) 
      {
        if (lKeyPos >= lKeyLen) lKeyPos = 0;
        lBuf = (lBuf << 8) | (WORD32)(pKey[lKeyPos++] & 0x0ff); 
      }
      pCtx->pbox[nJ][nI] ^= lBuf;
    }
  }

  // xor over the 1st S-Unit 
  for (nJ = 0; nJ < 4; nJ++) 
  {
    for (nI = 0; nI < 256; nI++) 
    {
      for (nK = 0; nK < 4; nK++) 
      {
        if (lKeyPos >= lKeyLen) lKeyPos = 0;
        lBuf = (lBuf << 8) | (WORD32)(pKey[lKeyPos++] & 0x0ff); 
      }
      pCtx->sbox1[nJ][nI] ^= lBuf;
    }
  }

  // xor over the 2nd S-Unit 
  for (nJ=0; nJ < 4; nJ++) 
  {
    for (nI = 0; nI < 256; nI++) 
    {
      for (nK = 0; nK < 4; nK++) 
      {
        if (lKeyPos >= lKeyLen) lKeyPos = 0;
        lBuf = (lBuf << 8) | (WORD32)(pKey[lKeyPos++] & 0x0ff); 
      }
      pCtx->sbox2[nJ][nI] ^= lBuf;
    }
  }

  // xor over the 3rd S-Unit 
  for (nJ = 0; nJ < 4; nJ++) 
  {
    for (nI = 0; nI < 256; nI++) 
    {
      for (nK = 0; nK < 4; nK++) 
      {
        if (lKeyPos >= lKeyLen) lKeyPos = 0;
        lBuf = (lBuf << 8) | (WORD32)(pKey[lKeyPos++] & 0x0ff); 
      }
      pCtx->sbox3[nJ][nI] ^= lBuf;
    }
  }

  
  for (nLoop = 0; nLoop < 2; nLoop++) 
  {
    // now we encrypt an all zero string and replace all boxes 
    azs[0] = azs[1] = azs[2] = azs[3] = 0x00000000;        
  
    // encrypt the pboxes 
    pHelpPtr = &pCtx->pbox[0][0]; // (use a help pointer to access the boxes) 
    for (nI = 0; nI < 9; nI++) 
    {
      _cobra128_encipher(pCtx, azs);  
      *(pHelpPtr++) = azs[0];
      *(pHelpPtr++) = azs[1];
      *(pHelpPtr++) = azs[2];
      *(pHelpPtr++) = azs[3];
    }

    // encrypt the 1st S-Unit 
    pHelpPtr = &pCtx->sbox1[0][0];
    for (nI = 0; nI < 256; nI++) 
    {
      _cobra128_encipher(pCtx, azs);
      *(pHelpPtr++) = azs[0];
      *(pHelpPtr++) = azs[1];
      *(pHelpPtr++) = azs[2];
      *(pHelpPtr++) = azs[3];
    }

    // encrypt the 2nd S-Unit 
    pHelpPtr = &pCtx->sbox2[0][0];
    for (nI = 0; nI < 256; nI++) 
    {
      _cobra128_encipher(pCtx, azs);
      *(pHelpPtr++) = azs[0];
      *(pHelpPtr++) = azs[1];
      *(pHelpPtr++) = azs[2];
      *(pHelpPtr++) = azs[3];
    }

    // encrypt the 3rd S-Unit 
    pHelpPtr = &pCtx->sbox3[0][0];
    for (nI = 0; nI < 256; nI++) 
    {
      _cobra128_encipher(pCtx, azs);
      *(pHelpPtr++) = azs[0];
      *(pHelpPtr++) = azs[1];
      *(pHelpPtr++) = azs[2];
      *(pHelpPtr++) = azs[3];
    }

    // encrypt the wboxes 
    pHelpPtr = &pCtx->wbox[0][0];
    for (nI = 0; nI < 2; nI++) 
    {
      _cobra128_encipher(pCtx, azs);
      *(pHelpPtr++) = azs[0];
      *(pHelpPtr++) = azs[1];
      *(pHelpPtr++) = azs[2];
      *(pHelpPtr++) = azs[3];
    }

    // in the 1st loop: again do the same xoring as above, 
    // but this time only the p-boxes 
    if (nLoop == 0) 
    {
      lKeyPos = 0;
      // xor the p-boxes 
      for (nJ = 0; nJ < 12; nJ++) 
      {
        for (nI = 0; nI < 3; nI++) 
        {
          for (nK = 0; nK < 4; nK++)
          {
            if (lKeyPos >= lKeyLen) lKeyPos = 0;
            lBuf = (lBuf << 8) | (WORD32)(pKey[lKeyPos++] & 0x0ff); 
          }
          pCtx->pbox[nJ][nI] ^= lBuf;
        }
      }
    }
  }

  // create and save the CBC iv or get it for decryption 
  pHelpPtr = (WORD32*) pInitData;
  if (lMode == CIPHER_MODE_ENCRYPT) 
  {
    GetRndBytes((WORD8*)&pCtx->cbc_iv[0], 16, pRndGenData);
    for (nI = 0; nI < 4; nI++) pHelpPtr[nI] = pCtx->cbc_iv[nI];
  }
  else 
  {
    for (nI = 0; nI < 4; nI++) pCtx->cbc_iv[nI] = pHelpPtr[nI];
  }

  return CIPHER_ERROR_NOERROR;
}



void Cobra128_ResetWorkContext
  (void* pContext,
   WORD32 lMode,
   void* pInitData,
   Cipher_RandomGenerator GetRndBytes,
   const void* pRndGenData) 
{
  int nI;
  WORD32* pHelpPtr;
  COBRA128CTX* pCtx = (COBRA128CTX*) pContext;

  // create and save the CBC iv or get it for decryption 
  pHelpPtr = (WORD32*) pInitData;
  if (lMode == CIPHER_MODE_ENCRYPT) 
  {
    GetRndBytes((WORD8*)&pCtx->cbc_iv[0], 16, pRndGenData);
    for (nI = 0; nI < 4; nI++) pHelpPtr[nI] = pCtx->cbc_iv[nI];
  }
  else 
  {
    for (nI = 0; nI < 4; nI++) pCtx->cbc_iv[nI] = pHelpPtr[nI];
  }
}



WORD32 Cobra128_DestroyWorkContext 
  (void* pContext) 
{
  WORD8* pDel = (WORD8*) pContext;
  int nI;

  // just clear the context
  for (nI = 0; nI < sizeof(COBRA128CTX); nI++) *(pDel++) = 0x00; 

  return CIPHER_ERROR_NOERROR;
}



void Cobra128_EncryptBuffer
  (void* pContext, 
   const void* pSource, 
   void* pTarget,
   WORD32 lNumOfBytes) 
{
  WORD32 lI, lJ;
  WORD32* pInBuf = (WORD32*) pSource;
  WORD32* pOutBuf = (WORD32*) pTarget;
  COBRA128CTX* pCtx = (COBRA128CTX*) pContext;
  
  // work through all blocks 
  for (lI = 0; lI < (lNumOfBytes / COBRA128_BLOCKSIZE); lI++) {
    
    // copy and chain the actual block  
    for (lJ = 0; lJ < 4; lJ++) 
    {
      pOutBuf[lJ] = pInBuf[lJ]; 
      pOutBuf[lJ] ^= pCtx->cbc_iv[lJ];
    }

    // encrypt the block 
    _cobra128_encipher(pCtx, pOutBuf);

    // set the new cbc iv 
    for (lJ = 0; lJ < 4; lJ++) pCtx->cbc_iv[lJ] = pOutBuf[lJ];

    // next block 
    pInBuf += COBRA128_BLOCKSIZE / sizeof(WORD32);
    pOutBuf += COBRA128_BLOCKSIZE / sizeof(WORD32);
  }
}



void Cobra128_DecryptBuffer
  (void* pContext, 
   const void* pSource, 
   void* pTarget, 
   WORD32 lNumOfBytes, 
   const void* pPreviousBlock) 
{
  WORD32 lI, lJ;
  WORD32* pInBuf = (WORD32*) pSource;
  WORD32* pOutBuf = (WORD32*) pTarget;
  WORD32 save_cbc_iv[4];
  COBRA128CTX* pCtx = (COBRA128CTX*) pContext;

  // load a new CBC IV, if necessary 
  if (pPreviousBlock != CIPHER_NULL)  
  {
    for (lI = 0; lI < 4; lI++) pCtx->cbc_iv[lI] = ((WORD32*)pPreviousBlock)[lI];
  }
  
  // work through all blocks 
  for (lI = 0; lI < (lNumOfBytes / COBRA128_BLOCKSIZE); lI++) 
  {
    // copy and chain the actual block  
    for (lJ = 0; lJ < 4; lJ++) pOutBuf[lJ] = save_cbc_iv[lJ] = pInBuf[lJ];
    
    // encrypt the block 
    _cobra128_decipher(pCtx, pOutBuf);

    // rechain the block and set the new cbc iv 
    for (lJ = 0; lJ < 4; lJ++) 
    {
      pOutBuf[lJ] ^= pCtx->cbc_iv[lJ];
      pCtx->cbc_iv[lJ] = save_cbc_iv[lJ];
    }

    // next block 
    pInBuf += COBRA128_BLOCKSIZE / sizeof(WORD32);
    pOutBuf += COBRA128_BLOCKSIZE / sizeof(WORD32);
  }
}
