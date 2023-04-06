/*
**  EXPAND.C      Copyright (C) 1992 by MarshallSoft Computing, Inc.
**
**  Expands file previously compressed with COMPRESS.
**  Usage is:  EXPAND <input_file> <output_file>
*/

#include <stdio.h>
#include <stdlib.h>
#include "LZW4C.H"
#include "RW_IO.H"
#include "SAYERROR.H"

#define FALSE 0
#define TRUE !FALSE

void main(int argc,char *argv[])
{int RetCode;
 /* begin */
 if(argc<3)
   {printf("Useage: EXPAND <infile> <outfile>\n");
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
 /* expand the compressed file */
 printf("Expanding %s",argv[1]);
 if((RetCode=Expand(Reader,Writer))<0)
   {SayError(RetCode);
    exit(3);
   }
 /* close files */
 ReaderClose();
 WriterClose();
 TermLZW(free);
}