

#ifndef __BLOWFISH_H
#define __BLOWFISH_H

#ifdef __cplusplus
extern "C" {
#endif

#include "CipherDef.h"

// some constants...
#define BLOWFISH_KEYSIZE       56   // equals 448 bits
#define BLOWFISH_BLOCKSIZE      8    
#define PBOX_SIZE              18
#define SBOX_SIZE             256
#define BOXES_SIZE (PBOX_SIZE + 4 * SBOX_SIZE) 
#define BLOWFISH_CIPHERNAME   "Blowfish"

// function interface

WORD32 Blowfish_GetCipherInfo(CIPHERINFOBLOCK*);

WORD32 Blowfish_SelfTest (void*);

WORD32 Blowfish_CreateWorkContext(void*, const WORD8*, WORD32, WORD32, void*,
                                  Cipher_RandomGenerator, const void*);

void Blowfish_ResetWorkContext(void*, 
                               WORD32, 
                               void*,
                               Cipher_RandomGenerator, 
                               const void*);

WORD32 Blowfish_DestroyWorkContext (void*);

void Blowfish_EncryptBuffer(void*, const void*, void*, WORD32);

void Blowfish_DecryptBuffer(void*, const void*, void*, WORD32, const void*);


#ifdef __cplusplus
}
#endif

#endif
