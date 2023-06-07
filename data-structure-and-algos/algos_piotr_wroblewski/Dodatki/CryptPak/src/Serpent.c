/* This is an independent implementation of the encryption algorithm:   */
/*                                                                      */
/*         Serpent by Ross Anderson, Eli Biham and Lars Knudsen         */
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
/* Converted to a CryptPak cipher by Christian Thoeing                  */
/* e-mail: c.thoeing@web.de                                             */
/* Some parts of this code are taken from Wei Dai's serpent.cpp         */

#include "Serpent.h"

// the Serpent work context
typedef struct {
  WORD32 l_key[140];
  WORD32 cbc_iv[4];
} SERPENTCTX;

#define rotr(x,n)   (((x) >> ((int)(n))) | ((x) << (32 - (int)(n))))
#define rotl(x,n)   (((x) << ((int)(n))) | ((x) >> (32 - (int)(n))))

/* Partially optimised Serpent S Box boolean functions derived	*/
/* using a recursive descent analyser but without a full search */
/* of all subtrees. This set of S boxes is the result of work	*/
/* by Sam Simpson and Brian Gladman using the spare time on a	*/
/* cluster of high capacity servers to search for S boxes with	*/
/* this customised search engine.				*/
/*								*/
/* Copyright:	Dr B. R Gladman (gladman@seven77.demon.co.uk)	*/
/*				and Sam Simpson (s.simpson@mia.co.uk) */
/*				17th December 1998		*/
/*								*/
/* We hereby give permission for information in this file to be */
/* used freely subject only to acknowledgement of its origin	*/

/* 15 terms */

#define sb0(a,b,c,d,e,f,g,h)	\
	t1 = a ^ d; 	\
	t2 = a & d; 	\
	t3 = c ^ t1;	\
	t6 = b & t1;	\
	t4 = b ^ t3;	\
	t10 = ~t3;		\
	h = t2 ^ t4;	\
	t7 = a ^ t6;	\
	t14 = ~t7;		\
	t8 = c | t7;	\
	t11 = t3 ^ t7;	\
	g = t4 ^ t8;	\
	t12 = h & t11;	\
	f = t10 ^ t12;	\
	e = t12 ^ t14

/* 15 terms */

#define ib0(a,b,c,d,e,f,g,h)	\
	t1 = ~a;		\
	t2 = a ^ b; 	\
	t3 = t1 | t2;	\
	t4 = d ^ t3;	\
	t7 = d & t2;	\
	t5 = c ^ t4;	\
	t8 = t1 ^ t7;	\
	g = t2 ^ t5;	\
	t11 = a & t4;	\
	t9 = g & t8;	\
	t14 = t5 ^ t8;	\
	f = t4 ^ t9;	\
	t12 = t5 | f;	\
	h = t11 ^ t12;	\
	e = h ^ t14

/* 14 terms!  */

#define sb1(a,b,c,d,e,f,g,h)	\
	t1 = ~a;		\
	t2 = b ^ t1;	\
	t3 = a | t2;	\
	t4 = d | t2;	\
	t5 = c ^ t3;	\
	g = d ^ t5; 	\
	t7 = b ^ t4;	\
	t8 = t2 ^ g;	\
	t9 = t5 & t7;	\
	h = t8 ^ t9;	\
	t11 = t5 ^ t7;	\
	f = h ^ t11;	\
	t13 = t8 & t11; \
	e = t5 ^ t13

/* 17 terms */

#define ib1(a,b,c,d,e,f,g,h)	\
	t1 = a ^ d; 	\
	t2 = a & b; 	\
	t3 = b ^ c; 	\
	t4 = a ^ t3;	\
	t5 = b | d; 	\
	t7 = c | t1;	\
	h = t4 ^ t5;	\
	t8 = b ^ t7;	\
	t11 = ~t2;		\
	t9 = t4 & t8;	\
	f = t1 ^ t9;	\
	t13 = t9 ^ t11; \
	t12 = h & f;	\
	g = t12 ^ t13;	\
	t15 = a & d;	\
	t16 = c ^ t13;	\
	e = t15 ^ t16

/* 16 terms */

#define sb2(a,b,c,d,e,f,g,h)	\
	t1 = ~a;		\
	t2 = b ^ d; 	\
	t3 = c & t1;	\
	t13 = d | t1;	\
	e = t2 ^ t3;	\
	t5 = c ^ t1;	\
	t6 = c ^ e; 	\
	t7 = b & t6;	\
	t10 = e | t5;	\
	h = t5 ^ t7;	\
	t9 = d | t7;	\
	t11 = t9 & t10; \
	t14 = t2 ^ h;	\
	g = a ^ t11;	\
	t15 = g ^ t13;	\
	f = t14 ^ t15

/* 16 terms */

#define ib2(a,b,c,d,e,f,g,h)	\
	t1 = b ^ d; 	\
	t2 = ~t1;		\
	t3 = a ^ c; 	\
	t4 = c ^ t1;	\
	t7 = a | t2;	\
	t5 = b & t4;	\
	t8 = d ^ t7;	\
	t11 = ~t4;		\
	e = t3 ^ t5;	\
	t9 = t3 | t8;	\
	t14 = d & t11;	\
	h = t1 ^ t9;	\
	t12 = e | h;	\
	f = t11 ^ t12;	\
	t15 = t3 ^ t12; \
	g = t14 ^ t15

/* 17 terms */

#define sb3(a,b,c,d,e,f,g,h)	\
	t1 = a ^ c; 	\
	t2 = d ^ t1;	\
	t3 = a & t2;	\
	t4 = d ^ t3;	\
	t5 = b & t4;	\
	g = t2 ^ t5;	\
	t7 = a | g; 	\
	t8 = b | d; 	\
	t11 = a | d;	\
	t9 = t4 & t7;	\
	f = t8 ^ t9;	\
	t12 = b ^ t11;	\
	t13 = g ^ t9;	\
	t15 = t3 ^ t8;	\
	h = t12 ^ t13;	\
	t16 = c & t15;	\
	e = t12 ^ t16

/* 16 term solution that performs less well than 17 term one
   in my environment (PPro/PII)

#define sb3(a,b,c,d,e,f,g,h)	\
	t1 = a ^ b; 	\
	t2 = a & c; 	\
	t3 = a | d; 	\
	t4 = c ^ d; 	\
	t5 = t1 & t3;	\
	t6 = t2 | t5;	\
	g = t4 ^ t6;	\
	t8 = b ^ t3;	\
	t9 = t6 ^ t8;	\
	t10 = t4 & t9;	\
	e = t1 ^ t10;	\
	t12 = g & e;	\
	f = t9 ^ t12;	\
	t14 = b | d;	\
	t15 = t4 ^ t12; \
	h = t14 ^ t15
*/

/* 17 terms */

#define ib3(a,b,c,d,e,f,g,h)	\
	t1 = b ^ c; 	\
	t2 = b | c; 	\
	t3 = a ^ c; 	\
	t7 = a ^ d; 	\
	t4 = t2 ^ t3;	\
	t5 = d | t4;	\
	t9 = t2 ^ t7;	\
	e = t1 ^ t5;	\
	t8 = t1 | t5;	\
	t11 = a & t4;	\
	g = t8 ^ t9;	\
	t12 = e | t9;	\
	f = t11 ^ t12;	\
	t14 = a & g;	\
	t15 = t2 ^ t14; \
	t16 = e & t15;	\
	h = t4 ^ t16

/* 15 terms */

#define sb4(a,b,c,d,e,f,g,h)	\
	t1 = a ^ d; 	\
	t2 = d & t1;	\
	t3 = c ^ t2;	\
	t4 = b | t3;	\
	h = t1 ^ t4;	\
	t6 = ~b;		\
	t7 = t1 | t6;	\
	e = t3 ^ t7;	\
	t9 = a & e; 	\
	t10 = t1 ^ t6;	\
	t11 = t4 & t10; \
	g = t9 ^ t11;	\
	t13 = a ^ t3;	\
	t14 = t10 & g;	\
	f = t13 ^ t14

/* 17 terms */

#define ib4(a,b,c,d,e,f,g,h)	\
	t1 = c ^ d; 	\
	t2 = c | d; 	\
	t3 = b ^ t2;	\
	t4 = a & t3;	\
	f = t1 ^ t4;	\
	t6 = a ^ d; 	\
	t7 = b | d; 	\
	t8 = t6 & t7;	\
	h = t3 ^ t8;	\
	t10 = ~a;		\
	t11 = c ^ h;	\
	t12 = t10 | t11;\
	e = t3 ^ t12;	\
	t14 = c | t4;	\
	t15 = t7 ^ t14; \
	t16 = h | t10;	\
	g = t15 ^ t16

/* 16 terms */

#define sb5(a,b,c,d,e,f,g,h)	\
	t1 = ~a;		\
	t2 = a ^ b; 	\
	t3 = a ^ d; 	\
	t4 = c ^ t1;	\
	t5 = t2 | t3;	\
	e = t4 ^ t5;	\
	t7 = d & e; 	\
	t8 = t2 ^ e;	\
	t10 = t1 | e;	\
	f = t7 ^ t8;	\
	t11 = t2 | t7;	\
	t12 = t3 ^ t10; \
	t14 = b ^ t7;	\
	g = t11 ^ t12;	\
	t15 = f & t12;	\
	h = t14 ^ t15

/* 16 terms */

#define ib5(a,b,c,d,e,f,g,h)	\
	t1 = ~c;		\
	t2 = b & t1;	\
	t3 = d ^ t2;	\
	t4 = a & t3;	\
	t5 = b ^ t1;	\
	h = t4 ^ t5;	\
	t7 = b | h; 	\
	t8 = a & t7;	\
	f = t3 ^ t8;	\
	t10 = a | d;	\
	t11 = t1 ^ t7;	\
	e = t10 ^ t11;	\
	t13 = a ^ c;	\
	t14 = b & t10;	\
	t15 = t4 | t13; \
	g = t14 ^ t15

/* 15 terms */

#define sb6(a,b,c,d,e,f,g,h)	\
	t1 = ~a;		\
	t2 = a ^ d; 	\
	t3 = b ^ t2;	\
	t4 = t1 | t2;	\
	t5 = c ^ t4;	\
	f = b ^ t5; 	\
	t13 = ~t5;		\
	t7 = t2 | f;	\
	t8 = d ^ t7;	\
	t9 = t5 & t8;	\
	g = t3 ^ t9;	\
	t11 = t5 ^ t8;	\
	e = g ^ t11;	\
	t14 = t3 & t11; \
	h = t13 ^ t14

/* 15 terms */

#define ib6(a,b,c,d,e,f,g,h)	\
	t1 = ~a;		\
	t2 = a ^ b; 	\
	t3 = c ^ t2;	\
	t4 = c | t1;	\
	t5 = d ^ t4;	\
	t13 = d & t1;	\
	f = t3 ^ t5;	\
	t7 = t3 & t5;	\
	t8 = t2 ^ t7;	\
	t9 = b | t8;	\
	h = t5 ^ t9;	\
	t11 = b | h;	\
	e = t8 ^ t11;	\
	t14 = t3 ^ t11; \
	g = t13 ^ t14

/* 17 terms */

#define sb7(a,b,c,d,e,f,g,h)	\
	t1 = ~c;		\
	t2 = b ^ c; 	\
	t3 = b | t1;	\
	t4 = d ^ t3;	\
	t5 = a & t4;	\
	t7 = a ^ d; 	\
	h = t2 ^ t5;	\
	t8 = b ^ t5;	\
	t9 = t2 | t8;	\
	t11 = d & t3;	\
	f = t7 ^ t9;	\
	t12 = t5 ^ f;	\
	t15 = t1 | t4;	\
	t13 = h & t12;	\
	g = t11 ^ t13;	\
	t16 = t12 ^ g;	\
	e = t15 ^ t16

/* 17 terms */

#define ib7(a,b,c,d,e,f,g,h)	\
	t1 = a & b; 	\
	t2 = a | b; 	\
	t3 = c | t1;	\
	t4 = d & t2;	\
	h = t3 ^ t4;	\
	t6 = ~d;		\
	t7 = b ^ t4;	\
	t8 = h ^ t6;	\
	t11 = c ^ t7;	\
	t9 = t7 | t8;	\
	f = a ^ t9; 	\
	t12 = d | f;	\
	e = t11 ^ t12;	\
	t14 = a & h;	\
	t15 = t3 ^ f;	\
	t16 = e ^ t14;	\
	g = t15 ^ t16

#define k_xor(r,a,b,c,d)	\
	a ^= l_key[4 * r +  8]; \
	b ^= l_key[4 * r +  9]; \
	c ^= l_key[4 * r + 10]; \
	d ^= l_key[4 * r + 11]

#define k_set(r,a,b,c,d)	\
	a = l_key[4 * r +  8];	\
	b = l_key[4 * r +  9];	\
	c = l_key[4 * r + 10];	\
	d = l_key[4 * r + 11]

#define k_get(r,a,b,c,d)	\
	l_key[4 * r +  8] = a;	\
	l_key[4 * r +  9] = b;	\
	l_key[4 * r + 10] = c;	\
	l_key[4 * r + 11] = d

/* the linear transformation and its inverse	*/

#define rot(a,b,c,d)	\
	a = rotl(a, 13);	\
	c = rotl(c, 3); 	\
	d ^= c ^ (a << 3);	\
	b ^= a ^ c; 		\
	d = rotl(d, 7); 	\
	b = rotl(b, 1); 	\
	a ^= b ^ d; 		\
	c ^= d ^ (b << 7);	\
	a = rotl(a, 5); 	\
	c = rotl(c, 22)

#define irot(a,b,c,d)	\
	c = rotr(c, 22);	\
	a = rotr(a, 5); 	\
	c ^= d ^ (b << 7);	\
	a ^= b ^ d; 		\
	d = rotr(d, 7); 	\
	b = rotr(b, 1); 	\
	d ^= c ^ (a << 3);	\
	b ^= a ^ c; 		\
	c = rotr(c, 3); 	\
	a = rotr(a, 13)

/* initialise the key schedule from the user supplied key	*/
/* Note: lKeyLen is the key length in BYTES, not in BITS!       */
/* Thanks to Wei Dai for this code!                             */

void serpentSetKey(SERPENTCTX* pCtx,
                   const WORD8* userKey,
                   WORD32 lKeyLen)
{
  WORD32 i,lk,a,b,c,d,e,f,g,h;
  WORD32 t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16;
  WORD32* l_key = pCtx->l_key;

  for (i = 0; i < 32; i++)
    l_key[i] = 0;

  for (i = 0; i < lKeyLen; i++)
    l_key[i/4] |= userKey[i] << ((i%4)*8);

  if (lKeyLen < 32)
    l_key[lKeyLen/4] |= 1 << ((lKeyLen%4)*8);

  for(i = 0; i < 132; ++i)
  {
    lk = l_key[i] ^ l_key[i + 3] ^ l_key[i + 5] ^ l_key[i + 7] ^ 0x9e3779b9 ^ i;
    l_key[i + 8] = (lk << 11) | (lk >> 21);
  }

  k_set( 0,a,b,c,d);sb3(a,b,c,d,e,f,g,h);k_get( 0,e,f,g,h);
  k_set( 1,a,b,c,d);sb2(a,b,c,d,e,f,g,h);k_get( 1,e,f,g,h);
  k_set( 2,a,b,c,d);sb1(a,b,c,d,e,f,g,h);k_get( 2,e,f,g,h);
  k_set( 3,a,b,c,d);sb0(a,b,c,d,e,f,g,h);k_get( 3,e,f,g,h);
  k_set( 4,a,b,c,d);sb7(a,b,c,d,e,f,g,h);k_get( 4,e,f,g,h);
  k_set( 5,a,b,c,d);sb6(a,b,c,d,e,f,g,h);k_get( 5,e,f,g,h);
  k_set( 6,a,b,c,d);sb5(a,b,c,d,e,f,g,h);k_get( 6,e,f,g,h);
  k_set( 7,a,b,c,d);sb4(a,b,c,d,e,f,g,h);k_get( 7,e,f,g,h);
  k_set( 8,a,b,c,d);sb3(a,b,c,d,e,f,g,h);k_get( 8,e,f,g,h);
  k_set( 9,a,b,c,d);sb2(a,b,c,d,e,f,g,h);k_get( 9,e,f,g,h);
  k_set(10,a,b,c,d);sb1(a,b,c,d,e,f,g,h);k_get(10,e,f,g,h);
  k_set(11,a,b,c,d);sb0(a,b,c,d,e,f,g,h);k_get(11,e,f,g,h);
  k_set(12,a,b,c,d);sb7(a,b,c,d,e,f,g,h);k_get(12,e,f,g,h);
  k_set(13,a,b,c,d);sb6(a,b,c,d,e,f,g,h);k_get(13,e,f,g,h);
  k_set(14,a,b,c,d);sb5(a,b,c,d,e,f,g,h);k_get(14,e,f,g,h);
  k_set(15,a,b,c,d);sb4(a,b,c,d,e,f,g,h);k_get(15,e,f,g,h);
  k_set(16,a,b,c,d);sb3(a,b,c,d,e,f,g,h);k_get(16,e,f,g,h);
  k_set(17,a,b,c,d);sb2(a,b,c,d,e,f,g,h);k_get(17,e,f,g,h);
  k_set(18,a,b,c,d);sb1(a,b,c,d,e,f,g,h);k_get(18,e,f,g,h);
  k_set(19,a,b,c,d);sb0(a,b,c,d,e,f,g,h);k_get(19,e,f,g,h);
  k_set(20,a,b,c,d);sb7(a,b,c,d,e,f,g,h);k_get(20,e,f,g,h);
  k_set(21,a,b,c,d);sb6(a,b,c,d,e,f,g,h);k_get(21,e,f,g,h);
  k_set(22,a,b,c,d);sb5(a,b,c,d,e,f,g,h);k_get(22,e,f,g,h);
  k_set(23,a,b,c,d);sb4(a,b,c,d,e,f,g,h);k_get(23,e,f,g,h);
  k_set(24,a,b,c,d);sb3(a,b,c,d,e,f,g,h);k_get(24,e,f,g,h);
  k_set(25,a,b,c,d);sb2(a,b,c,d,e,f,g,h);k_get(25,e,f,g,h);
  k_set(26,a,b,c,d);sb1(a,b,c,d,e,f,g,h);k_get(26,e,f,g,h);
  k_set(27,a,b,c,d);sb0(a,b,c,d,e,f,g,h);k_get(27,e,f,g,h);
  k_set(28,a,b,c,d);sb7(a,b,c,d,e,f,g,h);k_get(28,e,f,g,h);
  k_set(29,a,b,c,d);sb6(a,b,c,d,e,f,g,h);k_get(29,e,f,g,h);
  k_set(30,a,b,c,d);sb5(a,b,c,d,e,f,g,h);k_get(30,e,f,g,h);
  k_set(31,a,b,c,d);sb4(a,b,c,d,e,f,g,h);k_get(31,e,f,g,h);
  k_set(32,a,b,c,d);sb3(a,b,c,d,e,f,g,h);k_get(32,e,f,g,h);
}

void serpentEncrypt(SERPENTCTX* pCtx,
                    const WORD32* pInBlock,
                    WORD32* pOutBlock)
{
  WORD32 a,b,c,d,e,f,g,h;
  WORD32 t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16;
  WORD32* l_key = pCtx->l_key;

  a = pInBlock[0];
  b = pInBlock[1];
  c = pInBlock[2];
  d = pInBlock[3];

  // perform 32 rounds of encryption
  k_xor( 0,a,b,c,d); sb0(a,b,c,d,e,f,g,h); rot(e,f,g,h);
  k_xor( 1,e,f,g,h); sb1(e,f,g,h,a,b,c,d); rot(a,b,c,d);
  k_xor( 2,a,b,c,d); sb2(a,b,c,d,e,f,g,h); rot(e,f,g,h);
  k_xor( 3,e,f,g,h); sb3(e,f,g,h,a,b,c,d); rot(a,b,c,d);
  k_xor( 4,a,b,c,d); sb4(a,b,c,d,e,f,g,h); rot(e,f,g,h);
  k_xor( 5,e,f,g,h); sb5(e,f,g,h,a,b,c,d); rot(a,b,c,d);
  k_xor( 6,a,b,c,d); sb6(a,b,c,d,e,f,g,h); rot(e,f,g,h);
  k_xor( 7,e,f,g,h); sb7(e,f,g,h,a,b,c,d); rot(a,b,c,d);
  k_xor( 8,a,b,c,d); sb0(a,b,c,d,e,f,g,h); rot(e,f,g,h);
  k_xor( 9,e,f,g,h); sb1(e,f,g,h,a,b,c,d); rot(a,b,c,d);
  k_xor(10,a,b,c,d); sb2(a,b,c,d,e,f,g,h); rot(e,f,g,h);
  k_xor(11,e,f,g,h); sb3(e,f,g,h,a,b,c,d); rot(a,b,c,d);
  k_xor(12,a,b,c,d); sb4(a,b,c,d,e,f,g,h); rot(e,f,g,h);
  k_xor(13,e,f,g,h); sb5(e,f,g,h,a,b,c,d); rot(a,b,c,d);
  k_xor(14,a,b,c,d); sb6(a,b,c,d,e,f,g,h); rot(e,f,g,h);
  k_xor(15,e,f,g,h); sb7(e,f,g,h,a,b,c,d); rot(a,b,c,d);
  k_xor(16,a,b,c,d); sb0(a,b,c,d,e,f,g,h); rot(e,f,g,h);
  k_xor(17,e,f,g,h); sb1(e,f,g,h,a,b,c,d); rot(a,b,c,d);
  k_xor(18,a,b,c,d); sb2(a,b,c,d,e,f,g,h); rot(e,f,g,h);
  k_xor(19,e,f,g,h); sb3(e,f,g,h,a,b,c,d); rot(a,b,c,d);
  k_xor(20,a,b,c,d); sb4(a,b,c,d,e,f,g,h); rot(e,f,g,h);
  k_xor(21,e,f,g,h); sb5(e,f,g,h,a,b,c,d); rot(a,b,c,d);
  k_xor(22,a,b,c,d); sb6(a,b,c,d,e,f,g,h); rot(e,f,g,h);
  k_xor(23,e,f,g,h); sb7(e,f,g,h,a,b,c,d); rot(a,b,c,d);
  k_xor(24,a,b,c,d); sb0(a,b,c,d,e,f,g,h); rot(e,f,g,h);
  k_xor(25,e,f,g,h); sb1(e,f,g,h,a,b,c,d); rot(a,b,c,d);
  k_xor(26,a,b,c,d); sb2(a,b,c,d,e,f,g,h); rot(e,f,g,h);
  k_xor(27,e,f,g,h); sb3(e,f,g,h,a,b,c,d); rot(a,b,c,d);
  k_xor(28,a,b,c,d); sb4(a,b,c,d,e,f,g,h); rot(e,f,g,h);
  k_xor(29,e,f,g,h); sb5(e,f,g,h,a,b,c,d); rot(a,b,c,d);
  k_xor(30,a,b,c,d); sb6(a,b,c,d,e,f,g,h); rot(e,f,g,h);
  k_xor(31,e,f,g,h); sb7(e,f,g,h,a,b,c,d); k_xor(32,a,b,c,d);

  pOutBlock[0] = a;
  pOutBlock[1] = b;
  pOutBlock[2] = c;
  pOutBlock[3] = d;
}

void serpentDecrypt(SERPENTCTX* pCtx,
                    const WORD32* pInBlock,
                    WORD32* pOutBlock)
{
  WORD32 a,b,c,d,e,f,g,h;
  WORD32 t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16;
  WORD32* l_key = pCtx->l_key;

  a = pInBlock[0];
  b = pInBlock[1];
  c = pInBlock[2];
  d = pInBlock[3];

  k_xor(32,a,b,c,d); ib7(a,b,c,d,e,f,g,h); k_xor(31,e,f,g,h);
  irot(e,f,g,h); ib6(e,f,g,h,a,b,c,d); k_xor(30,a,b,c,d);
  irot(a,b,c,d); ib5(a,b,c,d,e,f,g,h); k_xor(29,e,f,g,h);
  irot(e,f,g,h); ib4(e,f,g,h,a,b,c,d); k_xor(28,a,b,c,d);
  irot(a,b,c,d); ib3(a,b,c,d,e,f,g,h); k_xor(27,e,f,g,h);
  irot(e,f,g,h); ib2(e,f,g,h,a,b,c,d); k_xor(26,a,b,c,d);
  irot(a,b,c,d); ib1(a,b,c,d,e,f,g,h); k_xor(25,e,f,g,h);
  irot(e,f,g,h); ib0(e,f,g,h,a,b,c,d); k_xor(24,a,b,c,d);
  irot(a,b,c,d); ib7(a,b,c,d,e,f,g,h); k_xor(23,e,f,g,h);
  irot(e,f,g,h); ib6(e,f,g,h,a,b,c,d); k_xor(22,a,b,c,d);
  irot(a,b,c,d); ib5(a,b,c,d,e,f,g,h); k_xor(21,e,f,g,h);
  irot(e,f,g,h); ib4(e,f,g,h,a,b,c,d); k_xor(20,a,b,c,d);
  irot(a,b,c,d); ib3(a,b,c,d,e,f,g,h); k_xor(19,e,f,g,h);
  irot(e,f,g,h); ib2(e,f,g,h,a,b,c,d); k_xor(18,a,b,c,d);
  irot(a,b,c,d); ib1(a,b,c,d,e,f,g,h); k_xor(17,e,f,g,h);
  irot(e,f,g,h); ib0(e,f,g,h,a,b,c,d); k_xor(16,a,b,c,d);
  irot(a,b,c,d); ib7(a,b,c,d,e,f,g,h); k_xor(15,e,f,g,h);
  irot(e,f,g,h); ib6(e,f,g,h,a,b,c,d); k_xor(14,a,b,c,d);
  irot(a,b,c,d); ib5(a,b,c,d,e,f,g,h); k_xor(13,e,f,g,h);
  irot(e,f,g,h); ib4(e,f,g,h,a,b,c,d); k_xor(12,a,b,c,d);
  irot(a,b,c,d); ib3(a,b,c,d,e,f,g,h); k_xor(11,e,f,g,h);
  irot(e,f,g,h); ib2(e,f,g,h,a,b,c,d); k_xor(10,a,b,c,d);
  irot(a,b,c,d); ib1(a,b,c,d,e,f,g,h); k_xor( 9,e,f,g,h);
  irot(e,f,g,h); ib0(e,f,g,h,a,b,c,d); k_xor( 8,a,b,c,d);
  irot(a,b,c,d); ib7(a,b,c,d,e,f,g,h); k_xor( 7,e,f,g,h);
  irot(e,f,g,h); ib6(e,f,g,h,a,b,c,d); k_xor( 6,a,b,c,d);
  irot(a,b,c,d); ib5(a,b,c,d,e,f,g,h); k_xor( 5,e,f,g,h);
  irot(e,f,g,h); ib4(e,f,g,h,a,b,c,d); k_xor( 4,a,b,c,d);
  irot(a,b,c,d); ib3(a,b,c,d,e,f,g,h); k_xor( 3,e,f,g,h);
  irot(e,f,g,h); ib2(e,f,g,h,a,b,c,d); k_xor( 2,a,b,c,d);
  irot(a,b,c,d); ib1(a,b,c,d,e,f,g,h); k_xor( 1,e,f,g,h);
  irot(e,f,g,h); ib0(e,f,g,h,a,b,c,d); k_xor( 0,a,b,c,d);

  pOutBlock[0] = a;
  pOutBlock[1] = b;
  pOutBlock[2] = c;
  pOutBlock[3] = d;
}


// public functions

WORD32 Serpent_GetCipherInfo(CIPHERINFOBLOCK* pInfo)
{
  WORD32 lI;
  WORD8* pSrc;
  WORD8* pDst;
  CIPHERINFOBLOCK tmpInfo;

  tmpInfo.lSizeOf = pInfo->lSizeOf;
  tmpInfo.lBlockSize = SERPENT_BLOCKSIZE;
  tmpInfo.lKeySize = SERPENT_KEYSIZE;
  tmpInfo.blOwnHasher = BOOL_FALSE;
  tmpInfo.lInitDataSize = SERPENT_BLOCKSIZE;
  tmpInfo.lContextSize = sizeof(SERPENTCTX);
  tmpInfo.bCipherIs = CIPHER_IS_BLOCKLINK;

  // copy as many bytes of the information block as possible
  pSrc = (WORD8*) &tmpInfo;
  pDst = (WORD8*) pInfo;
  for (lI = 0; lI < tmpInfo.lSizeOf; lI++)
    *pDst++ = *pSrc++;
  return CIPHER_ERROR_NOERROR;
}

WORD32 Serpent_SelfTest(void* pTestContext)
{
  /*
   * NOTE: These test vectors are NOT official test vectors.
   * I tested this implementation by comparing it with the outputs given
   * in ecb_e_m.txt (see the Serpent package for more details). The official
   * test implementation encrypts the plaintext vector 10,000 times, which
   * makes it fairly slow. That's why I decided to use my own test vectors.
   * However, this implementation was throughly tested and should work fine.
   */

  const WORD8 testkey[32] =
    { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
      21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31 };

  const WORD32 plaintext[4] =
    { 0x01234567, 0xABCDEF01, 0xA0B1C2D3, 0xE4F58899 };

  const WORD32 cipher_must[4] =
    { 0xB633567F, 0x52776204, 0x8D761E99, 0x6701200B };

  WORD32 testbuf[4];
  SERPENTCTX* pCtx = (SERPENTCTX*) pTestContext;
  int nI;

  // initialize the cipher
  serpentSetKey(pCtx, testkey, 32);

  // encrypt the test vector
  serpentEncrypt(pCtx, plaintext, testbuf);

  // did it work correctly?
  for (nI = 0; nI < 4; nI++)
  {
    if (testbuf[nI] != cipher_must[nI])
      return CIPHER_ERROR_INVALID;
  }

  // test the decryption
  serpentDecrypt(pCtx, testbuf, testbuf);

  for (nI = 0; nI < 4; nI++)
  {
    if (testbuf[nI] != plaintext[nI])
      return CIPHER_ERROR_INVALID;
  }

  return CIPHER_ERROR_NOERROR;
}

WORD32 Serpent_CreateWorkContext(void* pContext,
                                 const WORD8* pKey,
                                 WORD32 lKeyLen,
                                 WORD32 lMode,
                                 void* pInitData,
                                 Cipher_RandomGenerator GetRndBytes,
                                 const void* pRandGenData)
{
  SERPENTCTX* pCtx = (SERPENTCTX*) pContext;
  WORD32* pCBCIV;

  // do the key setup
  serpentSetKey(pCtx, pKey, lKeyLen);

  pCBCIV = (WORD32*) pInitData;
  if (lMode == CIPHER_MODE_ENCRYPT)
    GetRndBytes((WORD8*) pCBCIV, SERPENT_BLOCKSIZE, pRandGenData);

  // set the CBC IV
  pCtx->cbc_iv[0] = pCBCIV[0];
  pCtx->cbc_iv[1] = pCBCIV[1];
  pCtx->cbc_iv[2] = pCBCIV[2];
  pCtx->cbc_iv[3] = pCBCIV[3];

  return CIPHER_ERROR_NOERROR;
}

void Serpent_ResetWorkContext(void* pContext,
                              WORD32 lMode,
                              void* pInitData,
                              Cipher_RandomGenerator GetRndBytes,
                              const void* pRandGenData)
{
  SERPENTCTX* pCtx = (SERPENTCTX*) pContext;
  WORD32* pCBCIV = (WORD32*) pInitData;

  if (lMode == CIPHER_MODE_ENCRYPT)
    GetRndBytes((WORD8*) pCBCIV, SERPENT_BLOCKSIZE, pRandGenData);

  pCtx->cbc_iv[0] = pCBCIV[0];
  pCtx->cbc_iv[1] = pCBCIV[1];
  pCtx->cbc_iv[2] = pCBCIV[2];
  pCtx->cbc_iv[3] = pCBCIV[3];
}

WORD32 Serpent_DestroyWorkContext(void *pContext)
{
  int nI;
  WORD8* pCtxBuf = (WORD8*) pContext;

  for (nI = 0; nI < sizeof(SERPENTCTX); nI++)
    pCtxBuf[nI] = 0x00;

  return CIPHER_ERROR_NOERROR;
}

void Serpent_EncryptBuffer(void* pContext,
                           const void*  pSource,
                           void* pTarget,
                           WORD32 lNumOfBytes)
{
  WORD32 lNumOfBlocks;
  WORD32* pInBuf = (WORD32*) pSource;
  WORD32* pOutBuf = (WORD32*) pTarget;
  SERPENTCTX* pCtx = (SERPENTCTX*) pContext;

  lNumOfBlocks = lNumOfBytes / SERPENT_BLOCKSIZE;

  while (lNumOfBlocks--)
  {
    pOutBuf[0] = pInBuf[0] ^ pCtx->cbc_iv[0];
    pOutBuf[1] = pInBuf[1] ^ pCtx->cbc_iv[1];
    pOutBuf[2] = pInBuf[2] ^ pCtx->cbc_iv[2];
    pOutBuf[3] = pInBuf[3] ^ pCtx->cbc_iv[3];

    // encrypt the buffer
    serpentEncrypt(pCtx, pOutBuf, pOutBuf);

    // set the new IV
    pCtx->cbc_iv[0] = pOutBuf[0];
    pCtx->cbc_iv[1] = pOutBuf[1];
    pCtx->cbc_iv[2] = pOutBuf[2];
    pCtx->cbc_iv[3] = pOutBuf[3];

    pInBuf  += SERPENT_BLOCKSIZE / 4;
    pOutBuf += SERPENT_BLOCKSIZE / 4;
  }
}

void Serpent_DecryptBuffer(void* pContext,
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
  SERPENTCTX* pCtx = (SERPENTCTX*) pContext;

  lNumOfBlocks = lNumOfBytes / SERPENT_BLOCKSIZE;

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
    serpentDecrypt(pCtx, pInBuf, pOutBuf);

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

    pInBuf  += SERPENT_BLOCKSIZE / 4;
    pOutBuf += SERPENT_BLOCKSIZE / 4;
  }
}
