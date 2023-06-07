
/*
 * defines basic primitive data types to avoid system independencies
 */

#ifndef __BASICTYPES_H
#define __BASICTYPES_H


#ifdef WIN32

// basic unsigned integer types
typedef unsigned __int8  WORD8;   // unsigned 8bit integer, prefix "b"
typedef unsigned __int16 WORD16;  // unsigned 8bit integer, prefix "w"
typedef unsigned __int32 WORD32;  // unsigned 8bit integer, prefix "l"
typedef unsigned __int64 WORD64;  // unsigned 8bit integer, prefix "q"


// boolean definitions
typedef unsigned __int8 BYTEBOOL;  // 8bit boolean, prefix "bl"

// our own Unicode type
typedef unsigned __int16 UNICHAR;

#endif


#ifdef UNIX

typedef unsigned char      WORD8;
typedef unsigned short     WORD16;
typedef unsigned int       WORD32;
typedef unsigned long long WORD64;

typedef unsigned char      BYTEBOOL;

typedef unsigned short     UNICHAR;

#endif


#define BOOL_FALSE  0
#define BOOL_TRUE   1


// some nice macros
#define MAKE_WORD64(left, right) ((((WORD64)(left)) << 32) | (WORD64)(right))
#define WORD64_LO(value) ((WORD32)(value & 0xffffffff))
#define WORD64_HI(value) ((WORD32)(value >> 32))


#endif

