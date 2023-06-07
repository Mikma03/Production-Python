

#include <stdio.h>
#include <memory.h>

#include "TestInterface.h"



#define TESTBUFSIZE 256


void TestRandomPool
  (CTestStdOut* tso)
{
  static char as[] = "This is not important, but just confusing...";

  int nI;
  PRANDOMPOOLCTX rctx1, rctx2;
  WORD8 testbuf[TESTBUFSIZE];

  tso->Puts("random, the first...");

  rctx1 = RandomPool_Create(as, sizeof(as));

  RandomPool_GetData(rctx1, testbuf, TESTBUFSIZE);

  nI = 0;
  while (nI < TESTBUFSIZE)
  {
    tso->PrintF("%02x", testbuf[nI++]);
	if (0 == (nI % 40)) tso->Puts("");
  }
  tso->Puts("\n");

  tso->Puts("random, the second...");

  rctx2 = RandomPool_Create(NULL, 0);

  RandomPool_GetData(rctx2, testbuf, TESTBUFSIZE);

  nI = 0;
  while (nI < TESTBUFSIZE)
  {
    tso->PrintF("%02x", testbuf[nI++]);
	if (0 == (nI % 40)) tso->Puts("");
  }
  tso->Puts("\n");

  RandomPool_Destroy(rctx2);
  RandomPool_Destroy(rctx1);
}

