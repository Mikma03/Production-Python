

#include <stdio.h>
#include <string.h>

#include "TestInterface.h"


void TestCRC32
  (CTestStdOut* tso)
{
    // test zero string

    char zerostring[] = "";

    WORD32 lCRC32 = CRC32_INITVALUE;
    tso->Puts("checksumming zero string...");

    CRC32_Update(lCRC32, zerostring, 0);
    lCRC32 ^= CRC32_DONEVALUE;

    tso->PrintF("CRC32 -> 0x%08x\n", lCRC32);


    // checksumming the reference string

    char refstring[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZäöüÄÖÜ0123456789";

    lCRC32 = CRC32_INITVALUE;
    tso->Puts("checksumming reference string...");

    lCRC32 = CRC32_Update(lCRC32, refstring, strlen(refstring));
    lCRC32 ^= CRC32_DONEVALUE;

    tso->PrintF("CRC32 -> 0x%08x\n", lCRC32);
}
