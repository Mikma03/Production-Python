/* This is an independent implementation of the encryption algorithm:   */
/*                                                                      */
/*         RC6 by Ron Rivest and RSA Labs                               */
/*                                                                      */
/* which is a candidate algorithm in the Advanced Encryption Standard   */
/* programme of the US National Institute of Standards and Technology.  */
/*                                                                      */
/* Copyright in this implementation is held by Dr B R Gladman but I     */
/* hereby give permission for its free direct or derivative use subject */
/* to acknowledgment of its origin and compliance with any conditions   */
/* that the originators of the algorithm place on its exploitation.     */
/*                                                                      */
/* Dr Brian Gladman (gladman@seven77.demon.co.uk) 14th January 1999     */
/*                                                                      */
/* Changed for CryptPak by Christian Thoeing <c.thoeing@web.de>         */

#include "RC6.h"

typedef struct {
  WORD32 l_key[44];
  WORD32 cbc_iv[4];
} RC6CTX;

#define rotr(x,n)   (((x) >> ((int)(n))) | ((x) << (32 - (int)(n))))
#define rotl(x,n)   (((x) << ((int)(n))) | ((x) >> (32 - (int)(n))))

#define f_rnd(i,a,b,c,d)                    \
        u = rotl(d * (d + d + 1), 5);       \
        t = rotl(b * (b + b + 1), 5);       \
        a = rotl(a ^ t, u) + l_key[i];      \
        c = rotl(c ^ u, t) + l_key[i + 1]

#define i_rnd(i,a,b,c,d)                    \
	u = rotl(d * (d + d + 1), 5);       \
        t = rotl(b * (b + b + 1), 5);       \
        c = rotr(c - l_key[i + 1], t) ^ u;  \
        a = rotr(a - l_key[i], u) ^ t

void rc6SetKey(RC6CTX* pCtx,
               const WORD8* pKey,
               WORD32 lKeyLen)

{
  WORD32 i, j, k, a, b, l[8], t;
  WORD32* l_key = pCtx->l_key;

  l_key[0] = 0xb7e15163;
  for (k = 1; k < 44; ++k)
    l_key[k] = l_key[k - 1] + 0x9e3779b9;

  for (k = 0; k < 8; ++k)
    l[k] = 0;
  for (k = 0; k < lKeyLen; ++k)
    l[k/4] |= pKey[k] << ((k%4)*8);

  t = ((lKeyLen + 3) / 4) - 1; // t = (key_len / 32);
  a = b = i = j = 0;

  for (k = 0; k < 132; ++k)
  {
    a = rotl(l_key[i] + a + b, 3); b += a;
    b = rotl(l[j] + b, b);
    l_key[i] = a; l[j] = b;
    i = (i == 43 ? 0 : i + 1); // i = (i + 1) % 44;
    j = (j == t ? 0 : j + 1);  // j = (j + 1) % t;
  }

  // wipe sensitive data
  for (k = 0; k < 8; ++k)
    l[k] = 0;
}

void rc6Encrypt(RC6CTX* pCtx,
                const WORD32* pInBlock,
                WORD32* pOutBlock)
{
  WORD32 a, b, c, d, t, u;
  WORD32* l_key = pCtx->l_key;

  a = pInBlock[0];
  b = pInBlock[1] + l_key[0];
  c = pInBlock[2];
  d = pInBlock[3] + l_key[1];

  // perform 20 rounds of encryption
  f_rnd( 2,a,b,c,d); f_rnd( 4,b,c,d,a);
  f_rnd( 6,c,d,a,b); f_rnd( 8,d,a,b,c);
  f_rnd(10,a,b,c,d); f_rnd(12,b,c,d,a);
  f_rnd(14,c,d,a,b); f_rnd(16,d,a,b,c);
  f_rnd(18,a,b,c,d); f_rnd(20,b,c,d,a);
  f_rnd(22,c,d,a,b); f_rnd(24,d,a,b,c);
  f_rnd(26,a,b,c,d); f_rnd(28,b,c,d,a);
  f_rnd(30,c,d,a,b); f_rnd(32,d,a,b,c);
  f_rnd(34,a,b,c,d); f_rnd(36,b,c,d,a);
  f_rnd(38,c,d,a,b); f_rnd(40,d,a,b,c);

  pOutBlock[0] = a + l_key[42];
  pOutBlock[1] = b;
  pOutBlock[2] = c + l_key[43];
  pOutBlock[3] = d;
}

void rc6Decrypt(RC6CTX* pCtx,
                const WORD32* pIn,
                WORD32* pOut)
{
  WORD32 a, b, c, d, t, u;
  WORD32* l_key = pCtx->l_key;

  a = pIn[0] - l_key[42];
  b = pIn[1];
  c = pIn[2] - l_key[43];
  d = pIn[3];

  // perform 20 rounds of decryption
  i_rnd(40,d,a,b,c); i_rnd(38,c,d,a,b);
  i_rnd(36,b,c,d,a); i_rnd(34,a,b,c,d);
  i_rnd(32,d,a,b,c); i_rnd(30,c,d,a,b);
  i_rnd(28,b,c,d,a); i_rnd(26,a,b,c,d);
  i_rnd(24,d,a,b,c); i_rnd(22,c,d,a,b);
  i_rnd(20,b,c,d,a); i_rnd(18,a,b,c,d);
  i_rnd(16,d,a,b,c); i_rnd(14,c,d,a,b);
  i_rnd(12,b,c,d,a); i_rnd(10,a,b,c,d);
  i_rnd( 8,d,a,b,c); i_rnd( 6,c,d,a,b);
  i_rnd( 4,b,c,d,a); i_rnd( 2,a,b,c,d);

  pOut[0] = a;
  pOut[1] = b - l_key[0];
  pOut[2] = c;
  pOut[3] = d - l_key[1];
}

WORD32 RC6_GetCipherInfo(CIPHERINFOBLOCK* pInfo)
{
  WORD32 lI;
  WORD8* pSrc;
  WORD8* pDst;
  CIPHERINFOBLOCK tmpInfo;

  tmpInfo.lSizeOf = pInfo->lSizeOf;
  tmpInfo.lBlockSize = RC6_BLOCKSIZE;
  tmpInfo.lKeySize = RC6_KEYSIZE;
  tmpInfo.blOwnHasher = BOOL_FALSE;
  tmpInfo.lInitDataSize = RC6_BLOCKSIZE;
  tmpInfo.lContextSize = sizeof(RC6CTX);
  tmpInfo.bCipherIs = CIPHER_IS_BLOCKLINK;

  // copy as many bytes of the information block as possible
  pSrc = (WORD8*) &tmpInfo;
  pDst = (WORD8*) pInfo;
  for (lI = 0; lI < tmpInfo.lSizeOf; lI++)
    *pDst++ = *pSrc++;
  return CIPHER_ERROR_NOERROR;
}

WORD32 RC6_SelfTest(void* pTestContext)
{
  /*
   * NOTE: The following test vectors are NOT official test vectors.
   * This implementation was compared with the Gladman implementation
   * and the code available in the DelphiCrypt library; they all deliver the
   * same outputs. Sorry, but I could not find the official implementation
   * written by the authors of RC6.
   */

  const WORD8 testkey[32] =
    { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
      21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31 };

  const WORD32 plaintext[4] =
    { 0x01234567, 0xABCDEF01, 0xA0B1C2D3, 0xE4F58899 };

  const WORD32 cipher_must[4] =
    { 0x828294E0, 0x5A153FE7, 0x15B51F25, 0xBD6BE5B6 };

  WORD32 testbuf[4];
  RC6CTX* pCtx = (RC6CTX*) pTestContext;
  int nI;

  // initialize the cipher
  rc6SetKey(pCtx, testkey, 32);

  // encrypt the test vector
  rc6Encrypt(pCtx, plaintext, testbuf);

  // did it work correctly?
  for (nI = 0; nI < 4; nI++)
  {
    if (testbuf[nI] != cipher_must[nI])
      return CIPHER_ERROR_INVALID;
  }

  // test the decryption
  rc6Decrypt(pCtx, testbuf, testbuf);

  for (nI = 0; nI < 4; nI++)
  {
    if (testbuf[nI] != plaintext[nI])
      return CIPHER_ERROR_INVALID;
  }

  return CIPHER_ERROR_NOERROR;
}

WORD32 RC6_CreateWorkContext(void* pContext,
                             const WORD8* pKey,
                             WORD32 lKeyLen,
                             WORD32 lMode,
                             void* pInitData,
                             Cipher_RandomGenerator GetRndBytes,
                             const void* pRandGenData)
{
  RC6CTX* pCtx = (RC6CTX*) pContext;
  WORD32* pCBCIV;

  // do the key setup
  rc6SetKey(pCtx, pKey, lKeyLen);

  pCBCIV = (WORD32*) pInitData;
  if (lMode == CIPHER_MODE_ENCRYPT)
    GetRndBytes((WORD8*) pCBCIV, RC6_BLOCKSIZE, pRandGenData);

  // set the CBC IV
  pCtx->cbc_iv[0] = pCBCIV[0];
  pCtx->cbc_iv[1] = pCBCIV[1];
  pCtx->cbc_iv[2] = pCBCIV[2];
  pCtx->cbc_iv[3] = pCBCIV[3];

  return CIPHER_ERROR_NOERROR;
}

void RC6_ResetWorkContext(void*  pContext,
                          WORD32 lMode,
                          void*  pInitData,
                          Cipher_RandomGenerator GetRndBytes,
                          const void* pRandGenData)
{
  RC6CTX* pCtx = (RC6CTX*) pContext;
  WORD32* pCBCIV = (WORD32*) pInitData;

  if (lMode == CIPHER_MODE_ENCRYPT)
    GetRndBytes((WORD8*) pCBCIV, RC6_BLOCKSIZE, pRandGenData);

  // set the CBC IV
  pCtx->cbc_iv[0] = pCBCIV[0];
  pCtx->cbc_iv[1] = pCBCIV[1];
  pCtx->cbc_iv[2] = pCBCIV[2];
  pCtx->cbc_iv[3] = pCBCIV[3];
}

WORD32 RC6_DestroyWorkContext(void* pContext)
{
  WORD32 lI;
  WORD8* pCtxBuf = (WORD8*) pContext;

  for (lI = 0; lI < sizeof(RC6CTX); lI++)
    pCtxBuf[lI] = 0x00;

  return CIPHER_ERROR_NOERROR;
}

void RC6_EncryptBuffer(void* pContext,
                       const void* pSource,
                       void* pTarget,
                       WORD32 lNumOfBytes)
{
  WORD32 lNumOfBlocks;
  WORD32* pInBuf = (WORD32*) pSource;
  WORD32* pOutBuf = (WORD32*) pTarget;
  RC6CTX* pCtx = (RC6CTX*) pContext;

  lNumOfBlocks = lNumOfBytes / RC6_BLOCKSIZE;

  while (lNumOfBlocks--)
  {
    pOutBuf[0] = pInBuf[0] ^ pCtx->cbc_iv[0];
    pOutBuf[1] = pInBuf[1] ^ pCtx->cbc_iv[1];
    pOutBuf[2] = pInBuf[2] ^ pCtx->cbc_iv[2];
    pOutBuf[3] = pInBuf[3] ^ pCtx->cbc_iv[3];

    // encrypt the buffer
    rc6Encrypt(pCtx, pOutBuf, pOutBuf);

    // set the new IV
    pCtx->cbc_iv[0] = pOutBuf[0];
    pCtx->cbc_iv[1] = pOutBuf[1];
    pCtx->cbc_iv[2] = pOutBuf[2];
    pCtx->cbc_iv[3] = pOutBuf[3];

    // increase the pointers
    pInBuf  += RC6_BLOCKSIZE / 4;
    pOutBuf += RC6_BLOCKSIZE / 4;
  }
}

void RC6_DecryptBuffer(void* pContext,
                       const void* pSource,
                       void* pTarget,
                       WORD32 lNumOfBytes,
                       const void* pPreviousBlock)
{
  WORD32 lNumOfBlocks;
  WORD32* pInBuf = (WORD32*) pSource;
  WORD32* pOutBuf = (WORD32*) pTarget;
  WORD32* pPrevBlock = (WORD32*) pPreviousBlock;
  WORD32 save_cbc_iv[4];
  RC6CTX* pCtx = (RC6CTX*) pContext;

  lNumOfBlocks = lNumOfBytes / RC6_BLOCKSIZE;

  // load a new IV, if necessary
  if (pPreviousBlock != CIPHER_NULL)
  {
    pCtx->cbc_iv[0] = pPrevBlock[0];
    pCtx->cbc_iv[1] = pPrevBlock[1];
    pCtx->cbc_iv[2] = pPrevBlock[2];
    pCtx->cbc_iv[3] = pPrevBlock[3];
  }

  while (lNumOfBlocks--)
  {
    // save the current IV
    save_cbc_iv[0] = pInBuf[0];
    save_cbc_iv[1] = pInBuf[1];
    save_cbc_iv[2] = pInBuf[2];
    save_cbc_iv[3] = pInBuf[3];

    // now decrypt the block
    rc6Decrypt(pCtx, pInBuf, pOutBuf);

    // dechain the block
    pOutBuf[0] ^= pCtx->cbc_iv[0];
    pOutBuf[1] ^= pCtx->cbc_iv[1];
    pOutBuf[2] ^= pCtx->cbc_iv[2];
    pOutBuf[3] ^= pCtx->cbc_iv[3];

    // set the new IV
    pCtx->cbc_iv[0] = save_cbc_iv[0];
    pCtx->cbc_iv[1] = save_cbc_iv[1];
    pCtx->cbc_iv[2] = save_cbc_iv[2];
    pCtx->cbc_iv[3] = save_cbc_iv[3];

    // increase the pointers
    pInBuf  += RC6_BLOCKSIZE / 4;
    pOutBuf += RC6_BLOCKSIZE / 4;
  }
}
