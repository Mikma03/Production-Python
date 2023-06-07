/* Prototypes for LZW4C */

#ifndef FILE
#include <stdio.h>
#endif

#ifdef __SMALL__
#error SMALL model not supported
#endif

#ifdef __MEDIUM__
#error MEDIUM model not supported
#endif

#ifdef __COMPACT__
#ifdef __cplusplus
extern "C" int InitLZW(void far *(near *)(unsigned int), int);
extern "C" int TermLZW(void (near *)(void far *) );
extern "C" int Compress(int (near *)(void), int (near *)(char));
extern "C" int Expand(int (near *)(void), int (near *)(char));
#else
int InitLZW(void far *(near *)(unsigned int), int);
int TermLZW(void (near *)(void far *) );
int Compress(int (near *)(void), int (near *)(char));
int Expand(int (near *)(void), int (near *)(char));
#endif
#endif

#ifdef __LARGE__
#ifdef __cplusplus
extern "C" int InitLZW(void far *(far *)(unsigned int), int);
extern "C" int TermLZW(void (far *)(void far *) );
extern "C" int Compress(int (far *)(void), int (far *)(char));
extern "C" int Expand(int (far *)(void), int (far *)(char));
#else
int InitLZW(void far *(far *)(unsigned int), int);
int TermLZW(void (far *)(void far *) );
int Compress(int (far *)(void), int (far *)(char));
int Expand(int (far *)(void), int (far *)(char));
#endif
#endif

/* error codes */

#define EXPANSION_ERROR  -1
#define CANNOT_ALLOCATE  -2
#define INTERNAL_ERROR   -3
#define NOT_INITIALIZED  -4
#define BAD_BITCODE      -5
