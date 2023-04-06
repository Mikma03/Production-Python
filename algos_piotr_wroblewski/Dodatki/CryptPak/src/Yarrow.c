

/*
  Yarrow random number generator, not that cool as the original one
  of Counterpane, but uses the recommended technique after all
  (FIXME: currently we expect a full functional and compatible CryptPak
          library, otherwise this module might get pretty instable!)
*/

#include <stdlib.h>
#include <memory.h>

#include "CryptPak.h"

#include <time.h>


// number of blocks output limit
#define BLOCK_NUMBER_LIMIT  100000


// number of iterations for every reseed
#define RESEED_LOOPS    800




typedef struct
{
  WORD64 qCounter;
  WORD8 tdesKey[TRIPLEDES_KEYSIZE];
}
STARTDATA;



void CRYPTPAK_CALLCONV _dummyRandomGenerator
  (WORD8* pTargetBuffer,
   WORD32 lNumOfRandomBytes,
   const void* pData) 
{
  memset(pTargetBuffer, 0, lNumOfRandomBytes);
}


PYARROWCTX CRYPTPAK_API Yarrow_Create
  (const void* pAddSeed, 
   WORD32 lAddSeedLen) 
{
    // create the context
    PYARROWCTX pCtx = (PYARROWCTX) malloc(sizeof(YARROWCTX));

    // and init. it
    if (0 == Yarrow_Initialize(pCtx, pAddSeed, lAddSeedLen))
    {
      free(pCtx);
      return NULL;
    }

    return pCtx;
}



int CRYPTPAK_API Yarrow_Initialize
  (PYARROWCTX pCtx,
   const void* pAddSeed, 
   WORD32 lAddSeedLen) 
{
    WORD32 lResult;

    STARTDATA sd;

    // (we just know the init. data size right now)
    WORD8 initData[TRIPLEDES_BLOCKSIZE];  

    time_t tm = time(NULL);

    // create a (of course very weak) key out of the current time we go above,
    // if there's additional seed we will pass it as salt (which is then
    // safer, dependent on the seed's quality, of course)
    Support_CrunchKey(&tm,
                      sizeof(tm),
                      pAddSeed,
                      lAddSeedLen,
                      &sd,
                      sizeof(sd),
                      CRUNCHKEY_METHOD_SHAEXTENDER,
                      NULL);

    // set up the counter
    pCtx->qCounter = sd.qCounter;

    // start the triple-DES engine
    
    lResult = TripleDES_CreateWorkContext(&pCtx->tctx,
                                          (WORD8*)&(sd.tdesKey),
                                          TRIPLEDES_KEYSIZE,
                                          CIPHER_MODE_ENCRYPT,
                                          &initData,
                                          _dummyRandomGenerator,
                                          NULL);
 
    if ((lResult != CIPHER_ERROR_NOERROR) &&
        (lResult != CIPHER_ERROR_WEAKKEY)) // FIXME: do weak keys matter?
    {
      return 0;
    }
 
    // burn startup key material
    memset(&sd, 0, sizeof(sd));

    // no blocks were put out until now
    pCtx->lBlocksOut = 0;

    pCtx->lBytesInBuf= 0;

    return 1;
}


void CRYPTPAK_API Yarrow_Destroy
  (PYARROWCTX pCtx) 
{
  // clean up
  if (pCtx)
  {
    TripleDES_DestroyWorkContext(&pCtx->tctx);

    memset(pCtx, 0, sizeof(YARROWCTX));
    free(pCtx);
  }
}


// internal routines...

void Yarrow_RefillBuf
  (PYARROWCTX pCtx)
{
  // change CBC triple-DES to ECB artifically
  pCtx->tctx.lCBCHi = 0;
  pCtx->tctx.lCBCLo = 0;

  // encrypt that counter, result is put into the buffer
  TripleDES_EncryptBuffer(&(pCtx->tctx),
                          &(pCtx->qCounter),
                          &(pCtx->rndDataBuf),
                          TRIPLEDES_BLOCKSIZE);

  // increase the counter
  pCtx->qCounter++;

  // one block delivered
  pCtx->lBlocksOut++;

  // buffer is full now
  pCtx->lBytesInBuf = TRIPLEDES_BLOCKSIZE;
}


void Yarrow_Reset
  (PYARROWCTX pCtx)
{
  WORD32 lCpy, lPos, lRest;
  WORD8 tdesKey[TRIPLEDES_KEYSIZE];
  WORD8 dumData[TRIPLEDES_BLOCKSIZE];  // (see above)

  // generator gate...

  // random output is used as the new key (we cannot use Yarrow_GetBytes() here, 
  // after all the fact that TRIPLEDES_KEYSIZE > TRIPLEDES_BLOCKSIZE makes things 
  // easier)

  memcpy(&tdesKey, 
         &(pCtx->rndDataBuf[TRIPLEDES_BLOCKSIZE - pCtx->lBytesInBuf]),
         pCtx->lBytesInBuf);  // (might be zero)

  lPos = pCtx->lBytesInBuf;
  lRest = TRIPLEDES_KEYSIZE - pCtx->lBytesInBuf;

  do
  {
    Yarrow_RefillBuf(pCtx);

    lCpy = (lRest > pCtx->lBytesInBuf) ? pCtx->lBytesInBuf : lRest;

    memcpy(&(tdesKey[lPos]),
           &(pCtx->rndDataBuf),
           lCpy);

    lPos += lCpy;
    lRest -= lCpy;
  }
  while (lRest);

  // (but we keep the last old random bytes)
  pCtx->lBytesInBuf -= lCpy;

  // we need a session reopening with the new key now

  TripleDES_DestroyWorkContext(&pCtx->tctx);

  TripleDES_CreateWorkContext(&pCtx->tctx,
                              (WORD8*)&(tdesKey),
                              sizeof(tdesKey),
                              CIPHER_MODE_ENCRYPT,
                              &dumData,
                              _dummyRandomGenerator,
                              NULL);

  memset(&tdesKey, 0, sizeof(tdesKey));

  // (FIXME: other operations necessary here? (nothing more in the CP paper)

  pCtx->lBlocksOut = 0;
}



// back to the API ...



void CRYPTPAK_API Yarrow_Reseed
  (PYARROWCTX pCtx, 
   const void* pSeed, 
   WORD32 lSeedLen) 
{
  WORD64 qZero;
  int nI;
  SHA1CTX hashCtx;
  TRIPLEDESCTX tmpCtx;
  WORD8 digest[SHA1_DIGESTSIZE];
  WORD8 tmpKey[TRIPLEDES_KEYSIZE];
  WORD8 dumData[TRIPLEDES_BLOCKSIZE]; // (see above again)

  SHA1_Initialize(&hashCtx);

  // hash down the seed first
  SHA1_Update(&hashCtx, 
              pSeed, 
              lSeedLen);
  SHA1_Final((WORD8*)&digest, 
             &hashCtx);

  // now iterate on this data by self hashing
  for (nI = 0; nI < RESEED_LOOPS; nI++)
  {
    SHA1_Reset(&hashCtx);
    SHA1_Update(&hashCtx, 
                &digest, 
                SHA1_DIGESTSIZE);
    SHA1_Final((WORD8*)&digest, 
               &hashCtx);
  }

  // create a triple-DES key out of the last generated digest
  Support_CrunchKey(&digest,
                    SHA1_DIGESTSIZE,
                    NULL,
                    0,
                    &tmpKey,
                    sizeof(tmpKey),
                    CRUNCHKEY_METHOD_SHAEXTENDER,
                    NULL);

  // encrypt an all zero string with this key and use it as the new counter
  // (it's really the first time that we're using parallel sessions with
  //  one cipher context)

  TripleDES_CreateWorkContext(&tmpCtx,
                              (WORD8*)&tmpKey,
                              sizeof(tmpKey),
                              CIPHER_MODE_ENCRYPT,
                              &dumData,
                              _dummyRandomGenerator,
                              NULL);

  // (ECB mode here, too)
  pCtx->tctx.lCBCLo = 0;
  pCtx->tctx.lCBCHi = 0;
  qZero = 0;


  TripleDES_EncryptBuffer(&tmpCtx,
                          &qZero,
                          &(pCtx->qCounter),
                          TRIPLEDES_BLOCKSIZE);

  TripleDES_DestroyWorkContext(&tmpCtx);

  // leave no data behind
  memset(digest, 0, sizeof(digest));
  memset(tmpKey, 0, sizeof(tmpKey));
  memset(dumData, 0, sizeof(dumData));
}


void CRYPTPAK_API Yarrow_GetData
  (PYARROWCTX pCtx, 
   void* pDataTarget, 
   WORD32 lNumOfBytes) 
{
  WORD32 lPos;
  WORD32 lToCopy;
  WORD8* pOut;

  // generate the random data now
  pOut = (WORD8*) pDataTarget;

  // enough bytes in the buffer to fullfill the request?
  if (pCtx->lBytesInBuf >= lNumOfBytes) 
  {
    memcpy(pDataTarget,
           &(pCtx->rndDataBuf[TRIPLEDES_BLOCKSIZE - pCtx->lBytesInBuf]),
           lNumOfBytes);

    pCtx->lBytesInBuf -= lNumOfBytes;

    return;
  }

  // no, so flush the buffer first
  lPos = 0;
  if (pCtx->lBytesInBuf > 0)
  {
    memcpy(&pOut[lPos],
           &(pCtx->rndDataBuf[TRIPLEDES_BLOCKSIZE - pCtx->lBytesInBuf]),
           lNumOfBytes);

    lNumOfBytes -= pCtx->lBytesInBuf;
    lPos += pCtx->lBytesInBuf;

    pCtx->lBytesInBuf = 0;
  }

  // fill the "rest"
  while (lNumOfBytes)
  {
    // need a reset?
    if (pCtx->lBlocksOut >= BLOCK_NUMBER_LIMIT) Yarrow_Reset(pCtx);
  
    Yarrow_RefillBuf(pCtx);

    lToCopy = (lNumOfBytes > TRIPLEDES_BLOCKSIZE) ? TRIPLEDES_BLOCKSIZE : lNumOfBytes;

    memcpy(&pOut[lPos],
           &(pCtx->rndDataBuf),
           lToCopy);

    pCtx->lBytesInBuf = TRIPLEDES_BLOCKSIZE - lToCopy;

    lNumOfBytes -= lToCopy;

    lPos += lToCopy;
  }
}
