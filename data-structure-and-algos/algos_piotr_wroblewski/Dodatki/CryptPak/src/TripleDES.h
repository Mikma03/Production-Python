



#ifndef __TRIPLEDES_H
#define __TRIPLEDES_H

#ifdef __cplusplus
extern "C" {
#endif

#include "CipherDef.h"


// some constants...
#define TRIPLEDES_KEYSIZE      21   // 3 * (8 - 1)
#define TRIPLEDES_BLOCKSIZE     8    
#define TRIPLEDES_CIPHERNAME    "triple-DES"



// triple-DES context
typedef struct {

  // key context #1 (1st encryption)
  WORD32 k1[32];
  // key context #2 (decryption)
  WORD32 k2[32];
  // key context #3 (2nd encryption)
  WORD32 k3[32];

  // the CBC IV
  WORD32 lCBCLo;
  WORD32 lCBCHi;
} 
TRIPLEDESCTX;


// function interface

WORD32 TripleDES_GetCipherInfo(CIPHERINFOBLOCK*);

WORD32 TripleDES_SelfTest (void*);

WORD32 TripleDES_CreateWorkContext(void*, const WORD8*, WORD32, WORD32, void*,
                                   Cipher_RandomGenerator, const void*);

void TripleDES_ResetWorkContext(void*, WORD32, void*,
                                Cipher_RandomGenerator, const void*);

WORD32 TripleDES_DestroyWorkContext (void*);

void TripleDES_EncryptBuffer(void*, const void*, void*, WORD32);

void TripleDES_DecryptBuffer(void*, const void*, void*, WORD32, const void*);


#ifdef __cplusplus
}
#endif


#endif











