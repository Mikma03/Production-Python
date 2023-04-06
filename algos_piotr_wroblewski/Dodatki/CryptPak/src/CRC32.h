

#ifndef __CRC32_H
#define __CRC32_H

#include "cpconfig.h" 
#include "BasicTypes.h" 

#ifdef __cplusplus
extern "C" {
#endif

// startup value for a CRC32
#define CRC32_INITVALUE  0xffffffff

// xor this value to finish a CRC32
#define CRC32_DONEVALUE  0xffffffff


/*
 * updates an existing CRC32
 * -> old CRC32
 * -> pointer to (byte) buffer
 * -> number of bytes to process
 * <- new CRC32
 */
WORD32 CRYPTPAK_API
    CRC32_Update (WORD32, const void*, WORD32);


#ifdef __cplusplus
}
#endif


#endif
