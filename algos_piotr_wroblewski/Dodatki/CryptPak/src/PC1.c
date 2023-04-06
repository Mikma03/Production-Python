

#include "pc1.h"


typedef struct 
{
  WORD32 state[256];
  WORD32 lX, lY;

  // we hold a copy of the initial state after the key setup 
  // for a fast reset
  WORD32 saveState[256];
  WORD32 lSaveX, lSaveY;

} 
PC1CTX;



WORD32 PC1_GetCipherInfo
  (CIPHERINFOBLOCK* pInfo) 
{
  CIPHERINFOBLOCK tempinfo;
  WORD8* pSrc;
  WORD8* pDst;
  WORD32 lI;

  // prepare the information context
  tempinfo.lSizeOf = pInfo->lSizeOf;
  tempinfo.lBlockSize = PC1_BLOCKSIZE;
  tempinfo.lKeySize = PC1_KEYSIZE;
  tempinfo.blOwnHasher = BOOL_FALSE;
  tempinfo.lInitDataSize = 0;
  tempinfo.lContextSize = sizeof(PC1CTX);
  tempinfo.bCipherIs = CIPHER_IS_XORSTREAM;

  // copy as many bytes of the information block as possible
  pSrc = (WORD8*) &tempinfo;
  pDst = (WORD8*) pInfo;

  for (lI = 0; lI < tempinfo.lSizeOf; lI++)
    *pDst++ = *pSrc++;

  return CIPHER_ERROR_NOERROR;
}


static WORD8 refKey[5] = { 0x61, 0x8a, 0x63, 0xd2, 0xfb };
static WORD8 ptext[5] = { 0xdc, 0xee, 0x4c, 0xf9, 0x2c };
static WORD8 ctext[5] = { 0xf1, 0x38, 0x29, 0xc9, 0xde };


WORD32 PC1_SelfTest 
  (void* pTestContext) 
{
  WORD8 etext[5];
  WORD8 dtext[5];

  char ctx[sizeof(PC1CTX)];

  int nI;

  for (nI = 0; nI < 5; nI++)
    etext[nI] = dtext[nI] = 0;

  PC1_CreateWorkContext(&ctx,
                        refKey,
                        (WORD32)5,
                        (WORD32)0,
                        (void*)0,   // don't care...
                        0,
                        (void*)0);

  PC1_EncryptBuffer(&ctx,
                    ptext,
                    etext,
                    5);
  
  for (nI = 0; nI < 5; nI++)
    if (ctext[nI] != etext[nI])
      return CIPHER_ERROR_INVALID;

  PC1_ResetWorkContext(&ctx,
                       (WORD32)0,
                       (void*)0,
                       0,
                       (void*)0);

  PC1_DecryptBuffer(&ctx,
                    etext,
                    dtext,
                    5,
                    (void*)0);

  for (nI = 0; nI < 5; nI++)
    if (ptext[nI] != dtext[nI])
      return CIPHER_ERROR_INVALID;

  return CIPHER_ERROR_NOERROR;
}


WORD32 PC1_CreateWorkContext
  (void* pContext,
   const WORD8* pKey,
   WORD32 lKeyLen, 
   WORD32 lMode,
   void* pInitData,
   Cipher_RandomGenerator GetRndBytes,
   const void *pRndGenData) 
{
  PC1CTX* pCtx = (PC1CTX*) pContext;
  int nX;
  WORD32 lKeyPos = 0;
  WORD32 lSX, lY = 0;
  WORD32* state = &pCtx->state[0];

  pCtx->lX = pCtx->lY = 0;
  for (nX = 0; nX < 256; nX++)
    state[nX] = nX;

  for (nX = 0; nX < 256; nX++) 
  {
    lSX = state[nX];
    lY += lSX + pKey[lKeyPos];
    lY &= 0x00ff;
    state[nX] = state[lY];
    state[lY] = lSX;
    if (++lKeyPos == lKeyLen)
      lKeyPos = 0;
  }

  for (nX = 0; nX < 256; nX++)
    pCtx->saveState[nX] = pCtx->state[nX];
  pCtx->lSaveX = pCtx->lX; 
  pCtx->lSaveY = pCtx->lY;

  return CIPHER_ERROR_NOERROR;
}


void PC1_ResetWorkContext
  (void* pContext, 
   WORD32 lMode,
   void* pInitData,
   Cipher_RandomGenerator GetRndBytes,
   const void *pRndGenData) 
{
  PC1CTX* pCtx = (PC1CTX*) pContext;
  int nI;

  // just redo the key setup by copying the orginal state
  for (nI = 0; nI < 256; nI++)
    pCtx->state[nI] = pCtx->saveState[nI];

  pCtx->lX = pCtx->lSaveX; 
  pCtx->lY = pCtx->lSaveY;
}


WORD32 PC1_DestroyWorkContext 
  (void* pContext) 
{
  // clear the context
  WORD8* pClearIt = (WORD8*) pContext;
  int nI;
  for (nI = 0; nI < sizeof(PC1CTX); nI++)
    pClearIt[nI] = 0x00;
  return CIPHER_ERROR_NOERROR;
}



void PC1_EncryptBuffer
  (void* pContext, 
   const void* pSource, 
   void* pTarget,
   WORD32 lNumOfBytes) 
{
  PC1CTX* pCtx = (PC1CTX*) pContext;
  WORD32 lX = pCtx->lX;
  WORD32 lY = pCtx->lY;
  WORD32* state = &pCtx->state[0];
  WORD8* pDataIn = (WORD8*) pSource;
  WORD8* pDataOut = (WORD8*) pTarget;
  WORD32 lSX, lSY;

  while (lNumOfBytes--) 
  {
    lX++;
    lX &= 0x00ff;
    lSX = state[lX];
    lY += lSX;
    lY &= 0x00ff;
    lSY = state[lY];
    state[lY] = lSX;
    state[lX] = lSY;
    *pDataOut++ = *pDataIn++ ^ (WORD8)state[(lSX + lSY) & 0x00ff];
  }

  pCtx->lX = lX;
  pCtx->lY = lY;
}



void PC1_DecryptBuffer
  (void* pContext, 
   const void* pSource, 
   void* pTarget,
   WORD32 lNumOfBytes, 
   const void* pPreviousBlock) 
{
  // just map the call, previous blocks aren't significant
  PC1_EncryptBuffer(pContext, 
                    pSource, 
                    pTarget, 
                    lNumOfBytes);
}
