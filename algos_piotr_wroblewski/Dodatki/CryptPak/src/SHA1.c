

#include "cpkernel.h"
#include "SHA1.h"

#include <stdio.h>

#include <stdlib.h>
#include <memory.h>
#include <string.h>


// macros for encoding/decoding in the correct byte order
#define mgetBWORD32(memPtr)                                             \
            ( ((WORD32) memPtr[0] << 24) | ((WORD32) memPtr[1] << 16) | \
            ((WORD32) memPtr[2] << 8) | (WORD32) memPtr[3]);            \
            memPtr += 4

#define copyToBWORD32(dest,src,count)                           \
                    {                                           \
                    WORD32 *destPtr = (WORD32*) dest;           \
                    WORD8* srcPtr = src;                        \
                    int nI;                                     \
                    for (nI = 0; nI < (count >> 2); nI++)       \
                        {                                       \
                          destPtr[nI] = mgetBWORD32(srcPtr);    \
                        }                                       \
                    }



// the SHA-1 f()-functions (optimized version)
#define f1(x,y,z)   ( z ^ ( x & ( y ^ z ) ) )       // rounds  0-19 
#define f2(x,y,z)   ( x ^ y ^ z )                   // rounds 20-39 
#define f3(x,y,z)   ( x & y ) + ( z & ( x ^ y ) )   // rounds 40-59 
#define f4(x,y,z)   ( x ^ y ^ z )                   // rounds 60-79 

// SHA-1 mysterious constants 
#define K1  0x5A827999UL                            // rounds  0-19 
#define K2  0x6ED9EBA1UL                            // rounds 20-39 
#define K3  0x8F1BBCDCUL                            // rounds 40-59 
#define K4  0xCA62C1D6UL                            // rounds 60-79 

// SHA-1 init. values
#define H0INIT  0x67452301UL
#define H1INIT  0xEFCDAB89UL
#define H2INIT  0x98BADCFEUL
#define H3INIT  0x10325476UL
#define H4INIT  0xC3D2E1F0UL


// 32bit rotate left
#define ROTL(n, X)  (((X) << n) | ( (X) >> (32 - n)))

// for correct 32bit word extracting
#define MASK32(x)   ((x) & 0xffffffff)

// init. expanding function
#define expand(W,i) ( W[i & 15] = MASK32(ROTL(1, (W[i & 15] ^ W[i - 14 & 15] ^\
                                         W[i - 8 & 15] ^ W[i - 3 & 15]))) )

// prototype SHA-1 sub-round
#define subRound(a, b, c, d, e, f, k, data)             \
    e = MASK32( e + ROTL(5, a) + f(b, c, d) + k + data);\
    b = MASK32( ROTL(30, b) )



// the SHA-1 transformation
void _SHA1_transform
  (WORD32 *digest, 
   WORD32 *data) 
{
    WORD32 lA, lB, lC, lD, lE;  // local variables 
    WORD32 edata[16];           // expanded data 
    int nI;

    // set up first buffer and local data buffer 
    lA = digest[0];
    lB = digest[1];
    lC = digest[2];
    lD = digest[3];
    lE = digest[4];
    for (nI = 0; nI < 16; nI++) edata[nI] = data[nI];

    // heavy mangling, in 4 subrounds of 20 interations each...

    // round #1 
    subRound(lA, lB, lC, lD, lE, f1, K1, edata[0]);
    subRound(lE, lA, lB, lC, lD, f1, K1, edata[1]);
    subRound(lD, lE, lA, lB, lC, f1, K1, edata[2]);
    subRound(lC, lD, lE, lA, lB, f1, K1, edata[3]);
    subRound(lB, lC, lD, lE, lA, f1, K1, edata[4]);
    subRound(lA, lB, lC, lD, lE, f1, K1, edata[5]);
    subRound(lE, lA, lB, lC, lD, f1, K1, edata[6]);
    subRound(lD, lE, lA, lB, lC, f1, K1, edata[7]);
    subRound(lC, lD, lE, lA, lB, f1, K1, edata[8]);
    subRound(lB, lC, lD, lE, lA, f1, K1, edata[9]);
    subRound(lA, lB, lC, lD, lE, f1, K1, edata[10]);
    subRound(lE, lA, lB, lC, lD, f1, K1, edata[11]);
    subRound(lD, lE, lA, lB, lC, f1, K1, edata[12]);
    subRound(lC, lD, lE, lA, lB, f1, K1, edata[13]);
    subRound(lB, lC, lD, lE, lA, f1, K1, edata[14]);
    subRound(lA, lB, lC, lD, lE, f1, K1, edata[15]);
    subRound(lE, lA, lB, lC, lD, f1, K1, expand(edata, 16));
    subRound(lD, lE, lA, lB, lC, f1, K1, expand(edata, 17));
    subRound(lC, lD, lE, lA, lB, f1, K1, expand(edata, 18));
    subRound(lB, lC, lD, lE, lA, f1, K1, expand(edata, 19));
    // round #2 
    subRound(lA, lB, lC, lD, lE, f2, K2, expand(edata, 20));
    subRound(lE, lA, lB, lC, lD, f2, K2, expand(edata, 21));
    subRound(lD, lE, lA, lB, lC, f2, K2, expand(edata, 22));
    subRound(lC, lD, lE, lA, lB, f2, K2, expand(edata, 23));
    subRound(lB, lC, lD, lE, lA, f2, K2, expand(edata, 24));
    subRound(lA, lB, lC, lD, lE, f2, K2, expand(edata, 25));
    subRound(lE, lA, lB, lC, lD, f2, K2, expand(edata, 26));
    subRound(lD, lE, lA, lB, lC, f2, K2, expand(edata, 27));
    subRound(lC, lD, lE, lA, lB, f2, K2, expand(edata, 28));
    subRound(lB, lC, lD, lE, lA, f2, K2, expand(edata, 29));
    subRound(lA, lB, lC, lD, lE, f2, K2, expand(edata, 30));
    subRound(lE, lA, lB, lC, lD, f2, K2, expand(edata, 31));
    subRound(lD, lE, lA, lB, lC, f2, K2, expand(edata, 32));
    subRound(lC, lD, lE, lA, lB, f2, K2, expand(edata, 33));
    subRound(lB, lC, lD, lE, lA, f2, K2, expand(edata, 34));
    subRound(lA, lB, lC, lD, lE, f2, K2, expand(edata, 35));
    subRound(lE, lA, lB, lC, lD, f2, K2, expand(edata, 36));
    subRound(lD, lE, lA, lB, lC, f2, K2, expand(edata, 37));
    subRound(lC, lD, lE, lA, lB, f2, K2, expand(edata, 38));
    subRound(lB, lC, lD, lE, lA, f2, K2, expand(edata, 39));
    // round #3 
    subRound(lA, lB, lC, lD, lE, f3, K3, expand(edata, 40));
    subRound(lE, lA, lB, lC, lD, f3, K3, expand(edata, 41));
    subRound(lD, lE, lA, lB, lC, f3, K3, expand(edata, 42));
    subRound(lC, lD, lE, lA, lB, f3, K3, expand(edata, 43));
    subRound(lB, lC, lD, lE, lA, f3, K3, expand(edata, 44));
    subRound(lA, lB, lC, lD, lE, f3, K3, expand(edata, 45));
    subRound(lE, lA, lB, lC, lD, f3, K3, expand(edata, 46));
    subRound(lD, lE, lA, lB, lC, f3, K3, expand(edata, 47));
    subRound(lC, lD, lE, lA, lB, f3, K3, expand(edata, 48));
    subRound(lB, lC, lD, lE, lA, f3, K3, expand(edata, 49));
    subRound(lA, lB, lC, lD, lE, f3, K3, expand(edata, 50));
    subRound(lE, lA, lB, lC, lD, f3, K3, expand(edata, 51));
    subRound(lD, lE, lA, lB, lC, f3, K3, expand(edata, 52));
    subRound(lC, lD, lE, lA, lB, f3, K3, expand(edata, 53));
    subRound(lB, lC, lD, lE, lA, f3, K3, expand(edata, 54));
    subRound(lA, lB, lC, lD, lE, f3, K3, expand(edata, 55));
    subRound(lE, lA, lB, lC, lD, f3, K3, expand(edata, 56));
    subRound(lD, lE, lA, lB, lC, f3, K3, expand(edata, 57));
    subRound(lC, lD, lE, lA, lB, f3, K3, expand(edata, 58));
    subRound(lB, lC, lD, lE, lA, f3, K3, expand(edata, 59));
    // round #4 
    subRound(lA, lB, lC, lD, lE, f4, K4, expand(edata, 60));
    subRound(lE, lA, lB, lC, lD, f4, K4, expand(edata, 61));
    subRound(lD, lE, lA, lB, lC, f4, K4, expand(edata, 62));
    subRound(lC, lD, lE, lA, lB, f4, K4, expand(edata, 63));
    subRound(lB, lC, lD, lE, lA, f4, K4, expand(edata, 64));
    subRound(lA, lB, lC, lD, lE, f4, K4, expand(edata, 65));
    subRound(lE, lA, lB, lC, lD, f4, K4, expand(edata, 66));
    subRound(lD, lE, lA, lB, lC, f4, K4, expand(edata, 67));
    subRound(lC, lD, lE, lA, lB, f4, K4, expand(edata, 68));
    subRound(lB, lC, lD, lE, lA, f4, K4, expand(edata, 69));
    subRound(lA, lB, lC, lD, lE, f4, K4, expand(edata, 70));
    subRound(lE, lA, lB, lC, lD, f4, K4, expand(edata, 71));
    subRound(lD, lE, lA, lB, lC, f4, K4, expand(edata, 72));
    subRound(lC, lD, lE, lA, lB, f4, K4, expand(edata, 73));
    subRound(lB, lC, lD, lE, lA, f4, K4, expand(edata, 74));
    subRound(lA, lB, lC, lD, lE, f4, K4, expand(edata, 75));
    subRound(lE, lA, lB, lC, lD, f4, K4, expand(edata, 76));
    subRound(lD, lE, lA, lB, lC, f4, K4, expand(edata, 77));
    subRound(lC, lD, lE, lA, lB, f4, K4, expand(edata, 78));
    subRound(lB, lC, lD, lE, lA, f4, K4, expand(edata, 79));

    // build message digest 
    digest[0] = MASK32(digest[0] + lA);
    digest[1] = MASK32(digest[1] + lB);
    digest[2] = MASK32(digest[2] + lC);
    digest[3] = MASK32(digest[3] + lD);
    digest[4] = MASK32(digest[4] + lE);
}



PSHA1CTX CRYPTPAK_API SHA1_Create() 
{
    // create the context memory
    PSHA1CTX pCtx = (PSHA1CTX) malloc(sizeof(SHA1CTX));

    // init. 
    SHA1_Initialize(pCtx);

    return pCtx;
}


void CRYPTPAK_API SHA1_Initialize
  (PSHA1CTX pCtx) 
{
    // init the digest
    SHA1_Reset(pCtx);

    // set the bit counter to zero
    pCtx->lCountLo = pCtx->lCountHi = 0;
}



void CRYPTPAK_API SHA1_Reset
  (PSHA1CTX pCtx) 
{
    // to be sure clear all fields
    memset(pCtx, 0, sizeof(SHA1CTX));

    // init the digest
    pCtx->digest[0] = H0INIT;
    pCtx->digest[1] = H1INIT;
    pCtx->digest[2] = H2INIT;
    pCtx->digest[3] = H3INIT;
    pCtx->digest[4] = H4INIT;
}


void CRYPTPAK_API SHA1_Destroy
(PSHA1CTX pCtx) 
{
  memset(pCtx, 0, sizeof(SHA1CTX));
  free(pCtx);
}



void CRYPTPAK_API SHA1_Update
  (PSHA1CTX pCtx, 
   const void* pData, 
   WORD32 lNumOfBytes) 
{
    int nDataCount;
    WORD32 lTemp;
    WORD8* pBuffer = (WORD8*) pData;

    // update the bit counter
    lTemp = pCtx->lCountLo;
    if ((pCtx->lCountLo = lTemp + (lNumOfBytes << 3 )) < lTemp)
      pCtx->lCountHi++; // (carry from low to high)

    pCtx->lCountHi += lNumOfBytes >> 29;

    // get the number of cached bytes 
    nDataCount = (int) (lTemp >> 3 ) & 0x03f;

    // handle any leading odd-sized chunks 
    if (nDataCount) 
    {
      WORD8* pBP = pCtx->dataBuffer + nDataCount;
      nDataCount = SHA1_DATASIZE - nDataCount;

      if ((int) lNumOfBytes < nDataCount) 
      {
        memcpy(pBP, 
               pBuffer, 
               lNumOfBytes);
        return;
      }
      memcpy(pBP, 
             pBuffer, 
             nDataCount);

      copyToBWORD32(pCtx->data, 
                    pCtx->dataBuffer, 
                    SHA1_DATASIZE);

      _SHA1_transform(pCtx->digest, 
                      pCtx->data);

      pBuffer += nDataCount;
      lNumOfBytes -= nDataCount;
    }

    // process data in SHA1_DATASIZE chunks 
    while (lNumOfBytes >= SHA1_DATASIZE)    
    {
      memcpy(pCtx->dataBuffer, 
             pBuffer, 
             SHA1_DATASIZE);
      copyToBWORD32(pCtx->data, 
                    pCtx->dataBuffer, 
                    SHA1_DATASIZE);
      _SHA1_transform(pCtx->digest,  
                      pCtx->data);
      pBuffer += SHA1_DATASIZE;
      lNumOfBytes -= SHA1_DATASIZE;
    }

    // handle any remaining bytes of data. 
    memcpy(pCtx->dataBuffer, 
           pBuffer, 
           lNumOfBytes);
}



void CRYPTPAK_API SHA1_Final
  (WORD8* pDigest, 
   PSHA1CTX pCtx ) 
{
    WORD32 lTemp;
    int nCount, nI, nJ;
    WORD8* pData;

    // compute number of bytes mod 64 
    nCount = (int) pCtx->lCountLo;
    nCount = (nCount >> 3 ) & 0x03f;

    // set the first char of padding to 0x80, this is safe since there is
    // always at least one byte free 
    pData = pCtx->dataBuffer + nCount;
    *pData++ = 0x80;

    // bytes of padding needed to make 64 bytes 
    nCount = SHA1_DATASIZE - 1 - nCount;

    // pad out to 56 mod 64 
    if (nCount < 8) 
    {
      // two lots of padding: pad the first block to 64 bytes 
      memset(pData, 
             0,
             nCount);
      copyToBWORD32(pCtx->data, 
                    pCtx->dataBuffer, 
                    SHA1_DATASIZE);
      _SHA1_transform(pCtx->digest, 
                      pCtx->data );

      // now fill the next block with 56 bytes 
      memset(pCtx->dataBuffer, 
             0,
             SHA1_DATASIZE - 8);
    }
    else 
    {
      // pad block to 56 bytes 
      memset(pData, 0, nCount - 8);
    }
    copyToBWORD32(pCtx->data, 
                  pCtx->dataBuffer, 
                  SHA1_DATASIZE);

    // append length in bits and transform 
    pCtx->data[14] = pCtx->lCountHi;
    pCtx->data[15] = pCtx->lCountLo;

    _SHA1_transform(pCtx->digest, pCtx->data);

    // copy the digest
    for (nI = 0, nJ = 0; nI < 5; nI++, nJ += 4) 
    {
      lTemp = pCtx->digest[nI];
      pDigest[nJ]     = (WORD8)((lTemp >> 24) & 0x0ff);
      pDigest[nJ + 1] = (WORD8)((lTemp >> 16) & 0x0ff);
      pDigest[nJ + 2] = (WORD8)((lTemp >> 8) & 0x0ff);
      pDigest[nJ + 3] = (WORD8)(lTemp & 0x0ff);
    }

    // clear the context
    memset(pCtx, 0, sizeof(SHA1CTX));

    // over and out
    pCtx->blDone = BOOL_TRUE;
}


// the selftest strings and digests
static char* selfTestSource[3] = 
{
  "abc",
  "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",
  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
};


static WORD8 selfTestDigest[3][SHA1_DIGESTSIZE] = 
{
  { 0xA9, 0x99, 0x3E, 0x36, 0x47, 0x06, 0x81, 0x6A, 0xBA, 0x3E, 0x25, 0x71, 0x78, 0x50, 0xC2, 0x6C, 0x9C, 0xD0, 0xD8, 0x9D },
  { 0x84, 0x98, 0x3E, 0x44, 0x1C, 0x3B, 0xD2, 0x6E, 0xBA, 0xAE, 0x4A, 0xA1, 0xF9, 0x51, 0x29, 0xE5, 0xE5, 0x46, 0x70, 0xF1 },
  { 0x00, 0x98, 0xBA, 0x82, 0x4B, 0x5C, 0x16, 0x42, 0x7B, 0xD7, 0xA1, 0x12, 0x2A, 0x5A, 0x44, 0x2A, 0x25, 0xEC, 0x64, 0x4D }
};



BYTEBOOL CRYPTPAK_API SHA1_SelfTest() 
{
    int nI, nJ;	//////!!!!
    PSHA1CTX pCtx;
    WORD8 actDigest[SHA1_DIGESTSIZE];

    // run tests
    for (nI = 0; nI < 3; nI++)
    {
      pCtx = SHA1_Create();

      SHA1_Update(pCtx, 
                  selfTestSource[nI], 
                  strlen(selfTestSource[nI]));

      SHA1_Final(actDigest, pCtx);

      SHA1_Destroy(pCtx);

      if (0 != memcmp(&selfTestDigest[nI], 
                      actDigest, 
                      SHA1_DIGESTSIZE))
      {                      
        return BOOL_FALSE;
      }   
    }

    // all tests passed
    return BOOL_TRUE;
}
