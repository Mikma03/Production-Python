

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "TestInterface.h"



#define BUFSIZE     1024
#define KEYSIZE     47


#define NO_USER_INPUT


void PrintHexBuf
  (CTestStdOut* tso,
   WORD8* buf,
   int nNumOfBytes)
{
  for (int nI = 0; nI < nNumOfBytes; nI++)
  {
    tso->PrintF("%02x  ", buf[nI]);
  }
}



void TestCrunchKey
  (CTestStdOut* tso)
{
  char passw[BUFSIZE];
  char salt[BUFSIZE];
  WORD8 key[KEYSIZE];

#ifdef NO_USER_INPUT
  strcpy(passw, "the password.");
  strcpy(salt, "salt!salt!salt!");
#else
  tso->PrintF("password>");
  gets(passw);
  tso->PrintF("salt>");
  gets(salt);
#endif

  WORD32 lPasswLen = strlen(passw);
  WORD32 lSaltLen = strlen(salt);

  Support_CrunchKey(passw,
                    lPasswLen,
                    salt,
                    lSaltLen,
                    key,
                    KEYSIZE,
                    CRUNCHKEY_METHOD_SHAEXTXORLOOP,
                    NULL);

  PrintHexBuf(tso, key, KEYSIZE);
  tso->Puts("\n");

  WORD32 lBuildBufLen =
    Support_GetCrunchKeyBuildBufSize(lPasswLen,
                                     lSaltLen,
                                     KEYSIZE,
                                     CRUNCHKEY_METHOD_SHAEXTXORLOOP);

  void* pBuildBuf = malloc(lBuildBufLen);

  Support_CrunchKey(passw,
                    lPasswLen,
                    salt,
                    lSaltLen,
                    key,
                    KEYSIZE,
                    CRUNCHKEY_METHOD_SHAEXTXORLOOP,
                    pBuildBuf);

  PrintHexBuf(tso, key, KEYSIZE);

  free(pBuildBuf);

}
