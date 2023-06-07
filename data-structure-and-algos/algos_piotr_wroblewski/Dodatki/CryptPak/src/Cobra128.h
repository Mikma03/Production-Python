


#ifndef __COBRA128_H
#define __COBRA128_H


#ifdef __cplusplus
extern "C" {
#endif

#include "CipherDef.h"


// some characteristics 
#define COBRA128_BLOCKSIZE  16
#define COBRA128_KEYSIZE    72
#define COBRA128_CIPHERNAME "Cobra128"



// function interface

WORD32 Cobra128_GetCipherInfo(CIPHERINFOBLOCK*);

WORD32 Cobra128_SelfTest(void*);

WORD32 Cobra128_CreateWorkContext(void*, const WORD8*, WORD32, WORD32, void*,
                                  Cipher_RandomGenerator, const void*);

void Cobra128_ResetWorkContext(void*, WORD32, void*,
                               Cipher_RandomGenerator, const void*);

WORD32 Cobra128_DestroyWorkContext(void*);

void Cobra128_EncryptBuffer(void*, const void*, void*, WORD32);

void Cobra128_DecryptBuffer(void*, const void*, void*, WORD32, const void*);


#ifdef __cplusplus
}
#endif


#endif
