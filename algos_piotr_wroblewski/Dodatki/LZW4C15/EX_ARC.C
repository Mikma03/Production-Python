/*
**   EX_ARC.C       Copyright (C) 1994 by MarshallSoft Computing, Inc.
**
**   This program is used to extract a file from archive created with
**   MK_ARC. For example, to extract the file TEST.C from the archive
**   MY_PGMS.ARC, type:
**
**      EX_ARC TEST.C MY_PGMS.ARC
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

int DummyWrite(char);

void main(int argc, char *argv[])
{int i, k, c;
 int RetCode;
 int Len;
 char *Ptr;
 char Filename[15];
 char Requested[15];
 /* begin */
 if(argc!=3)
   {printf("Usage: EX_ARC <filename> <archive>\n");
    exit(1);
   }
 RetCode = InitLZW(malloc,14);
 if(RetCode<0)
   {SayError(RetCode);
    exit(2);
   }
 puts("\nEX_ARC 1.0: Type any key to abort...");
 /* make requested file all upper case */
 Ptr = argv[1];
 Len = strlen(Ptr);
 for(i=0;i<Len;i++) Requested[i] = toupper(Ptr[i]);
 Requested[Len] = '\0';
 printf("Searching for '%s' in archive '%s'\n",Requested,argv[2]);
 /* open input file for expansion */
 if(!ReaderOpen(argv[2])) exit(4);
 for(i=0;;i++)
   {if(kbhit())
      {puts("\n...Aborted by user !");
       break;
      }
    /* find start of next filename */
    for(k=0;k<5;k++)
       {c = Reader();
        if(c==-1)
           {ReaderClose();
            TermLZW(free);
            exit(0);
           }
        /* skip past any 0's */
        if(c!='\0') break;
       }
    Filename[0] = (char)c;
    /* get complete filename */
    for(k=1;k<13;k++)
       {c = Reader();
        Filename[k] = (char)c;
        if(c=='\0') break;
       }
    if(c!='\0')
       {printf("ERROR: Cannot find filename in %s\n",argv[1]);
        TermLZW(free);
        exit(0);
       }
    if(strcmp(Filename,argv[2])==0)
      {printf("ERROR: Archive contains file '%s' named same as archive\n",argv[2]);
       exit(1);
      }
    else
      {/* right file to extract ? */
       if(strcmp(Filename,Requested)==0)
         {/* open output file */
          printf("Expanding %12s ",Filename);
          if(!WriterOpen(Filename)) exit(3);
          /* do the expansion */
          if((RetCode=Expand(Reader,Writer))<0)
            {SayError(RetCode);
             exit(5);
            }
          puts("OK");
          WriterClose();
          ReaderClose();
          exit(0);
         }
       else
         {/* skip file */
          printf("Skipping %12s \n",Filename);
          if((RetCode=Expand(Reader,DummyWrite))<0)
            {SayError(RetCode);
             exit(5);
            }
         }
      }
   }
}

int DummyWrite(char Byte)
{int Code = 0;
 /* Byte dumped ! */
 Byte = Byte + 0;
 return(Code);
}
