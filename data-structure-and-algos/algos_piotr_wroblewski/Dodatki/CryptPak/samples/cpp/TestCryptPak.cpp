
#include <stdio.h>
#include <stdarg.h>

#include "TestInterface.h"


#define TESTFILE	"test.dat"


#define AUTOTESTFILE

// (undef this to use your own test file)
#ifdef AUTOTESTFILE

void MakeTestFile();
void MakeTestFile()
{
  FILE* tf = fopen(TESTFILE, "wb");
  if (tf)
  {
    fputs("//////////////////////////////////\n"\
		  "Something for CryptPak to test.\n"	\
		  "//////////////////////////////////", 
		  tf);
	fclose(tf);
  }
}

#endif




// simple mapper to stdout

class CTestStdOutImpl : public CTestStdOut
{
public:

  virtual void Puts 
    (const char* txt) 
  { 
	puts(txt);
  }

  virtual void PrintF
    (const char* fmt, ...)
  { 
    va_list lst;
    va_start(lst, fmt);
    vprintf(fmt, lst);
    va_end(lst);
  }
};



// (all the test together)

void main()
{
  CTestStdOutImpl tsoi;

#ifdef AUTOTESTFILE
  MakeTestFile();	
#endif

#ifndef CRYPTPAK_DLL
  CryptPak_Init();
#endif

  TestCipherServer(&tsoi);
  TestCRC32(&tsoi);
  TestCrunchKey(&tsoi);
  TestMD5(&tsoi, TESTFILE);
  TestSHA1(&tsoi, TESTFILE);
  TestRandomPool(&tsoi);
  TestYarrow(&tsoi);
  TestLZSS(&tsoi, TESTFILE);
}
