


#include "Support.h"
#include "BasicTypes.h"
#include "SHA1.h"
#include "cpkernel.h"

#include <stdlib.h>
#include <memory.h>


// the recent version of CryptPak
#define VERSION_MAJOR   4
#define VERSION_MINOR   5
#define VERSION_BUILT   0


WORD32 CRYPTPAK_API
  Support_GetVersion() 
{
  return (((WORD32) VERSION_MAJOR) << 24) |
         (((WORD32) VERSION_MINOR) << 16) |
         ((WORD32) VERSION_BUILT);

}



WORD32 CRYPTPAK_API Support_GetCrunchKeyBuildBufSize
  (WORD32 lPasswLen,
   WORD32 lSaltLen,
   WORD32 lOutputLen,
   WORD8 bMethod) 
{
  return lSaltLen + 
         lPasswLen +       
         SHA1_DIGESTSIZE * (lOutputLen / SHA1_DIGESTSIZE + 1);
}
                                        



BYTEBOOL CRYPTPAK_API Support_CrunchKey
  (const void* pPassw, 
   WORD32 lPasswLen, 
   const void* pSalt, 
   WORD32 lSaltLen, 
   void* pOutput, 
   WORD32 lOutputLen,
   WORD8 bMethod,
   void* pBuildBuf) 
{
  WORD8* outBuf = (WORD8*) pOutput;
  WORD8* buildBuf;
  WORD32 lBuildBufLen;
  WORD32 lBuildBufPos;
  WORD32 lRest;
  WORD32 lOutPos;
  BYTEBOOL blFirst = BOOL_TRUE;
  PSHA1CTX pCtx;
  WORD8 digest[SHA1_DIGESTSIZE];

  if (lOutputLen == 0) 
  {
    return BOOL_TRUE;
  }

  if (pSalt == NULL) 
  {
    lSaltLen = 0; 
  }

  // create the build buffer, if necessary
  if (pBuildBuf == NULL)
  {
    lBuildBufLen = Support_GetCrunchKeyBuildBufSize(lPasswLen, 
                                                    lSaltLen,
                                                    lOutputLen, 
                                                    bMethod);
    buildBuf = (WORD8*) malloc(lBuildBufLen);
    if (buildBuf == NULL) 
    {
      return BOOL_FALSE;   
    }
  }
  else  
  {
    buildBuf = (WORD8*) pBuildBuf;
  }

  // concat salt and key
  if (pSalt != NULL) 
  {
    memcpy(&buildBuf[0], 
           pSalt, 
           lSaltLen);
  }
  memcpy(&buildBuf[lSaltLen], 
         pPassw, 
         lPasswLen);
  lBuildBufPos = lSaltLen + lPasswLen;

  pCtx = SHA1_Create();

  lOutPos = 0;
  lRest = lOutputLen;
  
  do 
  {
    if (blFirst == BOOL_TRUE) 
    {
      blFirst = BOOL_FALSE;
    }
    else 
    {
      SHA1_Reset(pCtx);
    }

    SHA1_Update(pCtx, buildBuf, lBuildBufPos);
    SHA1_Final(digest, pCtx);

    // finished?
    if (lRest <= SHA1_DIGESTSIZE) 
    {
      memcpy(&outBuf[lOutPos], digest, lRest);

      // xor the rest of the last digest over the beginning of the output buffer?
      if (bMethod == CRUNCHKEY_METHOD_SHAEXTXORLOOP) 
      {
        lOutPos = 0;
        
        while (lRest < SHA1_DIGESTSIZE) 
        {
          outBuf[lOutPos++] ^= digest[lRest++];
          if (lOutPos == lOutputLen) 
          {
            lOutPos = 0;
          }
        }

      }
    
      break; // (out of do)

    }
    else 
    {
      memcpy(&outBuf[lOutPos], digest, SHA1_DIGESTSIZE);
      lOutPos += SHA1_DIGESTSIZE; 
      
      // append the new digest to the build buffer
      memcpy(&buildBuf[lBuildBufPos], digest, SHA1_DIGESTSIZE);
      memset(digest, 0, SHA1_DIGESTSIZE);
      lBuildBufPos += SHA1_DIGESTSIZE;

      lRest -= SHA1_DIGESTSIZE;
    }

  }
  while (1);

  SHA1_Destroy(pCtx);

  if (pBuildBuf == NULL) 
  {
    memset(buildBuf, 0, lBuildBufLen);
    free(buildBuf);
  }

  return BOOL_TRUE;
}
