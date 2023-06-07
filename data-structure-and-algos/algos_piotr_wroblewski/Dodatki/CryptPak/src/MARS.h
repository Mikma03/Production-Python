

#ifndef __MARS_H
#define __MARS_H

#ifdef __cplusplus
extern "C" {
#endif

#include "CipherDef.h"

#define MARS_CIPHERNAME   "Mars"



// function interface

WORD32 Mars_GetCipherInfo(CIPHERINFOBLOCK*);

WORD32 Mars_SelfTest (void*);

WORD32 Mars_CreateWorkContext(void*, const WORD8*, WORD32, WORD32, void*,
                              Cipher_RandomGenerator, const void*);

void Mars_ResetWorkContext(void*, WORD32, void*,
                           Cipher_RandomGenerator, const void*);

WORD32 Mars_DestroyWorkContext (void*);

void Mars_EncryptBuffer(void*, const void*, void*, WORD32);

void Mars_DecryptBuffer(void*, const void*, void*, WORD32, const void*);


#ifdef __cplusplus
}
#endif

#endif
