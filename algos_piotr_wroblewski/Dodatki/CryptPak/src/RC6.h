#ifndef RC6H
#define RC6H

#ifdef __cplusplus
extern "C" {
#endif

#include "CipherDef.h"

#define RC6_KEYSIZE    32
#define RC6_BLOCKSIZE  16
#define RC6_CIPHERNAME "RC6"

WORD32 RC6_GetCipherInfo(CIPHERINFOBLOCK*);

WORD32 RC6_SelfTest(void*);

WORD32 RC6_CreateWorkContext(void*,
                             const WORD8*,
                             WORD32,
                             WORD32,
                             void*,
                             Cipher_RandomGenerator,
                             const void*);

void RC6_ResetWorkContext(void*,
                          WORD32,
                          void*,
                          Cipher_RandomGenerator,
                          const void*);

WORD32 RC6_DestroyWorkContext(void*);

void RC6_EncryptBuffer(void*,
                       const void*,
                       void*,
                       WORD32);

void RC6_DecryptBuffer(void*,
                       const void*,
                       void*,
                       WORD32,
                       const void*);


#ifdef __cplusplus
}
#endif


#endif

