/*
**  COMPRESS.C      Copyright (C) 1992 by MarshallSoft Computing, Inc.
**
**  Compresses specified file. Use EXPAND to un-compress file.
**  Usage is:  COMPRESS <input_file> <output_file>
*/

#include <stdio.h>
#include <stdlib.h>
#include "LZW4C.H"
#include "RW_IO.H"
#include "SAYERROR.H"

void main(int argc, char *argv[])
{int RetCode;
 float Ratio;
 /* begin */
 if(argc<3)
    {printf("Usage: COMPRESS <infile> <outfile>\n");
     exit(1);
    }
 if((RetCode=InitLZW(malloc,14))<0)
    {SayError(RetCode);
     exit(2);
    }
 /* open input file */
 if(!ReaderOpen(argv[1])) exit(3);
 /* open output file */
 if(!WriterOpen(argv[2])) exit(4);
 printf("Compressing %s ",argv[1]);
 /* do the compression */
 if((RetCode=Compress(Reader,Writer))<0)
   {SayError(RetCode);
    exit(3);
   }
 if(ReaderCount() > 0)
   {Ratio = (float)(WriterCount())/(float)ReaderCount();
    printf(" %0.2f\n",Ratio);
   }
 /* close files */
 ReaderClose();
 WriterClose();
 TermLZW(free);
}