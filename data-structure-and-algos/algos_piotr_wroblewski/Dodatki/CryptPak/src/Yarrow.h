

#ifndef __YARROW_H
#define __YARROW_H

#include "cpconfig.h"
#include "BasicTypes.h"
#include "TripleDES.h"


#ifdef __cplusplus
extern "C" {
#endif


// context type for random data creation

typedef struct
{
  WORD64 qCounter;
  WORD8 rndDataBuf[TRIPLEDES_BLOCKSIZE];
  WORD32 lBytesInBuf;
  WORD32 lBlocksOut;
  TRIPLEDESCTX tctx;
}
YARROWCTX, *PYARROWCTX;


/*
 * sets up a new Yarrow context (seeded with the current time only!)
 * -> pointer to additional seed data (ignored if NULL)
 * -> number of additional seed bytes (ignored if pAddSeed equals NULL)
 * <- pointer to context
 */
PYARROWCTX CRYPTPAK_API
    Yarrow_Create (const void*, WORD32);


/*
 * sets up a Yarrow context statically
 * -> pointer to context
 * -> pointer to additional seed data (ignored if NULL)
 * -> number of additional seed bytes (ignored if pAddSeed equals NULL)
 * <- 1: success / 0: error
 */
int CRYPTPAK_API 
    Yarrow_Initialize (PYARROWCTX, const void*, WORD32);


/*
 * releases a Yarrow context
 * -> pointer to context to release
 */
void CRYPTPAK_API 
    Yarrow_Destroy (PYARROWCTX);


/*
 * adds seed to the random generator
 * -> pointer to context
 * -> pointer to the seed data
 * -> number of seed bytes
 */
void CRYPTPAK_API 
    Yarrow_Reseed (PYARROWCTX, const void*, WORD32);


/*
 * returns random bytes
 * -> pointer to context
 * -> pointer to target buffer
 * -> number of random bytes to deliver
 */
void CRYPTPAK_API 
    Yarrow_GetData (PYARROWCTX, void*, WORD32);


#ifdef __cplusplus
}
#endif


#endif
