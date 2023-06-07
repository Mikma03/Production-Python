

#ifndef __CIPHERSERVER_H
#define __CIPHERSERVER_H


#ifdef __cplusplus
extern "C" {
#endif

#include "cpconfig.h"

#include "CipherDef.h"



// error codes
#define CIPHERSERVER_ERROR_NOERROR              0
#define CIPHERSERVER_ERROR_ERROR                1
#define CIPHERSERVER_ERROR_INVALIDCIPHER        2
#define CIPHERSERVER_ERROR_OUTOFMEMORY          3
#define CIPHERSERVER_ERROR_WEAKKEY              4
#define CIPHERSERVER_ERROR_CIPHERNOTFOUND       5
 


// crypt modes
#define CIPHERSERVER_MODE_ENCRYPT   CIPHER_MODE_ENCRYPT
#define CIPHERSERVER_MODE_DECRYPT   CIPHER_MODE_DECRYPT



// work context, stores everything for cryptcipher session
typedef struct CIPHERCTX  CIPHERCTX, *PCIPHERCTX;


// the handle for an encryption session
typedef struct CIPHERSESSION  CIPHERSESSION, *PCIPHERSESSION;



/*
 * returns the names of all supported ciphers
 * -> where to store the pointer to the list (readonly)
 * <- number of supported ciphers
 */
WORD32 CRYPTPAK_API 
    CipherServer_GetCipherNames (char***);



/*
 * returns a cipher's information block
 * -> cipher name
 * -> pointer to where to store the data
 * <- error code:
 *    CIPHERSERVER_ERROR_NOERROR        : success
 *    CIPHERSERVER_ERROR_INVALIDCIPHER  : cipher is not valid
 *    CIPHERSERVER_ERROR_CIPHERNOTFOUND : cipher could not be found
 */
WORD32 CRYPTPAK_API 
    CipherServer_GetCipherInfo (const char*, CIPHERINFOBLOCK*);



/*
 * loads a cipher
 * -> cipher name
 * -> pointer where to store the context pointer 
 * -> pointer to random generator function (may be CIPHER_NULL, if so
 *    an internal random generator is going to be used)
 * -> general pointer for random generator function, e.g. to point
 *    to an object instance (ignored if pRandGenFunc is CIPHER_NULL)
 * -> pointer to random seed data (only used for the internal random generator,
 *    ignored if pRandGenFunc differs from CIPHER_NULL, may also be CIPHER_NULL)
 * -> number of random seed bytes (ignored if pRandSeed is CIPHER_NULL)
 * <- error code:
 *    CIPHERSERVER_ERROR_NOERROR        : success
 *    CIPHERSERVER_ERROR_OUTOFMEMORY    : not enough memory
 *    CIPHERSERVER_ERROR_CIPHERNOTFOUND : cipher could not be found
 *    CIPHERSERVER_ERROR_INVALIDCIPHER  : cipher is not valid
 */
WORD32 CRYPTPAK_API 
    CipherServer_Create (const char*, PCIPHERCTX*, Cipher_RandomGenerator*,
                         const void*, const void*, WORD32);
/*
 * unloads a cipher, clears and frees the context
 * -> cipher context handle
 * <- error code:
 *    CIPHERSERVER_ERROR_NOERROR : success
 *    CIPHERSERVER_ERROR_ERROR   : unloading (fatal) error
  */
WORD32 CRYPTPAK_API 
    CipherServer_Destroy (PCIPHERCTX);



/*
 * executes the selftest function of an already
 * loaded cipher, this guarantees that the cipher
 * cannot be altered between selftest and usage
 * -> cipher context handle
 * -> flag for extended testing (testing with own data)
 * <- error code:
 *    CIPHERSERVER_ERROR_NOERROR       : success
 *    CIPHERSERVER_ERROR_INVALIDCIPHER : cipher is not valid
 *    CIPHERSERVER_ERROR_OUTOFMEMORY   : not enough memory
 */
WORD32 CRYPTPAK_API 
    CipherServer_ExecuteSelfTest(PCIPHERCTX, BYTEBOOL);



/*
 * returns the information block of the cipher
 * -> pDrvCtx cipher context handle
 * -> pInfoBlock pointer to block where to store the data
 * <- error code:
 * CIPHER_ERROR_NOERROR       : cipher declares itself as valid
 * CIPHER_ERROR_ERROR         : unknown error code (invalid cipher)
 * CIPHER_ERROR_INVALIDCIPHER : cipher declares itself as invalid
 */
WORD32 CRYPTPAK_API 
    CipherServer_GetInfoBlock(PCIPHERCTX, CIPHERINFOBLOCK*);



/*
 * creates a new session for encrypting or decrypting data
 * -> work mode, see CIPHERSERVER_MODE_xxx constants
 * -> pointer to key stored a byte buffer
 * -> key size in bytes (must fit to the cipher, if demanded)
 * -> cipher handle
 * -> pointer where to get/set the init. data (usually a CBC IV)
 * -> pointer to the storage of the created session handle
 * <- error code:
 *    CIPHERSERVER_ERROR_NOERROR     : success
 *    CIPHERSERVER_ERROR_ERROR       : key setup failed
 *    CIPHERSERVER_ERROR_OUTOFMEMORY : not enough memory
 *    CIPHERSERVER_ERROR_WEAKKEY     : weak key detected
 */
WORD32 CRYPTPAK_API 
    CipherServer_OpenSession (WORD32, const WORD8*, WORD32,
                              PCIPHERCTX, void*, PCIPHERSESSION*);


/*
 * allows an interruption of the en-/decryption stream
 * without a timeconsuming new key setup (mostly used
 * to set a new CBC IV, if any, to allow chunking)
 * -> cryptsession handle
 * -> pointer where to get/set the init. data (usually a CBC IV)
 */
void CRYPTPAK_API 
    CipherServer_ResetSession (PCIPHERSESSION, void*);


/*
 * destroys a session handle
 * -> cryptsession handle
 * <- error code:
 *    CIPHERSERVER_ERROR_NOERROR : success
 *    CIPHERSERVER_ERROR_ERROR   : cipher couldn't stop properly (fatal error)
 */
WORD32 CRYPTPAK_API 
    CipherServer_CloseSession (PCIPHERSESSION);



/*
 * encrypts a number of blocks
 * -> cryptsession handle
 * -> pointer to the source buffer (may be equal to the source buffer)
 * -> pointer to the target buffer
 * -> number of _blocks_ to encrypt
 */
void CRYPTPAK_API 
    CipherServer_EncryptBlocks (PCIPHERSESSION, const void*, void*, WORD32);


/*
 * decrypts a number of blocks
 * -> cryptsession handle
 * -> pointer to the source buffer
 * -> pointer to the target buffer (may be equal to the source buffer)
 * -> number of _blocks_ to decrypt
 * -> pointer to previous block (ignored if CIPHER_NULL)
 */
void CRYPTPAK_API 
    CipherServer_DecryptBlocks (PCIPHERSESSION, const void*, void*, WORD32, const void*);


/*
 * delivers random data from the current generator
 * -> cryptcipher handle
 * -> pointer to the output buffer
 * -> number of random bytes to deliver
 */
void CRYPTPAK_API 
    CipherServer_GetRandomData (PCIPHERCTX, void*, WORD32);



// this is an undocumented function allowing us to 
// clear the current triple-DES CBC IV (so it can
// be run in ECB mode, used for an external Yarrow
// implementation)
// -> the triple-DES session
void CRYPTPAK_API clear_tdes_cbciv(PCIPHERSESSION); 


#ifdef __cplusplus
}
#endif


#endif

