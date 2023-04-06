


#ifndef __LZSS_H
#define __LZSS_H

#include "cpconfig.h"
#include "BasicTypes.h"


#ifdef __cplusplus
extern "C" {
#endif


// the condition codes, these are bitflags
#define  LZSS_START  1
#define  LZSS_WORK   2
#define  LZSS_STOP   4



// LZSS context
typedef struct LZSSCTX  LZSSCTX, *PLZSSCTX;



/*
 * creates an LZSS context
 * <- pointer to LZSS context (NULL if out of memory)
 */
PLZSSCTX CRYPTPAK_API LZSS_Create();


/*
 * destroys an LZSS context
 * -> pointer to LZSS context
 */
void CRYPTPAK_API LZSS_Destroy(PLZSSCTX);



/*
 * compresses a buffer content into a second buffer, due to
 * the stream characteristic of the original source we need 
 * a clever interruption technique, and it's not guaranteed
 * that there'll be something in the target buffer, so the
 * target buffer should be least 12.5% larger than the source
 * -> pointer to work context
 * -> pointer to source buffer
 * -> pointer to target buffer
 * -> number of bytes to compress
 * -> code number, for sending start and stop signals
 * <- number of compressed bytes
 */
WORD32 CRYPTPAK_API 
    LZSS_Compress (PLZSSCTX, const void*, void*, WORD32, WORD8);

                   
/*
 * decompresses a data stream, has two interrupt
 * possibilities in a cycle: either a buffer has been
 * processed completely or the output buffer is full and
 * needs to be emptied
 * -> pointer to work context
 * -> pointer to source buffer
 * -> pointer to target buffer
 * -> number of bytes to decompress
 * -> size of the output buffer
 * -> code number, for sending start and stop signals
 * -> pointer to a flag which 
 *        a) lets the routine detect that not all input data
 *           of the last cycle has been decompressed
 *        b) forces the caller to empty its output buffer
 *           and to recall (!) the routine
 *        (the flag has to be set to BOOL_FALSE for a new input buffer)
 * <- number of decompressed bytes when the cycle is finished
 */
WORD32 CRYPTPAK_API 
    LZSS_Decompress (PLZSSCTX, const void*, void*, WORD32, WORD32, WORD8, BYTEBOOL*);


#ifdef __cplusplus
}
#endif


#endif

