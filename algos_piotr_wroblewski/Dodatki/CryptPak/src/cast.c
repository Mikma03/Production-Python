/*
 *
 * CAST-128 (also known as CAST5)
 * implementing the CAST-128 algorithm in CBC mode
 *
 * Written by Walter Dvorak <e9226745@student.tuwien.ac.at>
 *
 * For details in the CAST Encryption Algorithm please refer:
 * [1] C. Adams, "Constructing Symmetric Ciphers Using the CAST
 *                Design Procedure", in
 *     Selected Areas in Cryptography, Kluwer Academic Publishers,
 *     1997, pp. 71-104.
 *
 * This work based in parts on a cast-128 implementation
 *   for OpenBSD from Steve Reid <sreid@sea-to-sky.net>
 *
 * modified to fit into CryptPak by Markus Hahn <markus_hahn@gmx.net>
 * (on 12 April 2000)
 *
 * source code reformatted by Markus Hahn <markus_hahn@gmx.net> (00/08/04)
 * const modifiers added by Markus Hahn <markus_hahn@gmx.net> (00/09/29)
 * uneffective code removed by Markus Hahn <markus_hahn@gmx.net> (01/07/29)
 *
 * This program is Public Domain
 *
 * Some notes:
 *  1. CAST 16-rounds/128bit key only implementation. No support
 *     for 12-rounds/ 80bit key version.
 *  2. In _DEBUG compiled version, the selftest is a full
 *     maintenance test, specifed in appendix C in [1]
 *
 * Date: 26.9.1998
 *
 */

#include "cast.h"

#undef _DEBUG

/*
 * S-Boxes for CAST-128
 */
#include "cast_boxes.h"

/*
 * CAST5 work context
 */
typedef struct 
{
   WORD32 xkey[32];                     /* Key after expansion */
   WORD32 lCBCLo;                       /* CBC IV */
   WORD32 lCBCHi;
} 
CASTCTX;



/*
 * Macros to access 8-bit bytes out of a 32-bit word
 */
#define U8a(x) ( (WORD8)  (x>>24)      )
#define U8b(x) ( (WORD8) ((x>>16) &255))
#define U8c(x) ( (WORD8) ((x>>8)  &255))
#define U8d(x) ( (WORD8) ((x)     &255))

/*
 * Circular left shift
 */
#define ROL(x, n) ( ((x)<<(n)) | ((x)>>(32-(n))) )

/*
 * CAST-128 uses three different round functions
 */
#define F1(l, r, i) \
    t = ROL(key->xkey[i] + r, key->xkey[i+16]); \
    l ^= ((cast_sbox1[U8a(t)] ^ cast_sbox2[U8b(t)]) - \
     cast_sbox3[U8c(t)]) + cast_sbox4[U8d(t)];

#define F2(l, r, i) \
    t = ROL(key->xkey[i] ^ r, key->xkey[i+16]); \
    l ^= ((cast_sbox1[U8a(t)] - cast_sbox2[U8b(t)]) + \
     cast_sbox3[U8c(t)]) ^ cast_sbox4[U8d(t)];

#define F3(l, r, i) \
    t = ROL(key->xkey[i] - r, key->xkey[i+16]); \
    l ^= ((cast_sbox1[U8a(t)] + cast_sbox2[U8b(t)]) ^ \
     cast_sbox3[U8c(t)]) - cast_sbox4[U8d(t)];


/*
 * CAST Encryption Function
 */
void _cast_encrypt
  (CASTCTX* key, 
   WORD8* inblock, 
   WORD8* outblock)
{
   register WORD32 t, l, r;

    /* Get inblock into l,r */
   l = ((WORD32)inblock[0] << 24) | ((WORD32)inblock[1] << 16) |
       ((WORD32)inblock[2] <<  8) |  (WORD32)inblock[3];
   r = ((WORD32)inblock[4] << 24) | ((WORD32)inblock[5] << 16) |
       ((WORD32)inblock[6] <<  8) |  (WORD32)inblock[7];

   /* unrolled encryption loop */
    F1(l, r,  0);
    F2(r, l,  1);
    F3(l, r,  2);
    F1(r, l,  3);
    F2(l, r,  4);
    F3(r, l,  5);
    F1(l, r,  6);
    F2(r, l,  7);
    F3(l, r,  8);
    F1(r, l,  9);
    F2(l, r, 10);
    F3(r, l, 11);
    F1(l, r, 12);
    F2(r, l, 13);
    F3(l, r, 14);
    F1(r, l, 15);

   /* Put l,r into outblock */
    outblock[0] = U8a(r);
    outblock[1] = U8b(r);
    outblock[2] = U8c(r);
    outblock[3] = U8d(r);
    outblock[4] = U8a(l);
    outblock[5] = U8b(l);
    outblock[6] = U8c(l);
    outblock[7] = U8d(l);
}


/*
 * Decryption Function
 */
void _cast_decrypt
  (CASTCTX* key, 
   WORD8* inblock, 
   WORD8* outblock)
{
register WORD32 t, l, r;

    /* Get inblock into l,r */
   r = ((WORD32)inblock[0] << 24) | ((WORD32)inblock[1] << 16) |
    ((WORD32)inblock[2] << 8) | (WORD32)inblock[3];
   l = ((WORD32)inblock[4] << 24) | ((WORD32)inblock[5] << 16) |
    ((WORD32)inblock[6] << 8) | (WORD32)inblock[7];

    F1(r, l, 15);
    F3(l, r, 14);
    F2(r, l, 13);
    F1(l, r, 12);
    F3(r, l, 11);
    F2(l, r, 10);
    F1(r, l,  9);
    F3(l, r,  8);
    F2(r, l,  7);
    F1(l, r,  6);
    F3(r, l,  5);
    F2(l, r,  4);
    F1(r, l,  3);
    F3(l, r,  2);
    F2(r, l,  1);
    F1(l, r,  0);

   /* Put l,r into outblock */
    outblock[0] = U8a(l);
    outblock[1] = U8b(l);
    outblock[2] = U8c(l);
    outblock[3] = U8d(l);
    outblock[4] = U8a(r);
    outblock[5] = U8b(r);
    outblock[6] = U8c(r);
   outblock[7] = U8d(r);
}


/*
 * Key Schedule
 */
void _cast_setkey
  (CASTCTX* key, 
   WORD8* rawkey, 
   WORD32 keybytes)
{
    WORD32 t[4], z[4], x[4];
    unsigned int i;

   /* Copy key to workspace */
    for (i = 0; i < 4; i++) 
    {
        x[i] = 0;
      if ((i*4+0) < keybytes) x[i] = (WORD32)rawkey[i*4+0] << 24;
      if ((i*4+1) < keybytes) x[i] |= (WORD32)rawkey[i*4+1] << 16;
      if ((i*4+2) < keybytes) x[i] |= (WORD32)rawkey[i*4+2] << 8;
      if ((i*4+3) < keybytes) x[i] |= (WORD32)rawkey[i*4+3];
    }
    /* Generate 32 subkeys, four at a time */
    for (i = 0; i < 32; i+=4) 
    {
        switch (i & 4) 
        {
         case 0:
            t[0] = z[0] = x[0] ^ cast_sbox5[U8b(x[3])] ^
             cast_sbox6[U8d(x[3])] ^ cast_sbox7[U8a(x[3])] ^
             cast_sbox8[U8c(x[3])] ^ cast_sbox7[U8a(x[2])];
            t[1] = z[1] = x[2] ^ cast_sbox5[U8a(z[0])] ^
             cast_sbox6[U8c(z[0])] ^ cast_sbox7[U8b(z[0])] ^
             cast_sbox8[U8d(z[0])] ^ cast_sbox8[U8c(x[2])];
            t[2] = z[2] = x[3] ^ cast_sbox5[U8d(z[1])] ^
             cast_sbox6[U8c(z[1])] ^ cast_sbox7[U8b(z[1])] ^
             cast_sbox8[U8a(z[1])] ^ cast_sbox5[U8b(x[2])];
            t[3] = z[3] = x[1] ^ cast_sbox5[U8c(z[2])] ^
             cast_sbox6[U8b(z[2])] ^ cast_sbox7[U8d(z[2])] ^
             cast_sbox8[U8a(z[2])] ^ cast_sbox6[U8d(x[2])];
            break;
         case 4:
            t[0] = x[0] = z[2] ^ cast_sbox5[U8b(z[1])] ^
             cast_sbox6[U8d(z[1])] ^ cast_sbox7[U8a(z[1])] ^
             cast_sbox8[U8c(z[1])] ^ cast_sbox7[U8a(z[0])];
            t[1] = x[1] = z[0] ^ cast_sbox5[U8a(x[0])] ^
             cast_sbox6[U8c(x[0])] ^ cast_sbox7[U8b(x[0])] ^
             cast_sbox8[U8d(x[0])] ^ cast_sbox8[U8c(z[0])];
            t[2] = x[2] = z[1] ^ cast_sbox5[U8d(x[1])] ^
             cast_sbox6[U8c(x[1])] ^ cast_sbox7[U8b(x[1])] ^
             cast_sbox8[U8a(x[1])] ^ cast_sbox5[U8b(z[0])];
            t[3] = x[3] = z[3] ^ cast_sbox5[U8c(x[2])] ^
             cast_sbox6[U8b(x[2])] ^ cast_sbox7[U8d(x[2])] ^
             cast_sbox8[U8a(x[2])] ^ cast_sbox6[U8d(z[0])];
            break;
        }
        switch (i & 12) 
        {
         case 0:
         case 12:
            key->xkey[i+0] = cast_sbox5[U8a(t[2])] ^ cast_sbox6[U8b(t[2])] ^
             cast_sbox7[U8d(t[1])] ^ cast_sbox8[U8c(t[1])];
            key->xkey[i+1] = cast_sbox5[U8c(t[2])] ^ cast_sbox6[U8d(t[2])] ^
             cast_sbox7[U8b(t[1])] ^ cast_sbox8[U8a(t[1])];
            key->xkey[i+2] = cast_sbox5[U8a(t[3])] ^ cast_sbox6[U8b(t[3])] ^
             cast_sbox7[U8d(t[0])] ^ cast_sbox8[U8c(t[0])];
            key->xkey[i+3] = cast_sbox5[U8c(t[3])] ^ cast_sbox6[U8d(t[3])] ^
             cast_sbox7[U8b(t[0])] ^ cast_sbox8[U8a(t[0])];
            break;
         case 4:
         case 8:
            key->xkey[i+0] = cast_sbox5[U8d(t[0])] ^ cast_sbox6[U8c(t[0])] ^
             cast_sbox7[U8a(t[3])] ^ cast_sbox8[U8b(t[3])];
            key->xkey[i+1] = cast_sbox5[U8b(t[0])] ^ cast_sbox6[U8a(t[0])] ^
             cast_sbox7[U8c(t[3])] ^ cast_sbox8[U8d(t[3])];
            key->xkey[i+2] = cast_sbox5[U8d(t[1])] ^ cast_sbox6[U8c(t[1])] ^
             cast_sbox7[U8a(t[2])] ^ cast_sbox8[U8b(t[2])];
            key->xkey[i+3] = cast_sbox5[U8b(t[1])] ^ cast_sbox6[U8a(t[1])] ^
             cast_sbox7[U8c(t[2])] ^ cast_sbox8[U8d(t[2])];
            break;
        }
        switch (i & 12) 
        {
         case 0:
            key->xkey[i+0] ^= cast_sbox5[U8c(z[0])];
            key->xkey[i+1] ^= cast_sbox6[U8c(z[1])];
            key->xkey[i+2] ^= cast_sbox7[U8b(z[2])];
            key->xkey[i+3] ^= cast_sbox8[U8a(z[3])];
            break;
         case 4:
            key->xkey[i+0] ^= cast_sbox5[U8a(x[2])];
            key->xkey[i+1] ^= cast_sbox6[U8b(x[3])];
            key->xkey[i+2] ^= cast_sbox7[U8d(x[0])];
            key->xkey[i+3] ^= cast_sbox8[U8d(x[1])];
            break;
         case 8:
            key->xkey[i+0] ^= cast_sbox5[U8b(z[2])];
            key->xkey[i+1] ^= cast_sbox6[U8a(z[3])];
            key->xkey[i+2] ^= cast_sbox7[U8c(z[0])];
            key->xkey[i+3] ^= cast_sbox8[U8c(z[1])];
            break;
         case 12:
            key->xkey[i+0] ^= cast_sbox5[U8d(x[0])];
            key->xkey[i+1] ^= cast_sbox6[U8d(x[1])];
            key->xkey[i+2] ^= cast_sbox7[U8a(x[2])];
            key->xkey[i+3] ^= cast_sbox8[U8b(x[3])];
            break;
        }
        if (i >= 16) 
        {
            key->xkey[i+0] &= 31;
            key->xkey[i+1] &= 31;
            key->xkey[i+2] &= 31;
            key->xkey[i+3] &= 31;
        }
    }
    /* Wipe clean */
    for (i = 0; i < 4; i++) 
    {
        t[i] = x[i] = z[i] = 0;
    }
}

/*
 * GetDriver Info
 */
WORD32 CAST_GetCipherInfo
  (CIPHERINFOBLOCK* pInfo) 
{
  WORD32 lI;
  WORD8* pSrc;
  WORD8* pDst;
  CIPHERINFOBLOCK tempinfo;

  // prepare the information context
  tempinfo.lSizeOf = pInfo->lSizeOf;
  tempinfo.lBlockSize = 8;
  tempinfo.lKeySize = 16; 
  tempinfo.blOwnHasher = BOOL_FALSE;
  tempinfo.lInitDataSize = 8;
  tempinfo.lContextSize = sizeof(CASTCTX);
  tempinfo.bCipherIs = CIPHER_IS_BLOCKLINK;

  // copy as many bytes of the information block as possible
  pSrc = (WORD8*) &tempinfo;
  pDst = (WORD8*) pInfo;
  for (lI = 0; lI < tempinfo.lSizeOf; lI++) 
  { 
    *pDst++ = *pSrc++;
  }

  return CIPHER_ERROR_NOERROR;
}



/*
 * Driver Selftest
 */
WORD32 CAST_SelfTest 
  (void* pTestContext) 
{

  #ifdef _DEBUG
   WORD32 i;

   WORD32 a[4] = { 0x67452301, 0x78563412, 0x89674523, 0x9A785634 };
   WORD32 b[4] = { 0x67452301, 0x78563412, 0x89674523, 0x9A785634 };
   WORD32 av[4]= { 0xa2d0a9ee, 0xa63bfd49, 0xb86f43b3, 0x92ca6d9d };
   WORD32 bv[4]= { 0xb05ec9b2, 0x71ad310c, 0xb805ac80, 0x6e693de8 };
  #endif

  /* test the driver for correct encrypting and decrypting... */
  CASTCTX* testCtx = (CASTCTX*) pTestContext;

  /* offical test vector from C. Adams; For details see [1] */
  WORD8 testKey[16] = { 0x01, 0x23, 0x45, 0x67, 0x12, 0x34, 0x56, 0x78,
                        0x23, 0x45, 0x67, 0x89, 0x34, 0x56, 0x78, 0x9A };
  WORD32 tv_p[2] = { 0x67452301, 0xefcdab89 };     /* little endian */
  WORD32 tv_c[2] = { 0xe54f8b23, 0xb2447e84 };
  WORD32 tv_t[2] = { 0x00000000, 0x00000000 };

  _cast_setkey(testCtx, testKey, 16);

  _cast_encrypt(testCtx, (WORD8*) tv_p, (WORD8*) tv_t);
  if ((tv_c[0] != tv_t[0]) || (tv_c[1] != tv_t[1]))
    return CIPHER_ERROR_INVALID;

  _cast_decrypt(testCtx, (WORD8*) tv_t, (WORD8*) tv_t);
  if ((tv_p[0] != tv_t[0]) || (tv_p[1] != tv_t[1]))
    return CIPHER_ERROR_INVALID;

  /* Only in the debug version is a full maintenance test
   * included. This test verify "very hard" the correctness
   * of the implementation and S-boxes. Please refer [1] for
   * more details. This test take up to some minutes,
   * depending on the CPU speed, so please don´t get confused.
   */

  #ifdef _DEBUG
   for (i=0 ; i<1000000 ; i++) 
   {
     _cast_setkey (testCtx, (WORD8*) b, 16);
     _cast_encrypt(testCtx, (WORD8*) &a[0], (WORD8*) &a[0]);
     _cast_encrypt(testCtx, (WORD8*) &a[2], (WORD8*) &a[2]);

     _cast_setkey (testCtx, (WORD8*) a, 16);
     _cast_encrypt(testCtx, (WORD8*) &b[0], (WORD8*) &b[0]);
     _cast_encrypt(testCtx, (WORD8*) &b[2], (WORD8*) &b[2]);
   }
   if ((a[0] != av[0]) || (a[1] != av[1]) ||
       (a[2] != av[2]) || (a[3] != av[3]))
     return CIPHER_ERROR_INVALID;

   if ((b[0] != bv[0]) || (b[1] != bv[1]) ||
       (b[2] != bv[2]) || (b[3] != bv[3]))
     return CIPHER_ERROR_INVALID;

  #endif


  /* Test passes */
  return CIPHER_ERROR_NOERROR;
}

/*
 * Create Work Context
 */
WORD32 CAST_CreateWorkContext
  (void* pContext,
   const WORD8* pKey,
   WORD32 lKeyLen,
   WORD32 lMode,
   void* pInitData,
   Cipher_RandomGenerator GetRndBytes,
   const void* pRndGenData) 
{
  WORD32* pCBCIV;
  CASTCTX* pCtx = (CASTCTX*) pContext;

  /* do the key setup */
  _cast_setkey(pCtx, (WORD8*)pKey, lKeyLen);
  
  /* for encryption create a CBC IV */
  pCBCIV = (WORD32*) pInitData;
  if (lMode == CIPHER_MODE_ENCRYPT)
  {
    GetRndBytes((WORD8*) pCBCIV, 8, pRndGenData); 
  }
 
  /* set the CBC IV */
  pCtx->lCBCLo = pCBCIV[0];
  pCtx->lCBCHi = pCBCIV[1];

  /* In CAST are no weak keys known */
  return CIPHER_ERROR_NOERROR;
}

/*
 * Reset Work Context
 */
void CAST_ResetWorkContext
  (void* pContext,
   WORD32 lMode,
   void* pInitData,
   Cipher_RandomGenerator GetRndBytes,
   const void* pRndGenData) 
{
  CASTCTX* pCtx = (CASTCTX*) pContext;

  /* just reset the CBC IV */
  WORD32* pCBCIV = (WORD32*) pInitData;

  if (lMode == CIPHER_MODE_ENCRYPT)
    GetRndBytes((WORD8*) pCBCIV, 8, pRndGenData);

  pCtx->lCBCLo = pCBCIV[0];
  pCtx->lCBCHi = pCBCIV[1];
}


/*
 * Destroy Work Context
 */
WORD32 CAST_DestroyWorkContext
  (void* pContext) 
{
  /* clear the context */
  int nI;
  WORD8* clearIt = (WORD8*) pContext;
  for (nI = 0; nI < sizeof(CASTCTX); nI++) clearIt[nI] = 0x00;
  return CIPHER_ERROR_NOERROR;
}

/*
 * Encrypt Buffer
 */
void CAST_EncryptBuffer
  (void* pContext,
   const void* pSource,
   void* pTarget,
   WORD32 lNumOfBytes) 
{
  WORD32 lNumOfInts;
  WORD32 lI;
  WORD32* pInBuf = (WORD32*) pSource;
  WORD32* pOutBuf = (WORD32*) pTarget;
  CASTCTX* pCtx = (CASTCTX*) pContext;

  /* calculate the number of (32bit) words */
  lNumOfInts = lNumOfBytes >> 2;

  /* anything to encrypt? */
  if (lNumOfInts < 2) return;

  /* work through all blocks... */
  for (lI = 0; lI < lNumOfInts; lI+=2) 
  {
    /* copy and chain the recent block */
     pOutBuf[lI]     = pInBuf[lI]     ^ pCtx->lCBCLo;
     pOutBuf[lI + 1] = pInBuf[lI + 1] ^ pCtx->lCBCHi;
     /* encrypt the block */
     _cast_encrypt(pCtx, (WORD8*) &pOutBuf[lI], (WORD8*) &pOutBuf[lI]);
     /* set the new CBC iv */
     pCtx->lCBCLo = pOutBuf[lI];
     pCtx->lCBCHi = pOutBuf[lI + 1];
  }
}

/*
 * Decrypt Buffer
 */
void CAST_DecryptBuffer
  (void* pContext,
   const void* pSource,
   void* pTarget,
   WORD32 lNumOfBytes,
   const void* pPreviousBlock) 
{
  WORD32 lNumOfInts;
  WORD32 lI;
  WORD32 lSaveCBCLo;
  WORD32 lSaveCBCHi;
  WORD32* pInBuf = (WORD32*) pSource;
  WORD32* pOutBuf = (WORD32*) pTarget;
  WORD32* pPrevBlock = (WORD32*) pPreviousBlock;
  CASTCTX* pCtx = (CASTCTX*) pContext;

  /* calculate the number of (32bit) words */
  lNumOfInts = lNumOfBytes >> 2;

  /* anything to decrypt? */
  if (lNumOfInts < 2) return;

  /* load a new CBC IV, if necessary */
  if (pPreviousBlock != CIPHER_NULL)  
  {
    pCtx->lCBCLo = pPrevBlock[0];
    pCtx->lCBCHi = pPrevBlock[1];
  }

  /* work through all blocks... */
  for (lI = 0; lI < lNumOfInts; lI += 2) 
  {
    /* save the recent CBC IV */
     lSaveCBCLo = pInBuf[lI];
    lSaveCBCHi = pInBuf[lI + 1];
     /* decrypt the block */
     _cast_decrypt(pCtx, (WORD8*) &pInBuf[lI], (WORD8*) &pOutBuf[lI]);
     /* dechain the recent block */
     pOutBuf[lI]     = pOutBuf[lI]     ^ pCtx->lCBCLo;
     pOutBuf[lI + 1] = pOutBuf[lI + 1] ^ pCtx->lCBCHi;
     /* set the new CBC iv */
     pCtx->lCBCLo = lSaveCBCLo;
     pCtx->lCBCHi = lSaveCBCHi;
  }
}



/*
 * That´s all for now, folks
 */
