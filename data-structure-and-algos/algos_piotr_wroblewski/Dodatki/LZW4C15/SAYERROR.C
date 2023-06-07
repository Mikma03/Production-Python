/* sayerror.c */

#include <stdio.h>
#include "LZW4C.H"
#include "SAYERROR.H"

void SayError(int Code)
{switch(Code)
  {case EXPANSION_ERROR:
     puts("\nExpansion Error: Can only expand a previously compressed file");
     break;
   case CANNOT_ALLOCATE:
     puts("\nAllocation Error: Could not allocate sufficient memory");
     break;
   case INTERNAL_ERROR:
     puts("\nInternal Error: LZW4C object code modified !");
     break;
   case NOT_INITIALIZED:
     puts("\nNot Initialized Error: Must run InitLZW() first");
     break;
   case BAD_BITCODE:
     puts("\nBit Code Error: Must be 12, 13, or 14");
     break;
   default:
     printf("\nUnknown error returned = %d [%xH]\n",Code,Code);
     break;
  }
}