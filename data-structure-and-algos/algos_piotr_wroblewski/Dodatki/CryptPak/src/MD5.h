


#ifndef __MD5_H
#define __MD5_H

#include "cpconfig.h"
#include "BasicTypes.h"


#ifdef __cplusplus
extern "C" {
#endif

// size of an MD5 digest
#define MD5_DIGESTSIZE  16


// MD5 context

typedef struct
{
  WORD32 state[4];  // state (ABCD)
  WORD32 count[2];  // number of bits, modulo 2^64 (lsb first)
  WORD8 buffer[64]; // input buffer
}
MD5CTX, *PMD5CTX;



/*
 * initialization, begins an MD5 operation, writing a new context
 * <- pointer to new MD5 context
 */
PMD5CTX CRYPTPAK_API 
    MD5_Create ();


/*
 * same initialization, but statically
 * -> pointer to MD5 context
 */
void CRYPTPAK_API 
    MD5_Initialize (PMD5CTX);


/*
 * resets an MD5 context
 * -> context to rest
 */
void CRYPTPAK_API 
    MD5_Reset (PMD5CTX);


/*
 * releases an MD5 context
 * -> pointer to MD5 context to release
 */
void CRYPTPAK_API 
    MD5_Destroy (PMD5CTX);


/*
 * block update operation, continues an MD5 message-digest operation,
 * processing another message block, and updating the context
 * -> pointer to MD5 context
 * -> pointer to input buffer, which is treated as a byte buffer
 * -> number of bytes to scramble
 */
void CRYPTPAK_API 
    MD5_Update (PMD5CTX, const void*, WORD32);



/*
 * MD5 finalization, ends an MD5 message-digest operation,
 * writing the message digest and clearing the context
 * -> buffer where to copy the digest's bytes
 * -> pointer to MD5 context
 */
void CRYPTPAK_API 
    MD5_Final (WORD8[MD5_DIGESTSIZE], PMD5CTX);


/*
 * selftest
 * <- BOOL_TRUE: selftest succeded / BOOL_FALSE: error
 */
BYTEBOOL CRYPTPAK_API 
    MD5_SelfTest();


#ifdef __cplusplus
}
#endif


#endif
