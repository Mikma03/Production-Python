

#ifndef __SUPPORT_H
#define __SUPPORT_H

#include "BasicTypes.h"
#include "cpconfig.h"


#ifdef __cplusplus
extern "C" {
#endif


/*
 * returns the version of CRYPTPAK.DLL
 * <- version number (low word: built number, high word: minor version
 *    in low byte, major version in high byte), valid in the
 *    xx.xx.xxx format
 */
WORD32 CRYPTPAK_API Support_GetVersion();




// key chrunching methods
#define CRUNCHKEY_METHOD_SHAEXTENDER    0
#define CRUNCHKEY_METHOD_SHAEXTXORLOOP  1


/*
 * calculates the necessary size of a buld buffer, which pointer
 * can be passed to Support_CrunchKey()
 * -> number of password bytes used
 * -> number of salt bytes
 * -> demanded key size
 * -> chrunch method (see CRUNCHKEY_METHOD_xxx) 
 * <- size of the build buffer
 */

WORD32 CRYPTPAK_API Support_GetCrunchKeyBuildBufSize(WORD32, WORD32, WORD32, WORD8);


/*
 * hashes a (salt and) password down to a defined key size
 * -> pointer to password
 * -> number of password bytes used
 * -> pointer to salt bytes (may be NULL)
 * -> number of salt bytes
 * -> pointer to output buffer
 * -> demanded key size
 * -> chrunch method (see CRUNCHKEY_METHOD_xxx) 
 * -> pointer to a build buffer with the size determined by 
 *    Support_GetChrunchKeyBuildBufSize(), may be NULL
 * <- BOOL_TRUE: success / BOOL_FALSE: out of memory
 */
BYTEBOOL CRYPTPAK_API Support_CrunchKey(const void*, WORD32, const void*, WORD32, 
                                        void*, WORD32, WORD8, void*);


#ifdef __cplusplus
}
#endif


#endif
