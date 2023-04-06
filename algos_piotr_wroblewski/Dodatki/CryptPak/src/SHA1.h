


#ifndef __SHA1_H
#define __SHA1_H

#include "cpconfig.h"
#include "BasicTypes.h"


#ifdef __cplusplus
extern "C" {
#endif


// size of an SHA-1 digest
#define SHA1_DIGESTSIZE 20


// the SHS block size (in bytes)
#define SHA1_DATASIZE   64



// context for storing SHA info 

typedef struct
{
  // message digest
  WORD32 digest[5];

  // 64bit bit counter
  WORD32 lCountLo, lCountHi;

  // SHS data buffer
  WORD32 data[16];

  // SHS data buffer
  WORD8 dataBuffer[SHA1_DATASIZE];

  // whether final digest present
  BYTEBOOL blDone;
}
SHA1CTX, *PSHA1CTX; 



/*
 * sets up an SHA-1 context
 * <- pointer to SHA-1 context
 */
PSHA1CTX CRYPTPAK_API 
  SHA1_Create();


/*
 * sets up an SHA-1 context statically
 * -> pointer to SHA-1 context
 */
void CRYPTPAK_API 
  SHA1_Initialize(PSHA1CTX);


/*
 * resets an SHA-1 context
 * -> context to reset
 */
void CRYPTPAK_API 
    SHA1_Reset(PSHA1CTX pCtx);


/*
 * releases an SHA-1 context
 * -> pCtx pointer to SHA-1 context
 */
void CRYPTPAK_API 
    SHA1_Destroy(PSHA1CTX pCtx);


/*
 * scrambles a bunch of bytes to the digest
 * -> pCtx pointer to SHA-1 context
 * -> pData pointer to data to scramble
 * -> lNumOfBytes number of bytes to scramble
 */
void CRYPTPAK_API 
    SHA1_Update (PSHA1CTX, const void*, WORD32);


/*
 * finalize the scrambling, copies the digest
 * -> pDigest pointer to the digest storage
 * -> pCtx pointer to SHA-1 context
 */
void CRYPTPAK_API 
    SHA1_Final (WORD8*, PSHA1CTX pCtx);


/*
 * executes a selftest
 * <- BOOL_TRUE: selftest succeded / FALSE: selftest failed
 */
BYTEBOOL CRYPTPAK_API 
   SHA1_SelfTest();


#ifdef __cplusplus
}
#endif


#endif
