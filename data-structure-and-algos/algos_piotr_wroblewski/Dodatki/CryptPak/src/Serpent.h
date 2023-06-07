#ifndef __SERPENT_H
#define __SERPENT_H

#ifdef __cplusplus
extern "C" {
#endif

#include "CipherDef.h"

#define SERPENT_KEYSIZE    32
#define SERPENT_BLOCKSIZE  16
#define SERPENT_CIPHERNAME "Serpent"

WORD32 Serpent_GetCipherInfo(CIPHERINFOBLOCK*);

WORD32 Serpent_SelfTest(void*);

WORD32 Serpent_CreateWorkContext(void*,
                                 const WORD8*,
                                 WORD32,
                                 WORD32,
                                 void*,
                                 Cipher_RandomGenerator,
                                 const void*);

void Serpent_ResetWorkContext(void*,
                              WORD32,
                              void*,
                              Cipher_RandomGenerator,
                              const void*);

WORD32 Serpent_DestroyWorkContext(void*);

void Serpent_EncryptBuffer(void*,
                           const void*,
                           void*,
                           WORD32);

void Serpent_DecryptBuffer(void*,
                           const void*,
                           void*,
                           WORD32,
                           const void*);

#ifdef __cplusplus
}
#endif

#endif
