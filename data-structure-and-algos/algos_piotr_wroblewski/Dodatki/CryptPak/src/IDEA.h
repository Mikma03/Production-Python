

#ifndef __IDEA_H
#define __IDEA_H


#ifdef __cplusplus
extern "C" {
#endif

#include "CipherDef.h"

// some constants...
#define IDEA_KEYSIZE        16
#define IDEA_BLOCKSIZE      8    
#define IDEA_ROUNDS         8
#define IDEA_KEYLEN         (6 * IDEA_ROUNDS + 4)
#define IDEA_CIPHERNAME     "IDEA"

// function interface

WORD32 IDEA_GetCipherInfo(CIPHERINFOBLOCK*);

WORD32 IDEA_SelfTest (void*);

WORD32 IDEA_CreateWorkContext(void*, const WORD8*, WORD32, WORD32, void*,
                              Cipher_RandomGenerator, const void*);

void IDEA_ResetWorkContext(void*, WORD32, void*,
                           Cipher_RandomGenerator, const void*);

WORD32 IDEA_DestroyWorkContext (void*);

void IDEA_EncryptBuffer(void*, const void*, void*, WORD32);

void IDEA_DecryptBuffer(void*, const void*, void*, WORD32, const void*);


#ifdef __cplusplus
}
#endif

#endif
