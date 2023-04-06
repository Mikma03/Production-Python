

#include "CipherServer.h"
#include "cpkernel.h"
#include "Yarrow.h"

#include "Blowfish.h"
#include "cast.h"
#include "Cobra128.h"
#include "IDEA.h"
#include "MARS.h"
#include "pc1.h"
#include "RC6.h"
#include "Rijndael.h"
#include "Serpent.h"
#include "TMS.h"
#include "TripleDES.h"
#include "Twofish.h"


#include <stdlib.h>
#include <string.h>
#include <memory.h>

// fixed key length (i.n.) for extended selftest
#define FIXKEYLEN   16

// set this flag if CryptPak should only support non-commercial algorithms
//#define NON_COMMERCIAL



struct CIPHERCTX
{
  // function addresses
  Cipher_GetCipherInfo*         pGetCipherInfo;
  Cipher_SelfTest*              pSelfTest;
  Cipher_CreateWorkContext*     pCreateWorkContext;
  Cipher_ResetWorkContext*      pResetWorkContext;
  Cipher_DestroyWorkContext*    pDestroyWorkContext;
  Cipher_EncryptBuffer*         pEncryptBuffer;
  Cipher_DecryptBuffer*         pDecryptBuffer;

  //  cipher information
  CIPHERINFOBLOCK infoblock;

  // function reference for random number generation
  Cipher_RandomGenerator* pRandomGenerator;

  // data reference for the random generator
  const void* pRndGenData;

  // to check if the internal random generator is used
  BYTEBOOL blUseInternalRndGen;
};



struct CIPHERSESSION
{
  // crypt mode, see CIPHERSERVER_xxx constants
  WORD32 lCryptMode;

  // pointer to a cipher context
  PCIPHERCTX pCipherContext;

  // pointer to an algorithm's runtime memory area
  void* pWorkContext;
};



// lookup table to fetch the function addresses

typedef struct
{
  char* szName;
  Cipher_GetCipherInfo*       pGetCipherInfo;
  Cipher_SelfTest*            pSelfTest;
  Cipher_CreateWorkContext*   pCreateWorkContext;
  Cipher_ResetWorkContext*    pResetWorkContext;
  Cipher_DestroyWorkContext*  pDestroyWorkContext;
  Cipher_EncryptBuffer*       pEncryptBuffer;
  Cipher_DecryptBuffer*       pDecryptBuffer;
}
CIPHERLOOKUP;


#ifdef NON_COMMERCIAL
  #define NUM_OF_CIPHERS  9
#else
  #define NUM_OF_CIPHERS  12
#endif

CIPHERLOOKUP cipherFaces[NUM_OF_CIPHERS] = {

{       TMS_CIPHERNAME,       TMS_GetCipherInfo,       TMS_SelfTest,       TMS_CreateWorkContext,       TMS_ResetWorkContext,       TMS_DestroyWorkContext,       TMS_EncryptBuffer,       TMS_DecryptBuffer },
{  BLOWFISH_CIPHERNAME,  Blowfish_GetCipherInfo,  Blowfish_SelfTest,  Blowfish_CreateWorkContext,  Blowfish_ResetWorkContext,  Blowfish_DestroyWorkContext,  Blowfish_EncryptBuffer,  Blowfish_DecryptBuffer },
{      CAST_CIPHERNAME,      CAST_GetCipherInfo,      CAST_SelfTest,      CAST_CreateWorkContext,      CAST_ResetWorkContext,      CAST_DestroyWorkContext,      CAST_EncryptBuffer,      CAST_DecryptBuffer },
{  COBRA128_CIPHERNAME,  Cobra128_GetCipherInfo,  Cobra128_SelfTest,  Cobra128_CreateWorkContext,  Cobra128_ResetWorkContext,  Cobra128_DestroyWorkContext,  Cobra128_EncryptBuffer,  Cobra128_DecryptBuffer },
{       PC1_CIPHERNAME,       PC1_GetCipherInfo,       PC1_SelfTest,       PC1_CreateWorkContext,       PC1_ResetWorkContext,       PC1_DestroyWorkContext,       PC1_EncryptBuffer,       PC1_DecryptBuffer },
{   SERPENT_CIPHERNAME,   Serpent_GetCipherInfo,   Serpent_SelfTest,   Serpent_CreateWorkContext,   Serpent_ResetWorkContext,   Serpent_DestroyWorkContext,   Serpent_EncryptBuffer,   Serpent_DecryptBuffer },
{  RIJNDAEL_CIPHERNAME,  Rijndael_GetCipherInfo,  Rijndael_SelfTest,  Rijndael_CreateWorkContext,  Rijndael_ResetWorkContext,  Rijndael_DestroyWorkContext,  Rijndael_EncryptBuffer,  Rijndael_DecryptBuffer },
{ TRIPLEDES_CIPHERNAME, TripleDES_GetCipherInfo, TripleDES_SelfTest, TripleDES_CreateWorkContext, TripleDES_ResetWorkContext, TripleDES_DestroyWorkContext, TripleDES_EncryptBuffer, TripleDES_DecryptBuffer },
{   TWOFISH_CIPHERNAME,   Twofish_GetCipherInfo,   Twofish_SelfTest,   Twofish_CreateWorkContext,   Twofish_ResetWorkContext,   Twofish_DestroyWorkContext,   Twofish_EncryptBuffer,   Twofish_DecryptBuffer }

#ifndef NON_COMMERCIAL
,
{      IDEA_CIPHERNAME,      IDEA_GetCipherInfo,      IDEA_SelfTest,      IDEA_CreateWorkContext,      IDEA_ResetWorkContext,      IDEA_DestroyWorkContext,      IDEA_EncryptBuffer,      IDEA_DecryptBuffer },
{      MARS_CIPHERNAME,      Mars_GetCipherInfo,      Mars_SelfTest,      Mars_CreateWorkContext,      Mars_ResetWorkContext,      Mars_DestroyWorkContext,      Mars_EncryptBuffer,      Mars_DecryptBuffer },
{       RC6_CIPHERNAME,       RC6_GetCipherInfo,       RC6_SelfTest,       RC6_CreateWorkContext,       RC6_ResetWorkContext,       RC6_DestroyWorkContext,       RC6_EncryptBuffer,       RC6_DecryptBuffer }
#endif
};


// simple table storing the cipher names
char* cipherNames[NUM_OF_CIPHERS] =
{
        TMS_CIPHERNAME,
   BLOWFISH_CIPHERNAME,
       CAST_CIPHERNAME,
   COBRA128_CIPHERNAME,
        PC1_CIPHERNAME,
    SERPENT_CIPHERNAME,
   RIJNDAEL_CIPHERNAME,
  TRIPLEDES_CIPHERNAME,
    TWOFISH_CIPHERNAME

#ifndef NON_COMMERCIAL
,
       IDEA_CIPHERNAME,
       MARS_CIPHERNAME,
        RC6_CIPHERNAME
#endif
};


WORD32 CRYPTPAK_API CipherServer_GetCipherNames
  (char*** pszList)
{
  *pszList = cipherNames;
  return NUM_OF_CIPHERS;
}




WORD32 CRYPTPAK_API CipherServer_GetCipherInfo
  (const char* pCipherName,
   CIPHERINFOBLOCK* pInfoBlock)
{
    Cipher_GetCipherInfo* pGetCipherInfo = NULL;
    int nI;

    // get the selftest function address
    for (nI = 0; nI < NUM_OF_CIPHERS; nI++)
    {
      if (strcmp(cipherFaces[nI].szName, pCipherName) == 0)
      {
        pGetCipherInfo = cipherFaces[nI].pGetCipherInfo;
        break;
      }
    }

    if (pGetCipherInfo == NULL) {
      return CIPHERSERVER_ERROR_CIPHERNOTFOUND;
    }

    // prepare the information block
    pInfoBlock->lSizeOf = sizeof(CIPHERINFOBLOCK);

    // call the retrieved function to get the information block
    switch ((*pGetCipherInfo)(pInfoBlock))
    {
      case CIPHER_ERROR_NOERROR :
        return CIPHERSERVER_ERROR_NOERROR;
      case CIPHER_ERROR_INVALID :
        return CIPHERSERVER_ERROR_INVALIDCIPHER;
      default:
        // unknown return value
        return CIPHERSERVER_ERROR_ERROR;
    }
}



// internal random generator
void CRYPTPAK_CALLCONV _internalRandomGenerator
  (WORD8* pTargetBuffer,
   WORD32 lNumOfRandomBytes,
   const void* pData)
{
  // just map the call
  Yarrow_GetData((PYARROWCTX) pData, pTargetBuffer, lNumOfRandomBytes);
}



WORD32 CRYPTPAK_API CipherServer_Create
  (const char* pCipherName,
   PCIPHERCTX* pCtxPtr,
   Cipher_RandomGenerator* pRandGenFunc,
   const void* pRandGenData,
   const void* pRandSeed,
   WORD32 lRandSeedLen)
{
    PCIPHERCTX pNewCtx;
    WORD32 lRetCode;
    PYARROWCTX pYrwCtx;
    int nI;

    // create a new cipher context
    pNewCtx = (PCIPHERCTX) malloc(sizeof(CIPHERCTX));
    if (pNewCtx == NULL)
      return CIPHERSERVER_ERROR_OUTOFMEMORY;

    // get the function addresses
    nI = 0;
    while (nI < NUM_OF_CIPHERS)
    {
      if (strcmp(cipherFaces[nI].szName, pCipherName) == 0)
        break;
      nI++;
    }
    if (nI == NUM_OF_CIPHERS)
    {
      return CIPHERSERVER_ERROR_CIPHERNOTFOUND;
    }

    pNewCtx->pGetCipherInfo      = cipherFaces[nI].pGetCipherInfo;
    pNewCtx->pSelfTest           = cipherFaces[nI].pSelfTest;
    pNewCtx->pCreateWorkContext  = cipherFaces[nI].pCreateWorkContext;
    pNewCtx->pResetWorkContext   = cipherFaces[nI].pResetWorkContext;
    pNewCtx->pDestroyWorkContext = cipherFaces[nI].pDestroyWorkContext;
    pNewCtx->pEncryptBuffer      = cipherFaces[nI].pEncryptBuffer;
    pNewCtx->pDecryptBuffer      = cipherFaces[nI].pDecryptBuffer;


    // call the info function to get the information block
    pNewCtx->infoblock.lSizeOf = sizeof(CIPHERINFOBLOCK);
    switch ((*pNewCtx->pGetCipherInfo)(&pNewCtx->infoblock))
    {
      case CIPHER_ERROR_NOERROR :
        lRetCode = CIPHERSERVER_ERROR_NOERROR;
        break;
      case CIPHER_ERROR_INVALID :
        lRetCode = CIPHERSERVER_ERROR_INVALIDCIPHER;
        break;
      default:
        // unknown return value
        lRetCode = CIPHERSERVER_ERROR_ERROR;
    }
    if (lRetCode != CIPHERSERVER_ERROR_NOERROR)
    {
      free(pNewCtx);
      return lRetCode;
    }

    // must we create our own random generator?
    if (pRandGenFunc == CIPHER_NULL)
    {
      // create a random context
      pYrwCtx = Yarrow_Create(pRandSeed, lRandSeedLen);
      if (pYrwCtx == NULL)
      {
        free(pNewCtx);
        return CIPHERSERVER_ERROR_OUTOFMEMORY;
      }

      // store the context pointer
      pNewCtx->pRndGenData = pYrwCtx;

      // store the address of the internal random generator
      pNewCtx->pRandomGenerator = _internalRandomGenerator;

      // set the internal usage flag
      pNewCtx->blUseInternalRndGen = BOOL_TRUE;
    }
    else
    {
      // just link to the external random generator
      pNewCtx->pRandomGenerator = pRandGenFunc;
      pNewCtx->pRndGenData = pRandGenData;
      pNewCtx->blUseInternalRndGen = BOOL_FALSE;
    }

    // return the cipher handle
    *pCtxPtr = pNewCtx;

    // cipher successfully loaded
    return CIPHERSERVER_ERROR_NOERROR;
}



WORD32 CRYPTPAK_API CipherServer_Destroy
  (PCIPHERCTX pCtx)
{
    // release the internal rng, if necessary
    PYARROWCTX yctx;

    if (pCtx->blUseInternalRndGen)
    {
      yctx = (PYARROWCTX) pCtx->pRndGenData;

      if (yctx)
      {
        Yarrow_Destroy(yctx);
      }
    }

    // clear the context
    memset(pCtx, 0, sizeof(CIPHERCTX));

    // free the context and quit
    free(pCtx);
    return CIPHERSERVER_ERROR_NOERROR;
}




WORD32 CRYPTPAK_API CipherServer_ExecuteSelfTest
  (PCIPHERCTX pCtx,
   BYTEBOOL blExtendedTest)
{
    void* pTempWorkCtx;
    void* pInitData;
    WORD32 lResult;
    WORD32 lKeySize;
    WORD32 lI;
    WORD8* keybuf;
    WORD8* twoblocks;
    int nTestBlockSize;
    int nI;
    PCIPHERSESSION chandle;

    // create a temporary work context
    if (pCtx->infoblock.lContextSize)
    {
      pTempWorkCtx = malloc(pCtx->infoblock.lContextSize);
      if (pTempWorkCtx == NULL)
        return CIPHERSERVER_ERROR_OUTOFMEMORY;
    }
    else
    {
      pTempWorkCtx = NULL;
    }

    // execute the cipher selftest
    if ((*pCtx->pSelfTest)(pTempWorkCtx) == CIPHER_ERROR_INVALID)
    {
      // selftest failed
      free(pTempWorkCtx);
      return CIPHERSERVER_ERROR_INVALIDCIPHER;
    }

    // free the temporary work context
    free(pTempWorkCtx);

    // execute the extended test, i.n.
    if (blExtendedTest)
    {
      // encrypt two blocks using a simple key
      if (pCtx->infoblock.blOwnHasher)
        lKeySize = FIXKEYLEN;
      else
        lKeySize = pCtx->infoblock.lKeySize;

      if (lKeySize)
      {
        keybuf = (WORD8*) malloc(lKeySize);
        if (keybuf == NULL)
          return CIPHERSERVER_ERROR_OUTOFMEMORY;
      }
      else
      {
        keybuf = NULL;
      }

      for (lI = 0; lI < lKeySize; lI++)
        keybuf[lI] = (WORD8) (lI & 0x0ff);

      // allocate the two block buffer
      nTestBlockSize = (int)pCtx->infoblock.lBlockSize << 1;
      twoblocks = (WORD8*) malloc(nTestBlockSize);
      if (twoblocks == NULL)
      {
        free(keybuf);
        return CIPHERSERVER_ERROR_OUTOFMEMORY;
      }

      // we use this creation for checking the right decryption later
      for (nI = 0; nI < nTestBlockSize; nI++)
        twoblocks[nI] = (WORD8) (nI & 0x0ff);

      // allocate the init. data memory
      if (pCtx->infoblock.lInitDataSize)
      {
        pInitData = malloc(pCtx->infoblock.lInitDataSize);
        if (pInitData == NULL)
        {
          free(twoblocks);
          free(keybuf);
          return CIPHERSERVER_ERROR_OUTOFMEMORY;
        }
      }
      else
      {
        pInitData = NULL;
      }

      // open an encryption session
      lResult = CipherServer_OpenSession(CIPHERSERVER_MODE_ENCRYPT,
                                         keybuf,
                                         lKeySize,
                                         pCtx,
                                         pInitData,
                                         &chandle);

      if ((lResult != CIPHER_ERROR_NOERROR) && (lResult != CIPHER_ERROR_WEAKKEY))
      {
        free(pInitData);
        free(twoblocks);
        free(keybuf);
        return CIPHERSERVER_ERROR_INVALIDCIPHER;
      }

      // encrypt the blocks
      CipherServer_EncryptBlocks(chandle,
                                 twoblocks,
                                 twoblocks,
                                 2);

      // close the session
      lResult = CipherServer_CloseSession(chandle);
      if (lResult != CIPHER_ERROR_NOERROR)
      {
        free(pInitData);
        free(twoblocks);
        free(keybuf);
        return CIPHERSERVER_ERROR_INVALIDCIPHER;
      }

      // open a decryption session
      lResult = CipherServer_OpenSession(CIPHERSERVER_MODE_DECRYPT,
                                         keybuf,
                                         lKeySize,
                                         pCtx,
                                         pInitData,
                                         &chandle);
      if ((lResult != CIPHER_ERROR_NOERROR) && (lResult != CIPHER_ERROR_WEAKKEY))
      {
        free(pInitData);
        free(twoblocks);
        free(keybuf);
        return CIPHERSERVER_ERROR_INVALIDCIPHER;
      }

      // decrypt the blocks
      CipherServer_DecryptBlocks(chandle,
                                 twoblocks,
                                 twoblocks,
                                 2,
                                 CIPHER_NULL);

      // close the session
      lResult = CipherServer_CloseSession(chandle);
      if (lResult != CIPHER_ERROR_NOERROR)
      {
        free(pInitData);
        free(twoblocks);
        free(keybuf);
        return CIPHERSERVER_ERROR_INVALIDCIPHER;
      }

      // correct decryption?
      for (nI = 0; nI < nTestBlockSize; nI++)
      {
        if (twoblocks[nI] != (nI & 0x0ff))
        {
          free(pInitData);
          free(twoblocks);
          free(keybuf);
          return CIPHERSERVER_ERROR_INVALIDCIPHER;
        }
      }

      // free all memory
      free(pInitData);
      free(twoblocks);
      free(keybuf);
    }

    // quit with success
    return CIPHERSERVER_ERROR_NOERROR;
}




WORD32 CRYPTPAK_API CipherServer_GetInfoBlock
  (PCIPHERCTX pCtx,
   CIPHERINFOBLOCK* pInfoBlock)
{
    // call the retrieved function to get the information block
    pInfoBlock->lSizeOf = sizeof(CIPHERINFOBLOCK);
    switch ((*pCtx->pGetCipherInfo)(pInfoBlock))
    {
      case CIPHER_ERROR_NOERROR :
        return CIPHERSERVER_ERROR_NOERROR;
      case CIPHER_ERROR_INVALID :
        return CIPHERSERVER_ERROR_INVALIDCIPHER;
      default:
        // unknown return value
        return CIPHERSERVER_ERROR_ERROR;
    }
}





WORD32 CRYPTPAK_API CipherServer_OpenSession
  (WORD32 lMode,
   const WORD8* pKey,
   WORD32 lKeyLen,
   PCIPHERCTX pCtx,
   void* pInitData,
   PCIPHERSESSION* pSessionHandlePtr)
{
    PCIPHERSESSION pNewCryptSession;
    WORD32 lRetCode;

    // allocate memory for a new session handle and the work
    // context (the algorithm's runtime memory area) together
    pNewCryptSession = (PCIPHERSESSION) malloc(sizeof(CIPHERSESSION) + pCtx->infoblock.lContextSize);
    if (pNewCryptSession == NULL)
      return CIPHERSERVER_ERROR_OUTOFMEMORY;

    // calculate the pointer for the work context
    pNewCryptSession->pWorkContext = (WORD8*)pNewCryptSession + sizeof(CIPHERSESSION);

    memset(pNewCryptSession->pWorkContext,
           0,
           pCtx->infoblock.lContextSize);

    // call the cipher's CreateWorkContext() function
    switch ((*pCtx->pCreateWorkContext)(pNewCryptSession->pWorkContext,
                                        pKey,
                                        lKeyLen,
                                        lMode,
                                        pInitData,
                                        pCtx->pRandomGenerator,
                                        pCtx->pRndGenData))
    {
      case CIPHER_ERROR_NOERROR :
        lRetCode = CIPHERSERVER_ERROR_NOERROR;
        break;
      case CIPHER_ERROR_WEAKKEY :
        lRetCode = CIPHERSERVER_ERROR_WEAKKEY;
        break;
      default:
        // unknown return value (including case CIPHER_ERROR_KEYSETUPERROR)
        lRetCode = CIPHERSERVER_ERROR_ERROR;
    }
    if (lRetCode != CIPHERSERVER_ERROR_NOERROR)
    {
      free(pNewCryptSession);
      return lRetCode;
    }

    // copy the cipher handle to the session handle
    pNewCryptSession->pCipherContext = pCtx;

    // copy the crypt mode to the session handle
    pNewCryptSession->lCryptMode = lMode;

    // return the cryptsession handle
    *pSessionHandlePtr = pNewCryptSession;

    // success
    return CIPHERSERVER_ERROR_NOERROR;
}



void CRYPTPAK_API CipherServer_ResetSession
  (PCIPHERSESSION pSessionHandle,
   void* pInitData)
{
    // call the ciphers ResetWorkContext() function
    (*pSessionHandle->pCipherContext->pResetWorkContext)(pSessionHandle->pWorkContext,
                                                         pSessionHandle->lCryptMode,
                                                         pInitData,
                                                         pSessionHandle->pCipherContext->pRandomGenerator,
                                                         pSessionHandle->pCipherContext->pRndGenData);
}




WORD32 CRYPTPAK_API CipherServer_CloseSession
  (PCIPHERSESSION pSessionHandle)
{
    WORD32 lRetCode;

    // call the cipher's DestroyContext() function
    if ((*pSessionHandle->pCipherContext->pDestroyWorkContext)(pSessionHandle->pWorkContext) == CIPHER_ERROR_NOERROR)
      lRetCode = CIPHERSERVER_ERROR_NOERROR;
    else
      lRetCode = CIPHERSERVER_ERROR_ERROR;

    // even if a (fatal) error has occured we clear (all in one)
    // and free all the session memory to quit properly
    memset(pSessionHandle,
           0,
           sizeof(CIPHERSESSION) + pSessionHandle->pCipherContext->infoblock.lContextSize);
    free(pSessionHandle);

    // deliver the error code retrieved above
    return lRetCode;
}




void CRYPTPAK_API CipherServer_EncryptBlocks
  (PCIPHERSESSION pSessionHandle,
   const void* pSource,
   void* pTarget,
   WORD32 lNumOfBlocks)
{
    WORD32 lNumOfBytes;

    // calculate the number of bytes to encrypt
    lNumOfBytes = lNumOfBlocks * pSessionHandle->pCipherContext->infoblock.lBlockSize;

    // call the cipher's EncryptBuffer() function
    (*pSessionHandle->pCipherContext->pEncryptBuffer)(pSessionHandle->pWorkContext,
                                                      pSource,
                                                      pTarget,
                                                      lNumOfBytes);
}




void CRYPTPAK_API CipherServer_DecryptBlocks
  (PCIPHERSESSION pSessionHandle,
   const void* pSource,
   void* pTarget,
   WORD32 lNumOfBlocks,
   const void* pPreviousBlock)
{
    WORD32 lNumOfBytes;

    // calculate the number of bytes to encrypt
    lNumOfBytes = lNumOfBlocks * pSessionHandle->pCipherContext->infoblock.lBlockSize;

    // call the cipher's DecryptBuffer() function
    (*pSessionHandle->pCipherContext->pDecryptBuffer)(pSessionHandle->pWorkContext,
                                                      pSource,
                                                      pTarget,
                                                      lNumOfBytes,
                                                      pPreviousBlock);
}


void CRYPTPAK_API CipherServer_GetRandomData
  (PCIPHERCTX pCtx,
   void* pTarget,
   WORD32 lNumOfBytes)
{
  // just map the call
  (*pCtx->pRandomGenerator)((WORD8*)pTarget,
                            lNumOfBytes,
                            pCtx->pRndGenData);
}


void CRYPTPAK_API clear_tdes_cbciv(PCIPHERSESSION pSessionHandle)
{
  TRIPLEDESCTX* pTDESCtx = (TRIPLEDESCTX*) pSessionHandle->pWorkContext;

  pTDESCtx->lCBCLo = pTDESCtx->lCBCHi = 0;
}
