/*
**   MK_ARC.C       Copyright (C) 1992 by MarshallSoft Computing, Inc.
**
**   This program is used to compress one or more files into a single
**   archive file. For example, to compress all files ending with the
**   extension '.C' into an archive named 'C.ARF', type:
**
**      MK_ARC *.C C.ARF
*/

#include <stdio.h>
#include <stdlib.h>
#include <dos.h>
#include <fcntl.h>
#include <sys\types.h>
#include <sys\stat.h>
#include <io.h>
#include <string.h>
#include <conio.h>
#include <ctype.h>

#include "LZW4C.H"
#include "RW_IO.H"
#include "DIR_IO.H"
#include "SAYERROR.H"

void main(int argc, char *argv[])
{int i, k;
 int RetCode;
 float Ratio;
 long TotalCount = 0;
 char Filename[15];
 int Files = 0;
 char *Ptr;
 /* begin */
 if(argc!=3)
   {printf("Usage: MK_ARC <filespec> <archive_file_name>\n");
    exit(1);
   }
 RetCode = InitLZW(malloc,14);
 if(RetCode<0)
   {SayError(RetCode);
    exit(2);
   }
 /* flush the keyboard */
 puts("\nMK_ARC 1.0: Type any key to abort...");
 /* open output file for compression */
 Ptr = argv[2];
 for(i=0;i<strlen(Ptr);i++) Ptr[i] = toupper(Ptr[i]);
 if(!WriterOpen(Ptr)) exit(4);
 for(i=0;;i++)
   {if(kbhit())
      {puts("\n...Aborted by user !");
       break;
      }
    if(i==0) RetCode = FindFirst(argv[1],Filename);
    else RetCode = FindNext(Filename);
    if(!RetCode) break;
    /* make filename upper case */
    for(k=0;k<strlen(Filename);k++) Filename[i] = toupper(Filename[i]);
    /* open input file for compression */
    if(strcmp(Filename,Ptr)==0)
      {printf("WARNING: Compress file same as archive file = %s (skipping)\n",
         Filename);
       continue;
      }
    if(!ReaderOpen(Filename)) exit(3);
    /* write filename to output file */
    Writer('\0');
    for(k=0;k<strlen(Filename);k++) Writer(Filename[k]);
    Writer('\0');
    /* do the compression */
    Files++;
    printf("Compressing %12s ",Filename);
    if((RetCode=Compress(Reader,Writer))<0)
      {SayError(RetCode);
       exit(5);
      }
    /* report compression ratio */
    if(ReaderCount() > 0)
       {Ratio = (float)(WriterCount()-TotalCount)/(float)ReaderCount();
        printf(" OK (%0.2f)\n",Ratio);
        TotalCount = WriterCount();
       }
    else puts("???");
    /* close file */
    ReaderClose();
   }
 WriterClose();
 TermLZW(free);
 printf("\n%d files compressed\n",Files);
 exit(0);
}