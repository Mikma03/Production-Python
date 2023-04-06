
#ifndef _CAST_H
#define _CAST_H


#ifdef __cplusplus
extern "C" {
#endif

#include "CipherDef.h"


// some constants...
#define CAST_CIPHERNAME   "CAST"


// function interface

WORD32 CAST_GetCipherInfo(CIPHERINFOBLOCK*);

WORD32 CAST_SelfTest (void*);

WORD32 CAST_CreateWorkContext(void*, const WORD8*, WORD32, WORD32, void*,
                              Cipher_RandomGenerator, const void*);

void CAST_ResetWorkContext(void*, WORD32, void*,
                           Cipher_RandomGenerator, const void*);

WORD32 CAST_DestroyWorkContext (void*);

void CAST_EncryptBuffer(void*, const void*, void*, WORD32);

void CAST_DecryptBuffer(void*, const void*, void*, WORD32, const void*);


#ifdef __cplusplus
}
#endif



#endif       /* ifndef _CAST_H_ */
