

#ifndef __PC1_H
#define __PC1_H


#ifdef __cplusplus
extern "C" {
#endif


#include "CipherDef.h"


// PC1 characteristics
#define PC1_BLOCKSIZE   1
#define PC1_KEYSIZE     20
#define PC1_CIPHERNAME  "PC1"


WORD32 PC1_GetCipherInfo(CIPHERINFOBLOCK*);

WORD32 PC1_SelfTest (void*);

WORD32 PC1_CreateWorkContext(void*, const WORD8*, WORD32, WORD32, void*,
                             Cipher_RandomGenerator, const void*);

void  PC1_ResetWorkContext(void*, WORD32, void*,
                           Cipher_RandomGenerator, const void*);

WORD32 PC1_DestroyWorkContext (void*);

void PC1_EncryptBuffer(void*, const void*, void*, WORD32);

void PC1_DecryptBuffer(void*, const void*, void*, WORD32, const void*);


#ifdef __cplusplus
}
#endif


#endif
