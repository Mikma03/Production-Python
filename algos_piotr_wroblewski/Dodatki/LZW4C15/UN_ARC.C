/*
**   UN_ARC.C       Copyright (C) 1992 by MarshallSoft Computing, Inc.
**
**   This program is used to expand archive created with MK_ARC. For
**   example, to un-archive all the files in 'C.ARF', type:
**
**      UN_ARC C.ARF
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

#include "LZW4C.H"
#include "RW_IO.H"
#include "DIR_IO.H"
#include "SAYERROR.H"

void main(int argc, char *argv[])
{int i, k, c;
 int RetCode;
 char Filename[15];
 int Files = 0;
 /* begin */
 if(argc!=2)
   {printf("Usage: UN_ARC <archive_filespec>\n");
    exit(1);
   }
 RetCode = InitLZW(malloc,14);
 if(RetCode<0)
   {SayError(RetCode);
    exit(2);
   }
 puts("\nUN_ARC 1.0: Type any key to abort...");
 /* open input file for expansion */
 if(!ReaderOpen(argv[1])) exit(4);
 for(i=0;;i++)
   {if(kbhit())
      {puts("\n...Aborted by user !");
       break;
      }
    /* get filename */
    for(k=0;k<5;k++)
       {c = Reader();
        if(c==-1)
           {ReaderClose();
            TermLZW(free);
            printf("\n%d files expanded\n",Files);
            exit(0);
           }
        /* skip past any 0's */
        if(c!='\0') break;
       }
    Filename[0] = (char)c;
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
    if(strcmp(Filename,argv[1])==0)
      {printf("ERROR: Archive contains file '%s' named same as archive\n",argv[1]);
       exit(1);
      }
    else
      {/* open output file */
       printf("Expanding %12s ",Filename);
       if(!WriterOpen(Filename)) exit(3);
       /* do the expansion */
       Files++;
       if((RetCode=Expand(Reader,Writer))<0)
         {SayError(RetCode);
          exit(5);
         }
       puts("OK");
       WriterClose();
      }
   }
}