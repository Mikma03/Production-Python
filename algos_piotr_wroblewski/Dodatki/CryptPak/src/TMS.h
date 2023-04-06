


#ifndef __TMS_H
#define __TMS_H

#ifdef __cplusplus
extern "C" {
#endif

#include "CipherDef.h"


// TMS "characteristics", simulates a stream cipher depending on a 16bit key
#define TMS_BLOCKSIZE   1
#define TMS_KEYSIZE     2
#define TMS_CIPHERNAME  "TMS"


WORD32 TMS_GetCipherInfo(CIPHERINFOBLOCK*);

WORD32 TMS_SelfTest(void*);

WORD32 TMS_CreateWorkContext(void*, const WORD8*, WORD32, WORD32, void*,
                             Cipher_RandomGenerator, const void*);

void TMS_ResetWorkContext(void*, WORD32, void*,
                          Cipher_RandomGenerator, const void*);

WORD32 TMS_DestroyWorkContext(void*);

void TMS_EncryptBuffer(void*, const void*, void*, WORD32);

void TMS_DecryptBuffer(void*, const void*, void*, WORD32, const void*);

#ifdef __cplusplus
}
#endif


#endif
