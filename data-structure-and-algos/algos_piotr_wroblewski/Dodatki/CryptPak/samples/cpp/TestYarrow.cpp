
#include <stdio.h>
#include <memory.h>

#include "TestInterface.h"


#define TESTBUFSIZE 1024

void TestYarrow
  (CTestStdOut* tso) 
{
  int nI;

  PYARROWCTX rctx1, rctx2;
 
  WORD8 testbuf[TESTBUFSIZE];
  
  char as[] = "This is not important, but just confusing...";

  tso->Puts("random, the first...");
  
  rctx1 = Yarrow_Create(as, sizeof(as));
  
  Yarrow_GetData(rctx1, testbuf, TESTBUFSIZE);
  
  nI = 0;
  while (nI < TESTBUFSIZE)
  {
    tso->PrintF("%02x", testbuf[nI++]);
	if (0 == (nI % 40)) tso->Puts("");
  }
  tso->Puts("\n");

  tso->Puts("random, the second...");

  rctx2 = Yarrow_Create(NULL, 0);
  
  Yarrow_GetData(rctx2, testbuf, TESTBUFSIZE);

  nI = 0;
  while (nI < TESTBUFSIZE)
  {
    tso->PrintF("%02x", testbuf[nI++]);
	if (0 == (nI % 40)) tso->Puts("");
  }
  tso->Puts("\n");

  Yarrow_Destroy(rctx2);
  Yarrow_Destroy(rctx1);
}

