



#ifndef __RANDOMPOOL_H
#define __RANDOMPOOL_H

#include "cpconfig.h"
#include "BasicTypes.h"
#include "SHA1.h"


#ifdef __cplusplus
extern "C" {
#endif


// context type for random data creation
typedef struct 
{
  // the hash context
  SHA1CTX hashCtx;

  // for holding the last digest, our random pool
  WORD8 pool[SHA1_DIGESTSIZE];

  // number of remaining bytes in the pool
  WORD32 lPoolSize;
}
RANDOMPOOLCTX, *PRANDOMPOOLCTX;



/*
 * sets up a new random pool context (init. seed is the systemn time)
 * -> pointer to additional seed data (ignored if NULL)
 * -> number of additional seed bytes (ignored if pAddSeed equals NULL)
 * -> number of additional seed bytes (ignored if pAddSeed equals NULL)
 * <- pointer to context
 */
PRANDOMPOOLCTX CRYPTPAK_API 
    RandomPool_Create (const void*, WORD32);


/*
 * same setup, but statically
 * -> pointer to additional seed data (ignored if NULL)
 * -> number of additional seed bytes (ignored if pAddSeed equals NULL)
 * -> number of additional seed bytes (ignored if pAddSeed equals NULL)
 * <- pointer to context
 */
void CRYPTPAK_API 
    RandomPool_Initialize (PRANDOMPOOLCTX, const void*, WORD32);



/*
 * releases a random pool context
 * -> pointer to context to release
 */
void CRYPTPAK_API 
    RandomPool_Destroy (PRANDOMPOOLCTX);


/*
 * adds seed to the random generator
 * -> pointer to context
 * -> pointer to the seed data
 * -> number of seed bytes
 */
void CRYPTPAK_API 
    RandomPool_Reseed (PRANDOMPOOLCTX, const void*, WORD32);


/*
 * returns random bytes
 * -> pointer to context
 * -> pointer to target buffer
 * -> number of random bytes to deliver
 */
void CRYPTPAK_API 
    RandomPool_GetData( PRANDOMPOOLCTX, void*, WORD32);


#ifdef __cplusplus
}
#endif


#endif
