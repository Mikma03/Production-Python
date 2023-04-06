/* This is an independent implementation of the encryption algorithm:	*/
/*									*/
/*                 RIJNDAEL by Joan Daemen and Vincent Rijmen           */
/*                                                                      */
/* which was selected as the Advanced Encryption Standard by the US     */
/* National Institute of Standards (NIST)                               */
/*                                                                      */
/* Copyright in this implementation is held by Dr B R Gladman but I 	*/
/* hereby give permission for its free direct or derivative use subject */
/* to acknowledgment of its origin and compliance with any conditions	*/
/* that the originators of the algorithm place on its exploitation. 	*/
/*                                                                      */
/* Dr Brian Gladman (gladman@seven77.demon.co.uk) 14th January 1999 	*/
/*                                                                      */
/* Modified for CryptPak by Christian Thoeing <c.thoeing@web.de>        */
/* Some parts of this implementation are taken from Wei Dai's           */
/* rijndael.cpp (see Crypto++ library)                                  */

#include "Rijndael.h"
#include "RijndaelBoxes.h"

typedef struct {
  WORD32 key[(RIJNDAEL_KEYSIZE / 4) * 5 + 24];
  WORD32 cbc_iv[4];
} RIJNDAELCTX;

#define rotr(x,n)   (((x) >> ((int)(n))) | ((x) << (32 - (int)(n))))
#define rotl(x,n)   (((x) << ((int)(n))) | ((x) >> (32 - (int)(n))))

#define ff_mult(a,b) (a && b ? pow_tab[(log_tab[a] + log_tab[b]) % 255] : 0)

#define byte(x,n)   ((WORD8)((x) >> (8 * (n))))

#define ls_box(x)                            \
    ((WORD32)sbx_tab[byte(x, 0)] <<  0) ^    \
    ((WORD32)sbx_tab[byte(x, 1)] <<  8) ^    \
    ((WORD32)sbx_tab[byte(x, 2)] << 16) ^    \
    ((WORD32)sbx_tab[byte(x, 3)] << 24)

#define star_x(x) (((x) & 0x7f7f7f7f) << 1) ^ ((((x) & 0x80808080) >> 7) * 0x1b)

#define imix_col(y,x)       \
    u   = star_x(x);        \
    v   = star_x(u);        \
    w   = star_x(v);        \
    t   = w ^ (x);          \
   (y)  = u ^ v ^ w;        \
   (y) ^= rotr(u ^ t,  8) ^ \
          rotr(v ^ t, 16) ^ \
          rotr(t,24)

void rijndaelSetKey(RIJNDAELCTX* pCtx,
                    const WORD8* userKey,
                    WORD32 lKeyLen,
                    WORD32 lMode)
{
  WORD32 t;
  WORD32* key = pCtx->key;
  int i;

  for (i = 0; i < RIJNDAEL_KEYSIZE / 4; i++)
    key[i] = 0;

  for (i = 0; i < RIJNDAEL_KEYSIZE; i++)
    key[i/4] |= userKey[i%lKeyLen] << ((i%4)*8);

  t = key[7];

  // we use 256-bit Rijndael
  for (i = 0; i < 7; i++)
  {
    t = rotr(t,  8);
    t = ls_box(t) ^ rco_tab[i];
    key[8 * i + 8] = t ^= key[8 * i];
    key[8 * i + 9] = t ^= key[8 * i + 1];
    key[8 * i + 10] = t ^= key[8 * i + 2];
    key[8 * i + 11] = t ^= key[8 * i + 3];
    key[8 * i + 12] = t = key[8 * i + 4] ^ ls_box(t);
    key[8 * i + 13] = t ^= key[8 * i + 5];
    key[8 * i + 14] = t ^= key[8 * i + 6];
    key[8 * i + 15] = t ^= key[8 * i + 7];
  }

  if (lMode == CIPHER_MODE_DECRYPT)
  {
    WORD32 t, u, v, w;

    for (i = 4; i < RIJNDAEL_KEYSIZE + 24; i++)
    {
      imix_col(key[i], key[i]);
    }
  }
}

#define f_rn(bo, bi, n, k)                          \
    bo[n] =  ft_tab[0][byte(bi[n],0)] ^             \
             ft_tab[1][byte(bi[(n + 1) & 3],1)] ^   \
             ft_tab[2][byte(bi[(n + 2) & 3],2)] ^   \
             ft_tab[3][byte(bi[(n + 3) & 3],3)] ^ *(k + n)

#define f_rl(bo, bi, n, k)                                      \
    bo[n] = (WORD32)sbx_tab[byte(bi[n],0)] ^                    \
        rotl(((WORD32)sbx_tab[byte(bi[(n + 1) & 3],1)]),  8) ^  \
        rotl(((WORD32)sbx_tab[byte(bi[(n + 2) & 3],2)]), 16) ^  \
        rotl(((WORD32)sbx_tab[byte(bi[(n + 3) & 3],3)]), 24) ^ *(k + n)

#define f_nround(bo, bi, k) \
	f_rn(bo, bi, 0, k); 	\
	f_rn(bo, bi, 1, k); 	\
	f_rn(bo, bi, 2, k); 	\
	f_rn(bo, bi, 3, k); 	\
	k += 4

#define f_lround(bo, bi, k) \
	f_rl(bo, bi, 0, k); 	\
	f_rl(bo, bi, 1, k); 	\
	f_rl(bo, bi, 2, k); 	\
	f_rl(bo, bi, 3, k)

void rijndaelEncrypt(RIJNDAELCTX* pCtx,
                     const WORD32* pInBlock,
                     WORD32* pOutBlock)
{
  WORD32 b0[4], b1[4];
  WORD32* kp = pCtx->key;

  b0[0] = pInBlock[0] ^ *kp++;
  b0[1] = pInBlock[1] ^ *kp++;
  b0[2] = pInBlock[2] ^ *kp++;
  b0[3] = pInBlock[3] ^ *kp++;

  f_nround(b1, b0, kp); f_nround(b0, b1, kp);
  f_nround(b1, b0, kp); f_nround(b0, b1, kp);
  f_nround(b1, b0, kp); f_nround(b0, b1, kp);
  f_nround(b1, b0, kp); f_nround(b0, b1, kp);
  f_nround(b1, b0, kp); f_nround(b0, b1, kp);
  f_nround(b1, b0, kp); f_nround(b0, b1, kp);
  f_nround(b1, b0, kp); f_lround(b0, b1, kp);

  pOutBlock[0] = b0[0];
  pOutBlock[1] = b0[1];
  pOutBlock[2] = b0[2];
  pOutBlock[3] = b0[3];
}

#define i_rn(bo, bi, n, k)                          \
    bo[n] =  it_tab[0][byte(bi[n],0)] ^             \
             it_tab[1][byte(bi[(n + 3) & 3],1)] ^   \
             it_tab[2][byte(bi[(n + 2) & 3],2)] ^   \
             it_tab[3][byte(bi[(n + 1) & 3],3)] ^ *(k + n)

#define i_rl(bo, bi, n, k)                                      \
    bo[n] = (WORD32)isb_tab[byte(bi[n],0)] ^                    \
        rotl(((WORD32)isb_tab[byte(bi[(n + 3) & 3],1)]),  8) ^  \
        rotl(((WORD32)isb_tab[byte(bi[(n + 2) & 3],2)]), 16) ^  \
        rotl(((WORD32)isb_tab[byte(bi[(n + 1) & 3],3)]), 24) ^ *(k + n)

#define i_nround(bo, bi, k) \
	i_rn(bo, bi, 0, k); 	\
	i_rn(bo, bi, 1, k); 	\
	i_rn(bo, bi, 2, k); 	\
	i_rn(bo, bi, 3, k); 	\
	k -= 4

#define i_lround(bo, bi, k) \
	i_rl(bo, bi, 0, k); 	\
	i_rl(bo, bi, 1, k); 	\
	i_rl(bo, bi, 2, k); 	\
	i_rl(bo, bi, 3, k)

void rijndaelDecrypt(RIJNDAELCTX* pCtx,
                     const WORD32* pInBlock,
                     WORD32* pOutBlock)
{
  WORD32 b0[4], b1[4];
  WORD32* kp = pCtx->key;

  b0[0] = pInBlock[0] ^ kp[RIJNDAEL_KEYSIZE + 24];
  b0[1] = pInBlock[1] ^ kp[RIJNDAEL_KEYSIZE + 25];
  b0[2] = pInBlock[2] ^ kp[RIJNDAEL_KEYSIZE + 26];
  b0[3] = pInBlock[3] ^ kp[RIJNDAEL_KEYSIZE + 27];

  kp += RIJNDAEL_KEYSIZE + 20;

  i_nround(b1, b0, kp); i_nround(b0, b1, kp);
  i_nround(b1, b0, kp); i_nround(b0, b1, kp);
  i_nround(b1, b0, kp); i_nround(b0, b1, kp);
  i_nround(b1, b0, kp); i_nround(b0, b1, kp);
  i_nround(b1, b0, kp); i_nround(b0, b1, kp);
  i_nround(b1, b0, kp); i_nround(b0, b1, kp);
  i_nround(b1, b0, kp); i_lround(b0, b1, kp);

  pOutBlock[0] = b0[0];
  pOutBlock[1] = b0[1];
  pOutBlock[2] = b0[2];
  pOutBlock[3] = b0[3];
}


// public functions

WORD32 Rijndael_GetCipherInfo(CIPHERINFOBLOCK* pInfo)
{
  WORD32 lI;
  WORD8* pSrc;
  WORD8* pDst;
  CIPHERINFOBLOCK tmpInfo;

  tmpInfo.lSizeOf = pInfo->lSizeOf;
  tmpInfo.lBlockSize = RIJNDAEL_BLOCKSIZE;
  tmpInfo.lKeySize = RIJNDAEL_KEYSIZE;
  tmpInfo.blOwnHasher = BOOL_FALSE;
  tmpInfo.lInitDataSize = RIJNDAEL_BLOCKSIZE;
  tmpInfo.lContextSize = sizeof(RIJNDAELCTX);
  tmpInfo.bCipherIs = CIPHER_IS_BLOCKLINK;

  // copy as many bytes of the information block as possible
  pSrc = (WORD8*) &tmpInfo;
  pDst = (WORD8*) pInfo;
  for (lI = 0; lI < tmpInfo.lSizeOf; lI++)
    *pDst++ = *pSrc++;
  return CIPHER_ERROR_NOERROR;
}

WORD32 Rijndael_SelfTest(void* pTestContext)
{
  /*
   * The following test vectors are Gladman test vectors,
   * which means that they are not official.
   */

  const WORD8 testkey[32] =
    { 0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6,
      0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c,
      0x76, 0x2e, 0x71, 0x60, 0xf3, 0x8b, 0x4d, 0xa5,
      0x6a, 0x78, 0x4d, 0x90, 0x45, 0x19, 0x0c, 0xfe };

  const WORD8 plaintext[16] =
    { 0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d,
      0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34 };

  const WORD8 cipher_must[16] =
    { 0x1a, 0x6e, 0x6c, 0x2c, 0x66, 0x2e, 0x7d, 0xa6,
      0x50, 0x1f, 0xfb, 0x62, 0xbc, 0x9e, 0x93, 0xf3 };

  WORD32 testbuf[4];
  RIJNDAELCTX* pCtx = (RIJNDAELCTX*) pTestContext;
  int nI;

  // init. the encryption
  rijndaelSetKey(pCtx, testkey, 32, CIPHER_MODE_ENCRYPT);
  rijndaelEncrypt(pCtx, (WORD32*) plaintext, testbuf);

  // check the encryption
  for (nI = 0; nI < 4; nI++)
  {
    if (testbuf[nI] != ((WORD32*) cipher_must)[nI])
      return CIPHER_ERROR_INVALID;
  }

  // init. the decryption
  rijndaelSetKey(pCtx, testkey, 32, CIPHER_MODE_DECRYPT);
  rijndaelDecrypt(pCtx, testbuf, testbuf);

  // check the decryption
  for (nI = 0; nI < 4; nI++)
  {
    if (testbuf[nI] != ((WORD32*) plaintext)[nI])
      return CIPHER_ERROR_INVALID;
  }

  return CIPHER_ERROR_NOERROR;
}

WORD32 Rijndael_CreateWorkContext(void* pContext,
                                  const WORD8* pKey,
                                  WORD32 lKeyLen,
                                  WORD32 lMode,
                                  void* pInitData,
                                  Cipher_RandomGenerator GetRndBytes,
                                  const void* pRandGenData)
{
  RIJNDAELCTX* pCtx = (RIJNDAELCTX*) pContext;
  WORD32* pCBCIV;

  // do the key setup
  rijndaelSetKey(pCtx, pKey, lKeyLen, lMode);

  pCBCIV = (WORD32*) pInitData;
  if (lMode == CIPHER_MODE_ENCRYPT)
    GetRndBytes((WORD8*) pCBCIV, RIJNDAEL_BLOCKSIZE, pRandGenData);

  // set the CBC IV
  pCtx->cbc_iv[0] = pCBCIV[0];
  pCtx->cbc_iv[1] = pCBCIV[1];
  pCtx->cbc_iv[2] = pCBCIV[2];
  pCtx->cbc_iv[3] = pCBCIV[3];

  return CIPHER_ERROR_NOERROR;
}

void Rijndael_ResetWorkContext(void* pContext,
                               WORD32 lMode,
                               void* pInitData,
                               Cipher_RandomGenerator GetRndBytes,
                               const void* pRandGenData)
{
  RIJNDAELCTX* pCtx = (RIJNDAELCTX*) pContext;
  WORD32* pCBCIV = (WORD32*) pInitData;

  if (lMode == CIPHER_MODE_ENCRYPT)
    GetRndBytes((WORD8*) pCBCIV, RIJNDAEL_BLOCKSIZE, pRandGenData);

  pCtx->cbc_iv[0] = pCBCIV[0];
  pCtx->cbc_iv[1] = pCBCIV[1];
  pCtx->cbc_iv[2] = pCBCIV[2];
  pCtx->cbc_iv[3] = pCBCIV[3];
}

WORD32 Rijndael_DestroyWorkContext(void* pContext)
{
  int nI;
  WORD8* pCtxBuf = (WORD8*) pContext;

  for (nI = 0; nI < sizeof(RIJNDAELCTX); nI++)
    pCtxBuf[nI] = 0x00;

  return CIPHER_ERROR_NOERROR;
}

void Rijndael_EncryptBuffer(void* pContext,
                            const void*  pSource,
                            void* pTarget,
                            WORD32 lNumOfBytes)
{
  WORD32 lNumOfBlocks;
  WORD32* pInBuf = (WORD32*) pSource;
  WORD32* pOutBuf = (WORD32*) pTarget;
  RIJNDAELCTX* pCtx = (RIJNDAELCTX*) pContext;

  lNumOfBlocks = lNumOfBytes / RIJNDAEL_BLOCKSIZE;

  while (lNumOfBlocks--)
  {
    pOutBuf[0] = pInBuf[0] ^ pCtx->cbc_iv[0];
    pOutBuf[1] = pInBuf[1] ^ pCtx->cbc_iv[1];
    pOutBuf[2] = pInBuf[2] ^ pCtx->cbc_iv[2];
    pOutBuf[3] = pInBuf[3] ^ pCtx->cbc_iv[3];

    // encrypt the buffer
    rijndaelEncrypt(pCtx, pOutBuf, pOutBuf);

    // set the new IV
    pCtx->cbc_iv[0] = pOutBuf[0];
    pCtx->cbc_iv[1] = pOutBuf[1];
    pCtx->cbc_iv[2] = pOutBuf[2];
    pCtx->cbc_iv[3] = pOutBuf[3];

    pInBuf  += RIJNDAEL_BLOCKSIZE / 4;
    pOutBuf += RIJNDAEL_BLOCKSIZE / 4;
  }
}

void Rijndael_DecryptBuffer(void* pContext,
                            const void* pSource,
                            void*  pTarget,
                            WORD32 lNumOfBytes,
                            const void* pPreviousBlock)
{
  WORD32 lNumOfBlocks;
  WORD32* pInBuf = (WORD32*) pSource;
  WORD32* pOutBuf = (WORD32*) pTarget;
  WORD32* pPrevBlock = (WORD32*) pPreviousBlock;
  WORD32 save_cbc_iv[4];
  RIJNDAELCTX* pCtx = (RIJNDAELCTX*) pContext;

  lNumOfBlocks = lNumOfBytes / RIJNDAEL_BLOCKSIZE;

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
    rijndaelDecrypt(pCtx, pInBuf, pOutBuf);

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

    pInBuf  += RIJNDAEL_BLOCKSIZE / 4;
    pOutBuf += RIJNDAEL_BLOCKSIZE / 4;
  }
}
