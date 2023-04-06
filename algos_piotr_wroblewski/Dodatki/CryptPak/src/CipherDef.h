

#ifndef __CIPHERDEF_H
#define __CIPHERDEF_H


#include "cpconfig.h"
#include "BasicTypes.h"


// to be sure we define our own NULL pointer value
#define  CIPHER_NULL        0


// the following constants describe a cipher's characteristic (bitmask)

// cipher is a stream cipher xoring (stream is plaintext
// independant) the plaintext
#define CIPHER_IS_XORSTREAM     1

// cipher is blockcipher, enabling single read and write block access (ECB)
#define CIPHER_IS_BLOCK         2

// cipher is blockcipher, enabling single read-only block access (CBC)
#define CIPHER_IS_BLOCKLINK     4

// cipher doesn't allow block access, but does also not simply
// xor the key stream over the plaintext (multiple streams can
// be used with the same key and some known plaintext also)
#define CIPHER_IS_NOBLOCK       8

// cipher is insecure, for debug purposes only, beta, whatever
#define CIPHER_IS_DEBUG       128




// error codes
#define CIPHER_ERROR_NOERROR            0
#define CIPHER_ERROR_INVALID            1
#define CIPHER_ERROR_KEYSETUPERROR      2
#define CIPHER_ERROR_WEAKKEY            3  // (this must only be a warning)
#define CIPHER_ERROR_DESTRUCTERROR      4


// work modes
#define CIPHER_MODE_ENCRYPT 0
#define CIPHER_MODE_DECRYPT 1


// max. length of a cipher title
#define CIPHER_MAX_NAME_LEN     32


// the following structure is returned by Cipher_GetInfo()
#pragma pack(push, 1)
typedef struct
{
   // size of this structure, must be set by the caller,
   // used for future extensions
   WORD32 lSizeOf;

   // size of one cipher block in bytes,
   // a stream cipher must return 1
   WORD32 lBlockSize;

   // key size. Can be 0, e.g. for individual
   // DLLs simulating a keycard.
   WORD32 lKeySize;

   // size of the initialisation data in bytes,
   // e.g. 8 for a 64bit block cipher in CBC mode (IV) or 0 for any
   // block cipher in ECB mode
   WORD32 lInitDataSize;

   // size of a work context, necessary for a proper multitasking.
   // Every caller's actual state is stored in a context, e.g. the
   // actual IV or pbox/sbox contents.
   WORD32 lContextSize;

    // the type of this cipher (see CIPHER_CIPHERIS_xxx)
   WORD8 bCipherIs;

   // Does the cipher hash the password by its own routines?
   // BOOL_FALSE: the application must deliver a key already hashed
   //             to nKeySize bytes
   // BOOL_TRUE : the cipher gets the raw password
   BYTEBOOL blOwnHasher;
}
CIPHERINFOBLOCK;
#pragma pack(pop)


// to avoid that the cipher must create necessary random numbers itself
// we define a function type which delivers a number of random bytes


/*
 * address of a function which creates cryptographic secure random numbers
 * -> pointer to buffer where to place the random values
 * -> number of required random bytes
 * -> general pointer for multithreading support
 */
typedef void CRYPTPAK_CALLCONV Cipher_RandomGenerator(WORD8*, WORD32, const void*);


/*
 * to get a cipher's characteristics
 * -> pointer where to store the informations, it's the cipher's job to
 *    check the CIPHERINFOBLOCK.wSizeOfMember first to deliver only that
 *    much bytes which fit into the given memory block!
 * <- error code:
 * CIPHER_ERROR_NOERROR - cipher declares itself as valid
 * CIPHER_ERROR_INVALID - cipher declares itself as invalid
 */
typedef WORD32 Cipher_GetCipherInfo(CIPHERINFOBLOCK*);


/*
 * to start a self-test of the cipher
 * -> pointer to a memory block of CIPHERINFOBLOCK.lContextSize
 *    to store a context for the tests. Memory block is allocated by the
 *    caller and should be cleared and freed after the function call.
 *    The self test was separated to give the caller a chance no to use it,
 *    e.g. if the test takes to much time.
 * <- error code:
 * CIPHER_ERROR_NOERROR - selftest succeeded
 * CIPHER_ERROR_INVALID - selftest failed
 */
typedef WORD32 Cipher_SelfTest(void*);


/*
 * to create a work context
 * -> pointer to a memory block of CIPHERINFOBLOCK.lContextSize
 *    to store the work context. Memory block is allocated by the caller
 *    and is as long valid as encryption/decryption is necessary (if the
 *    process is finished the memory block should be cleared and freed).
 * -> pointer to an array of bytes representing the key/password. If
 *    CIPHERINFOBLOCK.blOwnHasher is BOOL_TRUE the array contains the
 *    raw password, if it's BOOL_FALSE the array contains the already hashed key
 *    with the size of CIPHERINFOBLOCK.wKeySize bytes.
 * -> length of the key/password. This parameter never will be zero and
 *    contains always the valid length, even if the password was already
 *    hashed to a key with the right size.
 * -> work mode, see CIPHER_MODE_xx constants
 * -> pointer to init. data storage
 * -> address of the random generator
 * -> general pointer passed to the random generator
 * <- error code:
 * CIPHER_ERROR_NOERROR       - key setup succeeded
 * CIPHER_ERROR_KEYSETUPERROR - key setup failed
 * CIPHER_ERROR_WEAKKEY       - success, but weak key detected
 */
typedef WORD32 Cipher_CreateWorkContext(void*, const WORD8*, WORD32, WORD32, void*,
                                        Cipher_RandomGenerator, const void*);


/*
 * resets a cipher, to avoid time consuming key setups
 * -> pointer to a work context, see above for further details
 * -> mode, see CIPHER_MODE_xx constants
 * -> pointer to init. data storage (for new en-/decryption)
 * -> address of the random generator
 * -> general pointer passed to the random generator
 */
typedef void Cipher_ResetWorkContext(void* pContext, WORD32, void*,
                                     Cipher_RandomGenerator, const void*);


/*
 * destroys a work context, usually not necessary, but might be e.g. when the
 * cipher allocates memory for every work context
 * -> pointer to a work context, see above for further details
 * <- error code:
 * CIPHER_ERROR_NOERROR       - destruction succeeded
 * CIPHER_ERROR_DESTRUCTERROR - destruction failed, this should force the
 *                              caller not to use the cipher again!
 */
typedef WORD32 Cipher_DestroyWorkContext(void*);


/*
 * encrypts a buffer content to a target buffer. The target buffer must be adjusted
 * to the block size and can be the same as the source buffer. The caller must be adjusted
 * to the number of bytes to the blocksize, so the cipher hasn't to do any padding.
 * -> pointer to a work context
 * -> pointer to the source buffer
 * -> pointer to the target buffer
 * -> number of bytes to encrypt
 */
typedef void Cipher_EncryptBuffer(void*, const void*, void*, WORD32);

/*
 * decrypts a buffer content to a target buffer. The target buffer must be adjusted to
 * the block size and can be the same as the source buffer.
 * -> pointer to a work context
 * -> pointer to the source buffer
 * -> pointer to the target buffer
 * -> number of bytes to decrypt
 * -> pointer to previous block, used to enable to decrypt
 *    even chained blocks, e.g. CBC (ignored if CIPHER_NULL),
 *    if you want to access the very first block a call
 *    to the Cipher_ResetWorkContext routine is necessary and
 *    the original init. data has to be replaced
 */
typedef void Cipher_DecryptBuffer(void*, const void*, void*, WORD32, const void*);


#endif


