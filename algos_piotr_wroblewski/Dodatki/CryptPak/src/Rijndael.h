
#ifndef __RIJNDAEL_H
#define __RIJNDAEL_H

#ifdef __cplusplus
extern "C" {
#endif

#include "CipherDef.h"

#define RIJNDAEL_KEYSIZE    32
#define RIJNDAEL_BLOCKSIZE  16
#define RIJNDAEL_CIPHERNAME "Rijndael"

WORD32 Rijndael_GetCipherInfo(CIPHERINFOBLOCK*);

WORD32 Rijndael_SelfTest(void*);

WORD32 Rijndael_CreateWorkContext(void*,
                                  const WORD8*,
                                  WORD32,
                                  WORD32,
                                  void*,
                                  Cipher_RandomGenerator,
                                  const void*);

void Rijndael_ResetWorkContext(void*,
                               WORD32,
                               void*,
                               Cipher_RandomGenerator,
                               const void*);

WORD32 Rijndael_DestroyWorkContext(void*);

void Rijndael_EncryptBuffer(void*,
                            const void*,
                            void*,
                            WORD32);

void Rijndael_DecryptBuffer(void*,
                            const void*,
                            void*,
                            WORD32,
                            const void*);


#ifdef __cplusplus
}
#endif

#endif
