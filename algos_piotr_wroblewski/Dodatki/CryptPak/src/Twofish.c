

#include <stdio.h>

#include "Twofish.h"


// work context

typedef struct
{
  // expanded S-boxes
  WORD32 sbox[4 * 256];

  // round subkeys, input/output whitening bits
  WORD32 subKeys[8 + 32];

  // CBC initialisation vector
  WORD32 cbc_iv[4];

} TWOFISHCTX;



// internal constants

#define INPUTWHITEN     0
#define OUTPUTWHITEN    (TWOFISH_BLOCKSIZE / 4)
#define KEYBITS         (TWOFISH_KEYSIZE * 8)
#define NUMROUNDS       16
#define ROUNDSUBKEYS    (OUTPUTWHITEN + TWOFISH_BLOCKSIZE / 4)
#define TOTALSUBKEYS    (ROUNDSUBKEYS + NUMROUNDS * 2)
#define RS_GF_FDBK      0x14d
#define SK_STEP         0x02020202u
#define SK_BUMP         0x01010101u
#define SK_ROTL         9

// for accesing the permutation S-boxes more easily
#define P_00            1
#define P_01            0
#define P_02            0
#define P_03            (P_01 ^ 1)
#define P_04            1
#define P_10            0
#define P_11            0
#define P_12            1
#define P_13            (P_11 ^ 1)
#define P_14            0
#define P_20            1
#define P_21            1
#define P_22            0
#define P_23            (P_21 ^ 1)
#define P_24            0
#define P_30            0
#define P_31            1
#define P_32            1
#define P_33            (P_31 ^ 1)
#define P_34            1
#define p8(N)           p8x8[P_##N]

// the fixed 8x8 permutation S-boxes themselves
WORD8 p8x8[2][256] =
{
    0xa9, 0x67, 0xb3, 0xe8, 0x04, 0xfd, 0xa3, 0x76,
    0x9a, 0x92, 0x80, 0x78, 0xe4, 0xdd, 0xd1, 0x38,
    0x0d, 0xc6, 0x35, 0x98, 0x18, 0xf7, 0xec, 0x6c,
    0x43, 0x75, 0x37, 0x26, 0xfa, 0x13, 0x94, 0x48,
    0xf2, 0xd0, 0x8b, 0x30, 0x84, 0x54, 0xdf, 0x23,
    0x19, 0x5b, 0x3d, 0x59, 0xf3, 0xae, 0xa2, 0x82,
    0x63, 0x01, 0x83, 0x2e, 0xd9, 0x51, 0x9b, 0x7c,
    0xa6, 0xeb, 0xa5, 0xbe, 0x16, 0x0c, 0xe3, 0x61,
    0xc0, 0x8c, 0x3a, 0xf5, 0x73, 0x2c, 0x25, 0x0b,
    0xbb, 0x4e, 0x89, 0x6b, 0x53, 0x6a, 0xb4, 0xf1,
    0xe1, 0xe6, 0xbd, 0x45, 0xe2, 0xf4, 0xb6, 0x66,
    0xcc, 0x95, 0x03, 0x56, 0xd4, 0x1c, 0x1e, 0xd7,
    0xfb, 0xc3, 0x8e, 0xb5, 0xe9, 0xcf, 0xbf, 0xba,
    0xea, 0x77, 0x39, 0xaf, 0x33, 0xc9, 0x62, 0x71,
    0x81, 0x79, 0x09, 0xad, 0x24, 0xcd, 0xf9, 0xd8,
    0xe5, 0xc5, 0xb9, 0x4d, 0x44, 0x08, 0x86, 0xe7,
    0xa1, 0x1d, 0xaa, 0xed, 0x06, 0x70, 0xb2, 0xd2,
    0x41, 0x7b, 0xa0, 0x11, 0x31, 0xc2, 0x27, 0x90,
    0x20, 0xf6, 0x60, 0xff, 0x96, 0x5c, 0xb1, 0xab,
    0x9e, 0x9c, 0x52, 0x1b, 0x5f, 0x93, 0x0a, 0xef,
    0x91, 0x85, 0x49, 0xee, 0x2d, 0x4f, 0x8f, 0x3b,
    0x47, 0x87, 0x6d, 0x46, 0xd6, 0x3e, 0x69, 0x64,
    0x2a, 0xce, 0xcb, 0x2f, 0xfc, 0x97, 0x05, 0x7a,
    0xac, 0x7f, 0xd5, 0x1a, 0x4b, 0x0e, 0xa7, 0x5a,
    0x28, 0x14, 0x3f, 0x29, 0x88, 0x3c, 0x4c, 0x02,
    0xb8, 0xda, 0xb0, 0x17, 0x55, 0x1f, 0x8a, 0x7d,
    0x57, 0xc7, 0x8d, 0x74, 0xb7, 0xc4, 0x9f, 0x72,
    0x7e, 0x15, 0x22, 0x12, 0x58, 0x07, 0x99, 0x34,
    0x6e, 0x50, 0xde, 0x68, 0x65, 0xbc, 0xdb, 0xf8,
    0xc8, 0xa8, 0x2b, 0x40, 0xdc, 0xfe, 0x32, 0xa4,
    0xca, 0x10, 0x21, 0xf0, 0xd3, 0x5d, 0x0f, 0x00,
    0x6f, 0x9d, 0x36, 0x42, 0x4a, 0x5e, 0xc1, 0xe0,
    0x75, 0xf3, 0xc6, 0xf4, 0xdb, 0x7b, 0xfb, 0xc8,
    0x4a, 0xd3, 0xe6, 0x6b, 0x45, 0x7d, 0xe8, 0x4b,
    0xd6, 0x32, 0xd8, 0xfd, 0x37, 0x71, 0xf1, 0xe1,
    0x30, 0x0f, 0xf8, 0x1b, 0x87, 0xfa, 0x06, 0x3f,
    0x5e, 0xba, 0xae, 0x5b, 0x8a, 0x00, 0xbc, 0x9d,
    0x6d, 0xc1, 0xb1, 0x0e, 0x80, 0x5d, 0xd2, 0xd5,
    0xa0, 0x84, 0x07, 0x14, 0xb5, 0x90, 0x2c, 0xa3,
    0xb2, 0x73, 0x4c, 0x54, 0x92, 0x74, 0x36, 0x51,
    0x38, 0xb0, 0xbd, 0x5a, 0xfc, 0x60, 0x62, 0x96,
    0x6c, 0x42, 0xf7, 0x10, 0x7c, 0x28, 0x27, 0x8c,
    0x13, 0x95, 0x9c, 0xc7, 0x24, 0x46, 0x3b, 0x70,
    0xca, 0xe3, 0x85, 0xcb, 0x11, 0xd0, 0x93, 0xb8,
    0xa6, 0x83, 0x20, 0xff, 0x9f, 0x77, 0xc3, 0xcc,
    0x03, 0x6f, 0x08, 0xbf, 0x40, 0xe7, 0x2b, 0xe2,
    0x79, 0x0c, 0xaa, 0x82, 0x41, 0x3a, 0xea, 0xb9,
    0xe4, 0x9a, 0xa4, 0x97, 0x7e, 0xda, 0x7a, 0x17,
    0x66, 0x94, 0xa1, 0x1d, 0x3d, 0xf0, 0xde, 0xb3,
    0x0b, 0x72, 0xa7, 0x1c, 0xef, 0xd1, 0x53, 0x3e,
    0x8f, 0x33, 0x26, 0x5f, 0xec, 0x76, 0x2a, 0x49,
    0x81, 0x88, 0xee, 0x21, 0xc4, 0x1a, 0xeb, 0xd9,
    0xc5, 0x39, 0x99, 0xcd, 0xad, 0x31, 0x8b, 0x01,
    0x18, 0x23, 0xdd, 0x1f, 0x4e, 0x2d, 0xf9, 0x48,
    0x4f, 0xf2, 0x65, 0x8e, 0x78, 0x5c, 0x58, 0x19,
    0x8d, 0xe5, 0x98, 0x57, 0x67, 0x7f, 0x05, 0x64,
    0xaf, 0x63, 0xb6, 0xfe, 0xf5, 0xb7, 0x3c, 0xa5,
    0xce, 0xe9, 0x68, 0x44, 0xe0, 0x4d, 0x43, 0x69,
    0x29, 0x2e, 0xac, 0x15, 0x59, 0xa8, 0x0a, 0x9e,
    0x6e, 0x47, 0xdf, 0x34, 0x35, 0x6a, 0xcf, 0xdc,
    0x22, 0xc9, 0xc0, 0x9b, 0x89, 0xd4, 0xed, 0xab,
    0x12, 0xa2, 0x0d, 0x52, 0xbb, 0x02, 0x2f, 0xa9,
    0xd7, 0x61, 0x1e, 0xb4, 0x50, 0x04, 0xf6, 0xc2,
    0x16, 0x25, 0x86, 0x56, 0x55, 0x09, 0xbe, 0x91
};


// some macros

// (32bit) rotations
#define ROL(x,n)    (((x) << (n)) | ((x) >> (32 - (n))))
#define ROR(x,n)    (((x) >> (n)) | ((x) << (32 - (n))))

// some stuff for the complex f32() function
#define MDS_GF_FDBK     0x169
#define LFSR1(x) (((x) >> 1) ^ (((x) & 0x01) ? MDS_GF_FDBK/2 : 0))
#define LFSR2(x) (((x) >> 2) ^ (((x) & 0x02) ? MDS_GF_FDBK/2 : 0)  \
                             ^ (((x) & 0x01) ? MDS_GF_FDBK/4 : 0))
#define Mx_1(x) ((WORD32) (x))
#define Mx_X(x) ((WORD32) ((x) ^ LFSR2(x)))
#define Mx_Y(x) ((WORD32) ((x) ^ LFSR1(x) ^ LFSR2(x)))

#define Mul_1   Mx_1
#define Mul_X   Mx_X
#define Mul_Y   Mx_Y
#define M00     Mul_1
#define M01     Mul_Y
#define M02     Mul_X
#define M03     Mul_X
#define M10     Mul_X
#define M11     Mul_Y
#define M12     Mul_Y
#define M13     Mul_1
#define M20     Mul_Y
#define M21     Mul_X
#define M22     Mul_1
#define M23     Mul_Y
#define M30     Mul_Y
#define M31     Mul_1
#define M32     Mul_Y
#define M33     Mul_X

// for byte extraction from a 32bit word
#define b0(x)   ((x) & 0x0ff)
#define b1(x)   (((x) >> 8) & 0x0ff)
#define b2(x)   (((x) >> 16) & 0x0ff)
#define b3(x)   ((x) >> 24)



// optimized Fe32 macro: instead of a _b() function with a "switch() {...}"
// we use a lookup table with shift values

#define _bopt(x, n) (((x) >> (blu[(n) & 3])) & 0x0ff)
#define Fe32(sbox, x, r) (sbox[        (_bopt((x), (r)    ) << 1)] ^ \
                          sbox[    1 + (_bopt((x), (r) + 1) << 1)] ^ \
                          sbox[0x200 + (_bopt((x), (r) + 2) << 1)] ^ \
                          sbox[0x201 + (_bopt((x), (r) + 3) << 1)])


// internal static stuff

// the MDS matrix (will be precomputed on startup by PreCompMDS())
static WORD32 mds[4][256];

// lookup table for the Fe32() macro
static WORD32 blu[4] = { 0, 8, 16, 24 };



// support routines



// precomputes the MDS matrix, just called one time
void Twofish_PreCompMDS()
{
  WORD8 m1[2];
  WORD8 mx[2];
  WORD8 my[2];
  int nI;

  for (nI = 0; nI < 256; nI++)
  {
    // compute all the matrix elements
    m1[0] = p8x8[0][nI];
    mx[0] = (WORD8)Mul_X(m1[0]);
    my[0] = (WORD8)Mul_Y(m1[0]);
    m1[1] = p8x8[1][nI];
    mx[1] = (WORD8)Mul_X(m1[1]);
    my[1] = (WORD8)Mul_Y(m1[1]);

    // fill matrix
    mds[0][nI] = m1[P_00] <<  0 |
                 mx[P_00] <<  8 |
                 my[P_00] << 16 |
                 my[P_00] << 24;
    mds[1][nI] = my[P_10] <<  0 |
                 my[P_10] <<  8 |
                 mx[P_10] << 16 |
                 m1[P_10] << 24;
    mds[2][nI] = mx[P_20] <<  0 |
                 my[P_20] <<  8 |
                 m1[P_20] << 16 |
                 my[P_20] << 24;
    mds[3][nI] = mx[P_30] <<  0 |
                 m1[P_30] <<  8 |
                 my[P_30] << 16 |
                 mx[P_30] << 24;
  }
}



// use (12,8) Reed-Solomon code over GF(256) to produce
// a key S-box dword from two key material dwords
WORD32 RS_MDS_Encode
  (WORD32 lK0,
   WORD32 lK1)
{

  WORD32 lR;
  int nI, nJ;
  for (nI = lR = 0; nI < 2; nI++)
  {
    // merge in 32 more key bits
    lR ^= (nI) ? lK0 : lK1;

    // shift one byte at a time
    for (nJ = 0; nJ < 4; nJ++)
    {
      WORD8 bB = (WORD8)(lR >> 24);
      WORD32 lG2 = ((bB << 1) ^ ((bB & 0x80) ? RS_GF_FDBK : 0)) & 0xff;
      WORD32 lG3 = ((bB >> 1) & 0x7f) ^ ((bB & 1) ? RS_GF_FDBK >> 1 : 0) ^ lG2;
      lR = (lR << 8) ^ (lG3 << 24) ^ (lG2 << 16) ^ (lG3 << 8) ^ bB;
    }
  }
  return lR;
}



// run four bytes through keyed S-boxes
WORD32 f32
  (WORD32 lX,
   WORD32* pK32)
{
  int nB0 = b0(lX);     // use direct indexing
  int nB1 = b1(lX);
  int nB2 = b2(lX);
  int nB3 = b3(lX);
  WORD32 lK0 = pK32[0];
  WORD32 lK1 = pK32[1];
  WORD32 lK2 = pK32[2];
  WORD32 lK3 = pK32[3];

  nB0 = p8(04)[nB0] ^ b0(lK3);
  nB1 = p8(14)[nB1] ^ b1(lK3);
  nB2 = p8(24)[nB2] ^ b2(lK3);
  nB3 = p8(34)[nB3] ^ b3(lK3);

  nB0 = p8(03)[nB0] ^ b0(lK2);
  nB1 = p8(13)[nB1] ^ b1(lK2);
  nB2 = p8(23)[nB2] ^ b2(lK2);
  nB3 = p8(33)[nB3] ^ b3(lK2);

  return mds[0][p8(01)[p8(02)[nB0] ^ b0(lK1)] ^ b0(lK0)] ^
         mds[1][p8(11)[p8(12)[nB1] ^ b1(lK1)] ^ b1(lK0)] ^
         mds[2][p8(21)[p8(22)[nB2] ^ b2(lK1)] ^ b2(lK0)] ^
         mds[3][p8(31)[p8(32)[nB3] ^ b3(lK1)] ^ b3(lK0)] ;
}




// macro for the unrolled encryption loop, used in the following function
#define enc_loop(x0, x1, x2, x3, r)                         \
  lT0 = Fe32(sbox, x0, 0);                                  \
  lT1 = Fe32(sbox, x1, 3);                                  \
  x2 ^= lT0 + lT1 + subKeys[ROUNDSUBKEYS + (r)];            \
  x2 = ROR(x2, 1);                                          \
  x3 = ROL(x3, 1);                                          \
  x3 ^= lT0 + (lT1 << 1) + subKeys[ROUNDSUBKEYS + (r) + 1];



// encrypts a block
void twofish_blockEncrypt
  (TWOFISHCTX* pCtx,
   WORD8* pPlainBlock)
{
    // copy that for more speed
    WORD32* sbox = pCtx->sbox;
    WORD32* subKeys = pCtx->subKeys;
    WORD32* pBlock = (WORD32*) pPlainBlock;

    // get and whiten the block locally
    WORD32 lX0 = pBlock[0] ^ pCtx->subKeys[INPUTWHITEN];
    WORD32 lX1 = pBlock[1] ^ pCtx->subKeys[INPUTWHITEN + 1];
    WORD32 lX2 = pBlock[2] ^ pCtx->subKeys[INPUTWHITEN + 2];
    WORD32 lX3 = pBlock[3] ^ pCtx->subKeys[INPUTWHITEN + 3];

    // encryption loop (100% unrolled - fat, but fast)
    WORD32 lT0;
    WORD32 lT1;
    enc_loop(lX0, lX1, lX2, lX3, 0)
    enc_loop(lX2, lX3, lX0, lX1, 2)
    enc_loop(lX0, lX1, lX2, lX3, 4)
    enc_loop(lX2, lX3, lX0, lX1, 6)
    enc_loop(lX0, lX1, lX2, lX3, 8)
    enc_loop(lX2, lX3, lX0, lX1, 10)
    enc_loop(lX0, lX1, lX2, lX3, 12)
    enc_loop(lX2, lX3, lX0, lX1, 14)
    enc_loop(lX0, lX1, lX2, lX3, 16)
    enc_loop(lX2, lX3, lX0, lX1, 18)
    enc_loop(lX0, lX1, lX2, lX3, 20)
    enc_loop(lX2, lX3, lX0, lX1, 22)
    enc_loop(lX0, lX1, lX2, lX3, 24)
    enc_loop(lX2, lX3, lX0, lX1, 26)
    enc_loop(lX0, lX1, lX2, lX3, 28)
    enc_loop(lX2, lX3, lX0, lX1, 30)

    // final swap, whitening and back copy
    pBlock[0] = lX2 ^ pCtx->subKeys[OUTPUTWHITEN];
    pBlock[1] = lX3 ^ pCtx->subKeys[OUTPUTWHITEN + 1];
    pBlock[2] = lX0 ^ pCtx->subKeys[OUTPUTWHITEN + 2];
    pBlock[3] = lX1 ^ pCtx->subKeys[OUTPUTWHITEN + 3];
}



// macro for the unrolled decryption loop, used in the following function
#define dec_loop(x0, x1, x2, x3, r)                      \
  lT0 = Fe32(sbox, x2, 0);                               \
  lT1 = Fe32(sbox, x3, 3);                               \
  x1 ^= lT0 + (lT1 << 1) + subKeys[ROUNDSUBKEYS + (r)];  \
  x1 = ROR(x1, 1);                                       \
  x0 = ROL(x0, 1);                                       \
  x0 ^= lT0 + lT1 + subKeys[ROUNDSUBKEYS + (r) - 1];

// decrypts a block
void twofish_blockDecrypt
  (TWOFISHCTX* pCtx,
   void* pCipherBlock)
{
    // copy that for more speed
    WORD32* sbox = pCtx->sbox;
    WORD32* subKeys = pCtx->subKeys;
    WORD32* pBlock = (WORD32*) pCipherBlock;

    // get and rewhiten the block locally
    WORD32 lX2 = pBlock[0] ^ pCtx->subKeys[OUTPUTWHITEN];
    WORD32 lX3 = pBlock[1] ^ pCtx->subKeys[OUTPUTWHITEN + 1];
    WORD32 lX0 = pBlock[2] ^ pCtx->subKeys[OUTPUTWHITEN + 2];
    WORD32 lX1 = pBlock[3] ^ pCtx->subKeys[OUTPUTWHITEN + 3];

    // decryption loop (unrolled)
    WORD32 lT0;
    WORD32 lT1;
    dec_loop(lX0, lX1, lX2, lX3, 31)
    dec_loop(lX2, lX3, lX0, lX1, 29)
    dec_loop(lX0, lX1, lX2, lX3, 27)
    dec_loop(lX2, lX3, lX0, lX1, 25)
    dec_loop(lX0, lX1, lX2, lX3, 23)
    dec_loop(lX2, lX3, lX0, lX1, 21)
    dec_loop(lX0, lX1, lX2, lX3, 19)
    dec_loop(lX2, lX3, lX0, lX1, 17)
    dec_loop(lX0, lX1, lX2, lX3, 15)
    dec_loop(lX2, lX3, lX0, lX1, 13)
    dec_loop(lX0, lX1, lX2, lX3, 11)
    dec_loop(lX2, lX3, lX0, lX1, 9)
    dec_loop(lX0, lX1, lX2, lX3, 7)
    dec_loop(lX2, lX3, lX0, lX1, 5)
    dec_loop(lX0, lX1, lX2, lX3, 3)
    dec_loop(lX2, lX3, lX0, lX1, 1)

    // final rewhitening and back copy
    pBlock[0] = lX0 ^ pCtx->subKeys[INPUTWHITEN];
    pBlock[1] = lX1 ^ pCtx->subKeys[INPUTWHITEN + 1];
    pBlock[2] = lX2 ^ pCtx->subKeys[INPUTWHITEN + 2];
    pBlock[3] = lX3 ^ pCtx->subKeys[INPUTWHITEN + 3];
}



// interface implementation

WORD32 Twofish_GetCipherInfo
  (CIPHERINFOBLOCK *pInfo)
{
  WORD8* pSrc;
  WORD8* pDst;
  CIPHERINFOBLOCK tempinfo;
  WORD32 lI;

  // prepare the information context
  tempinfo.lSizeOf = pInfo->lSizeOf;
  tempinfo.lBlockSize = TWOFISH_BLOCKSIZE;
  tempinfo.lKeySize = TWOFISH_KEYSIZE;
  tempinfo.blOwnHasher = BOOL_FALSE;
  tempinfo.lInitDataSize = TWOFISH_BLOCKSIZE;
  tempinfo.lContextSize = sizeof(TWOFISHCTX);
  tempinfo.bCipherIs = CIPHER_IS_BLOCKLINK;

  // copy as many bytes of the information block as possible
  pSrc = (WORD8*) &tempinfo;
  pDst = (WORD8*) pInfo;
  for (lI = 0; lI < tempinfo.lSizeOf; lI++)
    *pDst++ = *pSrc++;

  return CIPHER_ERROR_NOERROR;
}



WORD32 Twofish_SelfTest
  (void* pCtx)
{
  // encrypt, decrypt and check an offical test vector

  WORD8 testkey[32] =
  {
    0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF,
    0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10,
    0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
    0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF
  };

  WORD8 plaintext[16] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
  };

  WORD8 cipher_must[16] =
  {
    0x37, 0x52, 0x7B, 0xE0, 0x05, 0x23, 0x34, 0xB8,
    0x9F, 0x0C, 0xFC, 0xCA, 0xE8, 0x7C, 0xFA, 0x20
  };

  WORD8 ciphertext[16];
  WORD8 initdata[16];
  int nI;

  for (nI = 0; nI < 16; nI++) initdata[nI] = 0;

  // create a context (used for en- and decryption,
  // because CBC isn't used and we init. in decryption
  // mode we don't need a random number generator)
  Twofish_CreateWorkContext(pCtx,
                            testkey,
                            32,
                            CIPHER_MODE_DECRYPT,
                            initdata,
                            0,
                            0);

  // test the encryption
  for (nI = 0; nI < 16; nI++)
    ciphertext[nI] = plaintext[nI];

  twofish_blockEncrypt((TWOFISHCTX*)pCtx, ciphertext);

  for (nI = 0; nI < 16; nI++)
    if (ciphertext[nI] != cipher_must[nI])
      return CIPHER_ERROR_INVALID;

  // test the decryption
  twofish_blockDecrypt((TWOFISHCTX*)pCtx, ciphertext);

  for (nI = 0; nI < 16; nI++)
    if (ciphertext[nI] != plaintext[nI])
      return CIPHER_ERROR_INVALID;

  // tests passed
  return CIPHER_ERROR_NOERROR;
}



WORD32 Twofish_CreateWorkContext
  (void* pContext,
   const WORD8* pKey,
   WORD32 lKeyLen,
   WORD32 lMode,
   void* pInitData,
   Cipher_RandomGenerator GetRndBytes,
   const void* pRndGenData)
{
  WORD32* pKeySrc;
  WORD32* pHelpPtr;

  int nI, nJ, nQ;

  WORD32 lA;
  WORD32 lB;

  TWOFISHCTX* pCtx = (TWOFISHCTX*) pContext;

  WORD32 lK0, lK1, lK2, lK3;
  WORD32 lB0, lB1, lB2, lB3;

  WORD32 key32[TWOFISH_KEYSIZE / 4];
  WORD32 sboxKeys[TWOFISH_KEYSIZE / 8];

  // even and odd key dwords
  WORD32 k32e[TWOFISH_KEYSIZE / 8];
  WORD32 k32o[TWOFISH_KEYSIZE / 8];

  // zero unused bits
  for (nI = 0; nI < (TWOFISH_KEYSIZE / 4); nI++)
    key32[nI] = 0;

  // copy the key material, depend on a fixed key size(!)
  // (direct copy is possible here)
  pKeySrc = (WORD32*)pKey;
  for (nI = 0; nI < (TWOFISH_KEYSIZE / sizeof(WORD32)); nI++)
    key32[nI] = pKeySrc[nI];

  // calculate the subkeys, pass #1
  nJ = (TWOFISH_KEYSIZE / 8) - 1;
  for (nI = 0; nI < (TWOFISH_KEYSIZE / 8); nI++)
  {
    // split into even/odd key dwords
    k32e[nI] = key32[nI << 1];
    k32o[nI] = key32[(nI << 1) + 1];

    // compute S-box keys using (12,8) Reed-Solomon code over GF(256),
    // in reversed order
    sboxKeys[nJ--] = RS_MDS_Encode(k32e[nI], k32o[nI]);
  }

  // compute round subkeys for PHT
  nQ = 0;
  for (nI = 0; nI < (TOTALSUBKEYS / 2); nI++, nQ += SK_STEP)
  {
    lA = f32(nQ,           k32e); // lA uses even key dwords
    lB = f32(nQ + SK_BUMP, k32o); // lB uses odd key dwords
    lB = ROL(lB, 8);

    // combine with a PHT
    pCtx->subKeys[nI << 1] = lA + lB;
    lB = lA + (lB << 1);
    pCtx->subKeys[(nI << 1) + 1] = ROL(lB, SK_ROTL);
  }

  // fully expand the table (subkeys calc., pass #2)
  lK0 = sboxKeys[0];
  lK1 = sboxKeys[1];
  lK2 = sboxKeys[2];
  lK3 = sboxKeys[3];
  for (nI = 0; nI < 256; nI++)
  {
    lB0 = p8(04)[nI] ^ b0(lK3);
    lB1 = p8(14)[nI] ^ b1(lK3);
    lB2 = p8(24)[nI] ^ b2(lK3);
    lB3 = p8(34)[nI] ^ b3(lK3);

    lB0 = p8(03)[lB0] ^ b0(lK2);
    lB1 = p8(13)[lB1] ^ b1(lK2);
    lB2 = p8(23)[lB2] ^ b2(lK2);
    lB3 = p8(33)[lB3] ^ b3(lK2);

    pCtx->sbox[        (nI << 1)] = mds[0][p8(01)[p8(02)[lB0] ^ b0(lK1)] ^ b0(lK0)];
    pCtx->sbox[    1 + (nI << 1)] = mds[1][p8(11)[p8(12)[lB1] ^ b1(lK1)] ^ b1(lK0)];
    pCtx->sbox[0x200 + (nI << 1)] = mds[2][p8(21)[p8(22)[lB2] ^ b2(lK1)] ^ b2(lK0)];
    pCtx->sbox[0x201 + (nI << 1)] = mds[3][p8(31)[p8(32)[lB3] ^ b3(lK1)] ^ b3(lK0)];
  }

  // clear all the local buffers now
  for (nI = 0; nI < (TWOFISH_KEYSIZE / 4); nI++)
    key32[nI] = 0;
  for (nI = 0; nI < (TWOFISH_KEYSIZE / 8); nI++)
    k32e[nI] = k32o[nI] = 0;
  for (nI = 0; nI < (TWOFISH_KEYSIZE / 8); nI++)
    sboxKeys[nI] = 0;

  // create and save the CBC iv or get it for decryption
  pHelpPtr = (WORD32*) pInitData;
  if (lMode == CIPHER_MODE_ENCRYPT)
  {
    GetRndBytes((WORD8*)&pCtx->cbc_iv[0],
                16,
                pRndGenData);

    for (nI = 0; nI < 4; nI++)
      pHelpPtr[nI] = pCtx->cbc_iv[nI];
  }
  else
  {
    for (nI = 0; nI < 4; nI++)
      pCtx->cbc_iv[nI] = pHelpPtr[nI];
  }

  return CIPHER_ERROR_NOERROR;
}


void Twofish_ResetWorkContext
  (void* pContext,
   WORD32 lMode,
   void* pInitData,
   Cipher_RandomGenerator GetRndBytes,
   const void* pRndGenData)
{
  int nI;
  WORD32* pHelpPtr;
  TWOFISHCTX* pCtx = (TWOFISHCTX*) pContext;

  // create and save the CBC iv or get it for decryption
  pHelpPtr = (WORD32*) pInitData;
  if (lMode == CIPHER_MODE_ENCRYPT)
  {
    GetRndBytes((WORD8*)&pCtx->cbc_iv[0], 16, pRndGenData);
    for (nI = 0; nI < 4; nI++)
      pHelpPtr[nI] = pCtx->cbc_iv[nI];
  }
  else
  {
    for (nI = 0; nI<4; nI++)
      pCtx->cbc_iv[nI] = pHelpPtr[nI];
  }
}



WORD32 Twofish_DestroyWorkContext
(void* pContext)
{
  WORD8* pDel = (WORD8*) pContext;
  int nI;

  // just clear the context
  for (nI = 0; nI < sizeof(TWOFISHCTX); nI++)
    *pDel++ = 0x00;

  return CIPHER_ERROR_NOERROR;
}




void Twofish_EncryptBuffer
  (void* pContext,
   const void* pSource,
   void* pTarget,
   WORD32 lNumOfBytes)
{
  WORD32 lI, lJ;
  WORD32* pInBuf = (WORD32*) pSource;
  WORD32* pOutBuf = (WORD32*) pTarget;
  TWOFISHCTX* pCtx = (TWOFISHCTX*) pContext;

  // work through all blocks
  for (lI = 0; lI < (lNumOfBytes / TWOFISH_BLOCKSIZE); lI++)
  {
    // copy and chain the actual block
    for (lJ = 0; lJ < 4; lJ++)
    {
      pOutBuf[lJ] = pInBuf[lJ];
      pOutBuf[lJ] ^= pCtx->cbc_iv[lJ];
    }

    // encrypt the block
    twofish_blockEncrypt(pCtx, (WORD8*)pOutBuf);

    // set the new cbc iv
    for (lJ = 0; lJ < 4; lJ++)
      pCtx->cbc_iv[lJ] = pOutBuf[lJ];

    // next block
    pInBuf += TWOFISH_BLOCKSIZE / sizeof(WORD32);
    pOutBuf += TWOFISH_BLOCKSIZE / sizeof(WORD32);
  }
}



void Twofish_DecryptBuffer
  (void* pContext,
   const void* pSource,
   void* pTarget,
   WORD32 lNumOfBytes,
   const void* pPreviousBlock)
{
  WORD32 lI, lJ;
  WORD32* pInBuf = (WORD32*) pSource;
  WORD32* pOutBuf = (WORD32*) pTarget;
  WORD32 save_cbc_iv[4];
  TWOFISHCTX* pCtx = (TWOFISHCTX*) pContext;

  // load a new CBC IV, if necessary
  if (pPreviousBlock != CIPHER_NULL)
  {
    for (lI = 0; lI < 4; lI++)
      pCtx->cbc_iv[lI] = ((WORD32*)pPreviousBlock)[lI];
  }

  // work through all blocks
  for (lI = 0; lI < (lNumOfBytes / TWOFISH_BLOCKSIZE); lI++)
  {
    // copy and chain the actual block
    for (lJ = 0; lJ < 4; lJ++)
      pOutBuf[lJ] = save_cbc_iv[lJ] = pInBuf[lJ];

    // decrypt the block
    twofish_blockDecrypt(pCtx, (WORD8*)pOutBuf);

    // rechain the block and set the new cbc iv
    for (lJ = 0; lJ < 4; lJ++)
    {
      pOutBuf[lJ] ^= pCtx->cbc_iv[lJ];
      pCtx->cbc_iv[lJ] = save_cbc_iv[lJ];
    }

    // next block
    pInBuf += TWOFISH_BLOCKSIZE / sizeof(WORD32);
    pOutBuf += TWOFISH_BLOCKSIZE / sizeof(WORD32);
  }
}
