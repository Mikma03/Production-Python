

#ifndef __TESTINTERFACE_H
#define __TESTINTERFACE_H


#include "CryptPak.h"


// generic output interface

class CTestStdOut
{
public:

  virtual void Puts(const char*) = 0;
  virtual void PrintF(const char*, ...) = 0;
};



// prototype of all test functions

void TestCipherServer(CTestStdOut*);
void TestCRC32(CTestStdOut*);
void TestCrunchKey(CTestStdOut*);
void TestLZSS(CTestStdOut*, const char*);
void TestRandomPool(CTestStdOut*);
void TestYarrow(CTestStdOut*);
void TestMD5(CTestStdOut*, const char*);
void TestSHA1(CTestStdOut*, const char*);


#endif
