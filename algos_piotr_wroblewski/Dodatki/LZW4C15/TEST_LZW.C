/*
**   TEST_LZW.C       Copyright (C) 1992 by MarshallSoft Computing, Inc.
**
**   This program is used to compress, expand, and verify each specified
**   file. It's purpose is for you to test the LZW4C library on your own
**   files. Your files are never modified. However, you should NOT have a
**   file named "XXX.XXX" or "YYY.YYY".  Compression ratios are printed
**   for each file compressed. For example, to compress all files ending
**   in *.C in your current directory, type:
**
**        TEST_LZW *.c
*/

#include <stdio.h>
#include <dos.h>
#include <fcntl.h>
#include <sys\types.h>
#include <sys\stat.h>
#include <io.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <conio.h>

#include "RW_IO.H"
#include "LZW4C.H"
#include "DIR_IO.H"
#include "SAYERROR.H"

FILE *FilePtr1;
FILE *FilePtr2;

void main(int argc,char *argv[])
{int i, k;            /* loop counters */
 int x, y;            /* last bytes read during compare */
 int RetCode;         /* return code */
 float Ratio;         /* compression ratio */
 long Index;          /* byte count */
 char Filename[15];   /* next filename */
 int Files = 0;       /* # files compressed/expanded */
 int BitCode;         /* 12, 13, or 14 */
 /* begin */
 switch(argc)
   {case 2:
      /* preferred value = 14 bits */
      BitCode = 14;
      break;
    case 3:
      /* get bit code value from command line */
      BitCode = atoi(argv[2]);
      break;
    default:
      printf("Usage: TEST_LZW <filespec> {<bitcode>}\n");
      exit(1);
   }
 /* use 9 to <BitCode> bit codes */
 RetCode = InitLZW(malloc,BitCode);
 if(RetCode<0)
   {SayError(RetCode);
    exit(2);
   }
 /* flush the keyboard */
 puts("\nTEST_LZW 1.1: Type any key to abort...");
 for(i=0;;i++)
   {if(kbhit())
      {puts("\n...Aborted by user !");
       break;
      }
    /* get next filename */
    if(i==0) RetCode = FindFirst(argv[1],Filename);
    else RetCode = FindNext(Filename);
    if(!RetCode) break;
    /* force to uppercase */
    for(k=0;k<strlen(Filename);k++) Filename[i] = toupper(Filename[i]);
    /* skip 'work' files XXX.XXX and YYY.YYY */
    if( (strcmp(Filename,"XXX.XXX")==0) ||
        (strcmp(Filename,"YYY.YYY")==0) ) continue;
    /* open input file for compression */
    if(!ReaderOpen(Filename)) exit(3);
    /* open output file for compression */
    if(!WriterOpen("XXX.XXX")) exit(4);
    /* do the compression */
    Files++;
    printf("\nCompressing %12s ",Filename);
    if((RetCode=Compress(Reader,Writer))<0)
      {SayError(RetCode);
       exit(5);
      }
    /* report compression ratio */
    if(ReaderCount() > 0)
       {Ratio = (float)(WriterCount())/(float)ReaderCount();
        printf(" OK (%0.2f)\n",Ratio);
       }
    else puts("???");
    /* close files */
    ReaderClose();
    WriterClose();
    /* open input file for expansion */
    if(!ReaderOpen("XXX.XXX")) exit(6);
    /* open output file for expansion */
    if(!WriterOpen("YYY.YYY")) exit(7);
    /* do the expansion */
    printf("  Expanding %12s ",Filename);
    if((RetCode=Expand(Reader,Writer))<0)
      {printf("Expand returns error %d\n",RetCode);
      }
    /* close files */
    ReaderClose();
    WriterClose();
    printf(" OK\n");
    /* compare original to expanded file */
    FilePtr1 = fopen(Filename,"rb");
    FilePtr2 = fopen("YYY.YYY","rb");
    printf("  Comparing              ");
    Index = 0;
    while(1)
      {x = fgetc(FilePtr1);
       y = fgetc(FilePtr2);
       Index++;
       /* print dot every 4K bytes */
       if((Index&0x0fff)==0) putchar('.');
       if((x==EOF)&&(y==EOF)) break;
       if(x!=y)
         {printf("ERROR: Difference between files at index %ld\n",Index-1);
          exit(8);
         }
      }
    printf(" OK\n");
    fclose(FilePtr1);
    fclose(FilePtr2);
   }
 /* all done */
 TermLZW(free);
 printf("\n%d files tested\n",Files);
 exit(0);
}