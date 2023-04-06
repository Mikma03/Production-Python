

#include "cpkernel.h"
#include "MD5.h"

#include <stdlib.h>
#include <memory.h>
#include <string.h>



// constants for MD5Transform routine.
#define S11  7
#define S12  12
#define S13  17
#define S14  22
#define S21  5
#define S22  9
#define S23  14
#define S24  20
#define S31  4
#define S32  11
#define S33  16
#define S34  23
#define S41  6
#define S42  10
#define S43  15
#define S44  21


// prototypes of the support routines
void _MD5_transform (WORD32[4], WORD8[64]);
void _MD5_encode (WORD8 *, WORD32*, WORD32);
void _MD5_decode (WORD32*, WORD8 *, WORD32);


// F, G, H and I are basic MD5 functions.
#define F(x, y, z) (((x) & (y)) | ((~x) & (z)))
#define G(x, y, z) (((x) & (z)) | ((y) & (~z)))
#define H(x, y, z) ((x) ^ (y) ^ (z))
#define I(x, y, z) ((y) ^ ((x) | (~z)))

// ROTATE_LEFT rotates x left n bits.
#define ROTATE_LEFT(x, n) (((x) << (n)) | ((x) >> (32-(n))))

// FF, GG, HH, and II transformations for rounds 1, 2, 3, and 4.
// Rotation is separate from addition to prevent recomputation.
#define FF(a, b, c, d, x, s, ac) {                  \
    (a) += F ((b), (c), (d)) + (x) + (WORD32)(ac);  \
    (a) = ROTATE_LEFT ((a), (s));                   \
    (a) += (b);                                     \
  }
#define GG(a, b, c, d, x, s, ac) {                  \
    (a) += G ((b), (c), (d)) + (x) + (WORD32)(ac);  \
    (a) = ROTATE_LEFT ((a), (s));                   \
    (a) += (b);                                     \
  }
#define HH(a, b, c, d, x, s, ac) {                  \
    (a) += H ((b), (c), (d)) + (x) + (WORD32)(ac);  \
    (a) = ROTATE_LEFT ((a), (s));                   \
    (a) += (b);                                     \
  }
#define II(a, b, c, d, x, s, ac) {                  \
    (a) += I ((b), (c), (d)) + (x) + (WORD32)(ac);  \
    (a) = ROTATE_LEFT ((a), (s));                   \
    (a) += (b);                                     \
  }



PMD5CTX CRYPTPAK_API MD5_Create() 
{
  PMD5CTX pCtx = (PMD5CTX) malloc(sizeof(MD5CTX));

  MD5_Initialize(pCtx);

  return pCtx;
}


void CRYPTPAK_API MD5_Initialize
  (PMD5CTX pCtx) 
{
  MD5_Reset(pCtx);
}


void CRYPTPAK_API MD5_Reset
  (PMD5CTX pCtx) 
{
  pCtx->count[0] = pCtx->count[1] = 0;

  // load magic init. constants.
  pCtx->state[0] = 0x67452301;
  pCtx->state[1] = 0xefcdab89;
  pCtx->state[2] = 0x98badcfe;
  pCtx->state[3] = 0x10325476;
}


void CRYPTPAK_API MD5_Destroy
  (PMD5CTX pCtx) 
{
  memset(pCtx, 0, sizeof(MD5CTX));
  free(pCtx);
}



void CRYPTPAK_API MD5_Update
  (PMD5CTX pCtx, 
   const void* pData, 
   WORD32 lNumOfBytes) 
{
  WORD8* pInput = (WORD8*) pData;
  WORD32 lI, lIndex, lPartLen;

  // compute number of bytes mod 64
  lIndex = (WORD32)((pCtx->count[0] >> 3) & 0x3F);

  // update number of bits
  if ((pCtx->count[0] += ((WORD32)lNumOfBytes << 3)) < ((WORD32)lNumOfBytes << 3))
    pCtx->count[1]++;
  pCtx->count[1] += ((WORD32)lNumOfBytes >> 29);
  
  lPartLen = 64 - lIndex;
  
  // transform as many times as possible.
  if (lNumOfBytes >= lPartLen) 
  {
    memcpy(&pCtx->buffer[lIndex], pInput, lPartLen);
    _MD5_transform (pCtx->state, pCtx->buffer);

    for (lI = lPartLen; lI + 63 < lNumOfBytes; lI += 64)
      _MD5_transform (pCtx->state, &pInput[lI]);

    lIndex = 0;
  }
  else lI = 0;
  
  // buffer remaining input
  memcpy(&pCtx->buffer[lIndex], 
         &pInput[lI], 
         lNumOfBytes - lI);
}



void CRYPTPAK_API MD5_Final
  (WORD8 digest[MD5_DIGESTSIZE], 
   PMD5CTX pCtx ) 
{
  // to allow multithreading we have to locate the padding memory here
  WORD8 PADDING[64] = {
  0x80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
  };

  WORD8 bits[8];
  WORD32 lIndex, lPadLen;

  // save number of bits
  _MD5_encode(bits, pCtx->count, 8);

  // pad out to 56 mod 64
  lIndex = (WORD32)((pCtx->count[0] >> 3) & 0x3f);
  lPadLen = (lIndex < 56) ? (56 - lIndex) : (120 - lIndex);
  MD5_Update(pCtx, PADDING, lPadLen);
  
  // append length (before padding)
  MD5_Update(pCtx, bits, 8);

  // store state in digest
  _MD5_encode(digest, pCtx->state, 16);
  
  // clear sensitive information.
  memset(pCtx, 0, sizeof(MD5CTX));
}




// the selftest strings and digests
static char* selfTestSource[3] = 
{
  "hellooo nurse!",
  "whoa nelly, says Sherman, the Shark",
  "01234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
};


static WORD8 selfTestDigest[3][MD5_DIGESTSIZE] = 
{ 
  { 0x13, 0x12, 0x04, 0x84, 0x56, 0x62, 0x22, 0xdf,
    0xcf, 0xac, 0x4f, 0xd4, 0x1e, 0x78, 0x18, 0x90 },
    
  { 0x1f, 0x6a, 0x8e, 0x65, 0xba, 0x18, 0xb7, 0x74,
    0xc0, 0xc1, 0xed, 0xcb, 0xe6, 0x29, 0xb4, 0x95 },

  { 0x9c, 0xdc, 0xa7, 0xfa, 0x46, 0xc7, 0xc7, 0x1a,
    0x5c, 0xfe, 0xd3, 0xbc, 0x99, 0x9e, 0x2f, 0x91 }
};



BYTEBOOL CRYPTPAK_API MD5_SelfTest() 
{
    int nI;
    PMD5CTX pCtx;
    WORD8 actDigest[MD5_DIGESTSIZE];

    // run tests
    for (nI = 0; nI < 3; nI++) 
    {
      pCtx = MD5_Create();
      MD5_Update(pCtx, selfTestSource[nI], strlen(selfTestSource[nI]));
      MD5_Final(actDigest, pCtx);
      MD5_Destroy(pCtx);

      if (0 != memcmp(&selfTestDigest[nI][0], actDigest, MD5_DIGESTSIZE))
        return BOOL_FALSE;
    }

    // all tests passed 
    return BOOL_TRUE;
}





// basic transformation, transforms state based on block.
void _MD5_transform 
  (WORD32 state[4], 
   WORD8 block[64]) 
{

  WORD32 lA = state[0], lB = state[1], lC = state[2], lD = state[3];
  WORD32 x[16];
  
  _MD5_decode (x, block, 64);

  // round 1 
  FF ( lA, lB, lC, lD, x[ 0], S11, 0xd76aa478); // 1 
  FF ( lD, lA, lB, lC, x[ 1], S12, 0xe8c7b756); // 2 
  FF ( lC, lD, lA, lB, x[ 2], S13, 0x242070db); // 3 
  FF ( lB, lC, lD, lA, x[ 3], S14, 0xc1bdceee); // 4 
  FF ( lA, lB, lC, lD, x[ 4], S11, 0xf57c0faf); // 5 
  FF ( lD, lA, lB, lC, x[ 5], S12, 0x4787c62a); // 6 
  FF ( lC, lD, lA, lB, x[ 6], S13, 0xa8304613); // 7 
  FF ( lB, lC, lD, lA, x[ 7], S14, 0xfd469501); // 8 
  FF ( lA, lB, lC, lD, x[ 8], S11, 0x698098d8); // 9 
  FF ( lD, lA, lB, lC, x[ 9], S12, 0x8b44f7af); // 10 
  FF ( lC, lD, lA, lB, x[10], S13, 0xffff5bb1); // 11 
  FF ( lB, lC, lD, lA, x[11], S14, 0x895cd7be); // 12 
  FF ( lA, lB, lC, lD, x[12], S11, 0x6b901122); // 13 
  FF ( lD, lA, lB, lC, x[13], S12, 0xfd987193); // 14 
  FF ( lC, lD, lA, lB, x[14], S13, 0xa679438e); // 15 
  FF ( lB, lC, lD, lA, x[15], S14, 0x49b40821); // 16 

  // round 2 
  GG ( lA, lB, lC, lD, x[ 1], S21, 0xf61e2562); // 17 
  GG ( lD, lA, lB, lC, x[ 6], S22, 0xc040b340); // 18 
  GG ( lC, lD, lA, lB, x[11], S23, 0x265e5a51); // 19 
  GG ( lB, lC, lD, lA, x[ 0], S24, 0xe9b6c7aa); // 20 
  GG ( lA, lB, lC, lD, x[ 5], S21, 0xd62f105d); // 21 
  GG ( lD, lA, lB, lC, x[10], S22,  0x2441453); // 22 
  GG ( lC, lD, lA, lB, x[15], S23, 0xd8a1e681); // 23 
  GG ( lB, lC, lD, lA, x[ 4], S24, 0xe7d3fbc8); // 24 
  GG ( lA, lB, lC, lD, x[ 9], S21, 0x21e1cde6); // 25 
  GG ( lD, lA, lB, lC, x[14], S22, 0xc33707d6); // 26 
  GG ( lC, lD, lA, lB, x[ 3], S23, 0xf4d50d87); // 27 
  GG ( lB, lC, lD, lA, x[ 8], S24, 0x455a14ed); // 28 
  GG ( lA, lB, lC, lD, x[13], S21, 0xa9e3e905); // 29 
  GG ( lD, lA, lB, lC, x[ 2], S22, 0xfcefa3f8); // 30 
  GG ( lC, lD, lA, lB, x[ 7], S23, 0x676f02d9); // 31 
  GG ( lB, lC, lD, lA, x[12], S24, 0x8d2a4c8a); // 32 

  // round 3 
  HH ( lA, lB, lC, lD, x[ 5], S31, 0xfffa3942); // 33 
  HH ( lD, lA, lB, lC, x[ 8], S32, 0x8771f681); // 34 
  HH ( lC, lD, lA, lB, x[11], S33, 0x6d9d6122); // 35 
  HH ( lB, lC, lD, lA, x[14], S34, 0xfde5380c); // 36 
  HH ( lA, lB, lC, lD, x[ 1], S31, 0xa4beea44); // 37 
  HH ( lD, lA, lB, lC, x[ 4], S32, 0x4bdecfa9); // 38 
  HH ( lC, lD, lA, lB, x[ 7], S33, 0xf6bb4b60); // 39 
  HH ( lB, lC, lD, lA, x[10], S34, 0xbebfbc70); // 40 
  HH ( lA, lB, lC, lD, x[13], S31, 0x289b7ec6); // 41 
  HH ( lD, lA, lB, lC, x[ 0], S32, 0xeaa127fa); // 42 
  HH ( lC, lD, lA, lB, x[ 3], S33, 0xd4ef3085); // 43 
  HH ( lB, lC, lD, lA, x[ 6], S34,  0x4881d05); // 44 
  HH ( lA, lB, lC, lD, x[ 9], S31, 0xd9d4d039); // 45 
  HH ( lD, lA, lB, lC, x[12], S32, 0xe6db99e5); // 46 
  HH ( lC, lD, lA, lB, x[15], S33, 0x1fa27cf8); // 47 
  HH ( lB, lC, lD, lA, x[ 2], S34, 0xc4ac5665); // 48 

  // round 4 
  II ( lA, lB, lC, lD, x[ 0], S41, 0xf4292244); // 49 
  II ( lD, lA, lB, lC, x[ 7], S42, 0x432aff97); // 50 
  II ( lC, lD, lA, lB, x[14], S43, 0xab9423a7); // 51 
  II ( lB, lC, lD, lA, x[ 5], S44, 0xfc93a039); // 52 
  II ( lA, lB, lC, lD, x[12], S41, 0x655b59c3); // 53 
  II ( lD, lA, lB, lC, x[ 3], S42, 0x8f0ccc92); // 54 
  II ( lC, lD, lA, lB, x[10], S43, 0xffeff47d); // 55 
  II ( lB, lC, lD, lA, x[ 1], S44, 0x85845dd1); // 56 
  II ( lA, lB, lC, lD, x[ 8], S41, 0x6fa87e4f); // 57 
  II ( lD, lA, lB, lC, x[15], S42, 0xfe2ce6e0); // 58 
  II ( lC, lD, lA, lB, x[ 6], S43, 0xa3014314); // 59 
  II ( lB, lC, lD, lA, x[13], S44, 0x4e0811a1); // 60 
  II ( lA, lB, lC, lD, x[ 4], S41, 0xf7537e82); // 61 
  II ( lD, lA, lB, lC, x[11], S42, 0xbd3af235); // 62 
  II ( lC, lD, lA, lB, x[ 2], S43, 0x2ad7d2bb); // 63 
  II ( lB, lC, lD, lA, x[ 9], S44, 0xeb86d391); // 64 

  state[0] += lA;
  state[1] += lB;
  state[2] += lC;
  state[3] += lD;
  
  // lClear sensitive information
  memset(x, 0, 16);
}


// encodes input (WORD32) into output (WORD8), 
// assumes that lLen is a multiple of 4
void _MD5_encode 
  (WORD8* pOutput, 
   WORD32* pInput, 
   WORD32 lLen) 
{
  WORD32 lI, lJ;

  for (lI = 0, lJ = 0; lJ < lLen; lI++, lJ += 4) 
  {
    pOutput[lJ]     = (WORD8)(pInput[lI] & 0x0ff);
    pOutput[lJ + 1] = (WORD8)((pInput[lI] >> 8) & 0x0ff);
    pOutput[lJ + 2] = (WORD8)((pInput[lI] >> 16) & 0x0ff);
    pOutput[lJ + 3] = (WORD8)((pInput[lI] >> 24) & 0x0ff);
  }
}


// encodes input (WORD8) into output (WORD32),
// assumes that lLen is a multiple of 4.
void _MD5_decode 
  (WORD32* pOutput, 
   WORD8* pInput, 
   WORD32 lLen) 
{
  WORD32 lI, lJ;

  for (lI = 0, lJ = 0; lJ < lLen; lI++, lJ += 4)
    pOutput[lI] = ((WORD32)pInput[lJ]) |
                 (((WORD32)pInput[lJ + 1]) << 8) |
                 (((WORD32)pInput[lJ + 2]) << 16) |
                 (((WORD32)pInput[lJ + 3]) << 24);
}

