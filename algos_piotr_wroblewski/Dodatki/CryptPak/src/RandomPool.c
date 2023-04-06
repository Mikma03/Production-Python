

#include "cpkernel.h"
#include "RandomPool.h"

#include <time.h>
#include <stdlib.h>
#include <memory.h>


// we use SHA-1 for creating random numbers
#include "SHA1.h"


// this constant sets the number of bytes used
// from an SHA-1 hash as random data
#define HASHBYTES_TO_USE   10




PRANDOMPOOLCTX CRYPTPAK_API RandomPool_Create
  (const void* pAddSeed, 
   WORD32 lAddSeedLen) 
{
    // create the context
    PRANDOMPOOLCTX pCtx = (PRANDOMPOOLCTX) malloc(sizeof(RANDOMPOOLCTX));

    // and initalize
    RandomPool_Initialize(pCtx, pAddSeed, lAddSeedLen);

    return pCtx;
}



void CRYPTPAK_API RandomPool_Initialize
  (PRANDOMPOOLCTX pCtx,
   const void* pAddSeed, 
   WORD32 lAddSeedLen) 
{
    time_t tm;

    // create a new SHA-1 context
    SHA1_Initialize(&pCtx->hashCtx);

    // now init. with the current time
    tm = time(NULL);
    SHA1_Update(&pCtx->hashCtx, &tm, sizeof(tm));

    // add the additional seed data, if necessary
    if (pAddSeed) SHA1_Update(&pCtx->hashCtx, pAddSeed, lAddSeedLen);

    // finish and copy the digest to the random pool
    SHA1_Final(pCtx->pool, &pCtx->hashCtx);
    memset(&pCtx->hashCtx, 0, SHA1_DIGESTSIZE);

    // the pool is filled now
    pCtx->lPoolSize = HASHBYTES_TO_USE;
}



void CRYPTPAK_API RandomPool_Destroy
  (PRANDOMPOOLCTX pCtx) 
{
  memset(pCtx, 0, sizeof(RANDOMPOOLCTX));
  free(pCtx);
}


void CRYPTPAK_API RandomPool_Reseed
  (PRANDOMPOOLCTX pCtx, 
   const void* pSeed, 
   WORD32 lSeedLen) 
{
    // reset the hash context
    SHA1_Reset(&pCtx->hashCtx);

    // hash the current buffer content first
    SHA1_Update(&pCtx->hashCtx, pCtx->pool, SHA1_DIGESTSIZE);

    // add the seed data
    SHA1_Update(&pCtx->hashCtx, pSeed, lSeedLen);

    // finish and copy the digest to the random pool
    SHA1_Final(pCtx->pool, &pCtx->hashCtx);
    memset(&pCtx->hashCtx, 0, SHA1_DIGESTSIZE);

    // the pool is filled now
    pCtx->lPoolSize = HASHBYTES_TO_USE;

}


void CRYPTPAK_API RandomPool_GetData
  (PRANDOMPOOLCTX pCtx, 
   void* pDataTarget, 
   WORD32 lNumOfBytes) 
{
    WORD8* pTarget = (WORD8*) pDataTarget;
    WORD32 lOutPos = 0;

    // loop until all random data has been put out
    while (lNumOfBytes) 
    {
      // do we need a refill?
      if (lNumOfBytes > pCtx->lPoolSize) 
      {
        // yes -> empty the pool completely
        memcpy(&pTarget[lOutPos], 
               &pCtx->pool[HASHBYTES_TO_USE - pCtx->lPoolSize], 
               pCtx->lPoolSize);
        lOutPos += pCtx->lPoolSize;
        lNumOfBytes -= pCtx->lPoolSize;

        // rehash the complete digest
        SHA1_Reset(&pCtx->hashCtx);
        SHA1_Update(&pCtx->hashCtx, pCtx->pool, SHA1_DIGESTSIZE);
        SHA1_Final(pCtx->pool, &pCtx->hashCtx);

        // the pool is filled again now
        pCtx->lPoolSize = HASHBYTES_TO_USE;
      }
      else 
      {
        // no -> just copy the random data
        memcpy(&pTarget[lOutPos], 
               &pCtx->pool[HASHBYTES_TO_USE - pCtx->lPoolSize], 
               lNumOfBytes);
        pCtx->lPoolSize -= lNumOfBytes;
        lNumOfBytes = 0;
      }
    }
}

