

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "TestInterface.h"


// speed test parameters

#define BLOCKSPERBUF    60000
#define BENCHLOOPS      40


#define NO_USER_INPUT
#define NO_BENCHMARK



void PrintInfoBlock
  (CTestStdOut* tso,
   CIPHERINFOBLOCK* infoblock)
{
  tso->PrintF("block size      : %d\n"\
			  "key size        : %d\n"\
			  "hashes key      : %d\n"\
			  "init. data size : %d\n"\
			  "context size    : %d\n"\
			  "sizeof          : %d\n"\
			  "cipher is       : 0x%02x\n",
			  infoblock->lBlockSize,
			  infoblock->lKeySize,
			  infoblock->blOwnHasher,
			  infoblock->lInitDataSize,
			  infoblock->lContextSize,
			  infoblock->lSizeOf,
			  infoblock->bCipherIs);
}



// keep the stack small in TestCipherServer(), so do the big
// things globally (makes this routine single threaded only)

WORD8 _key[65536];
WORD8 _inbuf[65536];
WORD8 _outbuf[65536];
WORD8 _lastbuf[65536];


void TestCipherServer
  (CTestStdOut* tso)
{
  int nI;
  int nNumOfCiphers;
  WORD32 lI;
  WORD32 lResult;
  WORD32 lKeySize;
  char** cipherNames;
  WORD8* pInitData;
  PCIPHERCTX pCtx;
  PCIPHERSESSION chandle;
  CIPHERINFOBLOCK infoblock;
  WORD8 rndbuf[8];
#ifndef NO_BENCHMARK
  void* benchbuf;
  clock_t starttime;
  WORD64 qRate;
#endif


  nNumOfCiphers = CipherServer_GetCipherNames(&cipherNames);
  tso->PrintF("%d ciphers available.\n\n", nNumOfCiphers);

  for (nI = 0; nI < nNumOfCiphers; nI++)
  {
    tso->PrintF("testing \"%s\" ...\n", cipherNames[nI]);

    // show cipher information
    infoblock.lSizeOf = sizeof(CIPHERINFOBLOCK);

    lResult = CipherServer_GetCipherInfo(cipherNames[nI],
		                                 &infoblock);

	if (lResult != CIPHERSERVER_ERROR_NOERROR)
    {
      tso->PrintF("ERROR #%d\n", lResult);
      return;
    }
    PrintInfoBlock(tso, &infoblock);


    // open the cipher (using the built-in random generator with no additional seed)

	lResult = CipherServer_Create(cipherNames[nI],
		                          &pCtx,
								  NULL,
								  NULL,
								  NULL,
								  0);

    if (lResult != CIPHERSERVER_ERROR_NOERROR)
    {
      tso->PrintF("ERROR #%d\n", lResult);
      return;
    }

    // execute the cipher's self test

    lResult = CipherServer_ExecuteSelfTest(pCtx,
		                                   BOOL_TRUE);

	if (lResult != CIPHERSERVER_ERROR_NOERROR)
    {
      tso->PrintF("ERROR #%d\n", lResult);
      CipherServer_Destroy(pCtx);
      return;
    }
    tso->Puts("extended selftest passed.");

    // get the cipher's information block

    tso->Puts("direct information block readout:");
    
	lResult = CipherServer_GetInfoBlock(pCtx, 
		                                &infoblock);

	if (lResult != CIPHERSERVER_ERROR_NOERROR)
    {
      tso->PrintF("ERROR #%d\n", lResult);
      CipherServer_Destroy(pCtx);
      return;
    }
    PrintInfoBlock(tso, &infoblock);

//////////////

    // open a new session for encryption, using a simply created key
	lKeySize = (infoblock.blOwnHasher) ? 1024 : infoblock.lKeySize;

    for (lI = 0; lI < lKeySize; lI++) 
	{	
	  _key[lI] = (WORD8)(lI & 0x0ff);
	}

    pInitData = (WORD8*) malloc(infoblock.lInitDataSize);
  
	lResult = CipherServer_OpenSession(CIPHERSERVER_MODE_ENCRYPT,
                                       _key,
                                       lKeySize,
                                       pCtx,
                                       pInitData,
                                       &chandle);
    
	if (lResult != CIPHERSERVER_ERROR_NOERROR)
    {
      tso->PrintF("ERROR #%d\n", lResult);
      CipherServer_Destroy(pCtx);
      free(pInitData);
      return;
    }

    if (infoblock.lInitDataSize)
    {
      tso->PrintF("init. data returned by the cipher: ");
    
	  for (lI = 0; lI < infoblock.lInitDataSize; lI++)
	  {
        tso->PrintF("%02x ", pInitData[lI]);
      }
	  tso->Puts("");
    }

    // get some test data from the user

#ifdef NO_USER_INPUT
    strcpy((char*)_inbuf, "something to encrypt and decrypt");
#else
    tso->PrintF("enter something >");
    gets((char*) _inbuf);
#endif

    // (don't forget the ending zero -> + 1)
    int nNumOfBlocks = strlen((char*)_inbuf) + 1;

    if (nNumOfBlocks % infoblock.lBlockSize)
	{
      nNumOfBlocks = nNumOfBlocks / infoblock.lBlockSize + 1;
	}
    else
	{
      nNumOfBlocks /= infoblock.lBlockSize;
	}
    
	tso->PrintF("number of %d byte blocks = %d\n",
                infoblock.lBlockSize, 
				nNumOfBlocks);

    // encrypt this data

    CipherServer_EncryptBlocks(chandle, _inbuf, _outbuf, nNumOfBlocks);
    
	tso->PrintF("encrypted message: ");
    
	for (lI = 0; lI < nNumOfBlocks * infoblock.lBlockSize; lI++)
    {
      tso->PrintF("%02x", _outbuf[lI]);
      if (0 == ((lI + 1) % infoblock.lBlockSize))
	  {
        tso->PrintF(" ");
	  }
    }
    tso->Puts("");

    // close the session

    lResult = CipherServer_CloseSession(chandle);
    
	if (lResult != CIPHERSERVER_ERROR_NOERROR)
    {
      tso->PrintF("ERROR #%d\n", lResult);
      CipherServer_Destroy(pCtx);
      free(pInitData);
      return;
    }

    // open a session for decryption
    lResult = CipherServer_OpenSession(CIPHERSERVER_MODE_DECRYPT,
                                       _key,
                                       lKeySize,
                                       pCtx,
                                       pInitData,
                                       &chandle);
    
	if (lResult != CIPHERSERVER_ERROR_NOERROR)
    {
      tso->PrintF("ERROR #%d\n", lResult);
      CipherServer_Destroy(pCtx);
      free(pInitData);
      return;
    }

    // reset before decrypting, just for fun here
    
	CipherServer_ResetSession(chandle, pInitData);

    // decrypt the data, interrupt after the first block, if possible
    
    if (nNumOfBlocks < 2)
	{
      CipherServer_DecryptBlocks(chandle, 
		                         _outbuf, 
								 _lastbuf, 
								 nNumOfBlocks, 
								 CIPHER_NULL);
	}
    else
    {
      CipherServer_DecryptBlocks(chandle, 
		                         _outbuf, 
								 _lastbuf, 
								 1, 
								 CIPHER_NULL);
      
	  CipherServer_DecryptBlocks(chandle, 
		                          &_outbuf[infoblock.lBlockSize],
                                 &_lastbuf[infoblock.lBlockSize],
                                 nNumOfBlocks - 1, 
								 _outbuf);
    }
    tso->PrintF("decrypted message: >>>%s<<<\n", (char*) _lastbuf);

    // close the session

    lResult = CipherServer_CloseSession(chandle);
    
	if (lResult != CIPHERSERVER_ERROR_NOERROR)
    {
      tso->PrintF("ERROR #%d\n", lResult);
      CipherServer_Destroy(pCtx);
      free(pInitData);
      return;
    }

    // get some random bytes
    
    CipherServer_GetRandomData(pCtx, 
		                       rndbuf, 
							   8);

    tso->PrintF("random bytes from the internal generator : "\
                "%02x %02x %02x %02x %02x %02x %02x %02x\n",
                rndbuf[0], rndbuf[1], rndbuf[2], rndbuf[3],
                rndbuf[4], rndbuf[5], rndbuf[6], rndbuf[7]);

    // speed tests with a big buffer

#ifndef NO_BENCHMARK
#ifndef NO_USER_INPUT
    tso->Puts("Execute benchmark [y/n]?");
    if (getchhar() == 'y')
#endif
    {
	  benchbuf = malloc(BLOCKSPERBUF * infoblock.lBlockSize);

      lResult = CipherServer_OpenSession(CIPHERSERVER_MODE_ENCRYPT,
                                         key,
                                         lKeySize,
                                         pCtx,
                                         pInitData,
                                         &chandle);

      if (lResult != CIPHERSERVER_ERROR_NOERROR)
      {
        tso->PrintF("ERROR #%d\n", lResult);
        CipherServer_Destroy(pCtx);
        free(benchbuf);
        free(pInitData);
        return;
      }

      tso->PrintF("running benchmark (%d bytes per hash) ...\n",
                  BLOCKSPERBUF * infoblock.lBlockSize);

      starttime = clock();
      
	  for (int nI = 0; nI < BENCHLOOPS; nI++)
      {
        CipherServer_EncryptBlocks(chandle, 
			                       benchbuf, 
								   benchbuf, 
								   BLOCKSPERBUF);
        tso->PrintF("#");
      }

      starttime = clock() - starttime;
      
	  qRate = (WORD64)(BLOCKSPERBUF * infoblock.lBlockSize) * BENCHLOOPS;
      
	  qRate *= CLK_TCK;
      
	  if (starttime)
      {
        tso->PrintF("\n%d bytes/sec\n", qRate / starttime);
      }
      else
      {
        tso->Puts("\ntoo fast");
      }
      free(benchbuf);

      lResult = CipherServer_CloseSession(chandle);

      if (lResult != CIPHERSERVER_ERROR_NOERROR)
      {
        tso->PrintF("ERROR #%d\n", lResult);
        CipherServer_Destroy(pCtx);
        free(pInitData);
        return;
      }
    }
#endif

	// free the init. data buffer
    free(pInitData);

    // close the cipher
    
	lResult = CipherServer_Destroy(pCtx);
    
	if (lResult != CIPHERSERVER_ERROR_NOERROR)
    {
      tso->PrintF("ERROR #%d\n", lResult);
      return;
    }

#ifndef NO_USER_INPUT
    if (nI < (nNumOfCiphers - 1))
    {
      tso->Puts("\nTest next cipher [y/n]?");
      if (getchhar() != 'y') break;
    }
#endif
 
  }
}
