/*   RW_IO.C
**
**   Reader/Writer Buffered I/O
**
**   Reader() and Writer() are called directly by the LZW4C.ASM code.
**   They should never be called by your application code.
**
**   The other functions are never called by the LZW4C.ASM code, but are
*    called only by your application routines.
**
**   Note that only a Reader() and Writer() function is required by the
**   LZW4C.ASM code. This means that you have complete control over data
**   coming into and out of the compression/expansion code. Instead of
**   reading or writing to disk, you can just as easily read/write to a
**   buffer, serial port, etc. You just have to write the Reader() and
**   Writer() code.
*/


#include <stdio.h>
#include "RW_IO.H"

#define FALSE 0
#define TRUE !FALSE

#define BUFFER_SIZE 2048

typedef struct IOstruct
{FILE *FilePtr;  /* file ptr */
 char Buffer[BUFFER_SIZE];
 int  Left;      /* leftmost byte in Buffer */
 int  Right;     /* rightmost byte in buffer */
 long Count;     /* # times Reader/Writer called */
} IOstruct;

static IOstruct InpControl;
static IOstruct OutControl;

int ReaderOpen(char *Ptr)
{/* open input file */
 InpControl.Left = 0;
 InpControl.Right = 0;
 InpControl.Count = 0;
 InpControl.FilePtr = fopen(Ptr,"rb");
 if(InpControl.FilePtr==NULL)
   {printf("Cannot open '%s'\n",Ptr);
    return(FALSE);
   }
 return(TRUE);
}

int Reader(void)
{char Byte;
 if(InpControl.Left==InpControl.Right)
    {/* read next buffer */
     InpControl.Left = 0;
     InpControl.Right = fread(&InpControl.Buffer,1,BUFFER_SIZE,InpControl.FilePtr);
     if(InpControl.Right<=0) return(EOF);
    }
 /* return next byte */
 Byte = InpControl.Buffer[InpControl.Left++];
 InpControl.Count++;
 return(0x00ff&Byte);
}

long ReaderCount(void)
{/* return bytes read */
 return(InpControl.Count);
}

void ReaderClose(void)
{/* close input file */
 fclose(InpControl.FilePtr);
#if 0
printf("%ld bytes read\n",InpControl.Count);
#endif
}

int WriterOpen(char *Ptr)
{/* open output file */
 OutControl.Left = 0;
 OutControl.Right = 0;
 OutControl.Count = 0;
 OutControl.FilePtr = fopen(Ptr,"wb");
 if(OutControl.FilePtr==NULL)
   {printf("Cannot open '%s'\n",Ptr);
    return(FALSE);
   }
 return(TRUE);
}

int Writer(char Byte)
{int Code;
 OutControl.Count++;
 if((OutControl.Count&0x0fff)==0) putchar('.');
 OutControl.Buffer[OutControl.Right++] = Byte;
 if(OutControl.Right==BUFFER_SIZE)
    {/* read next buffer */
     Code = fwrite(&OutControl.Buffer,1,OutControl.Right,OutControl.FilePtr);
     OutControl.Right = 0;
    }
 return(Code);
}

long WriterCount(void)
{/* return bytes written */
 return(OutControl.Count);
}


void WriterClose(void)
{/* flush buffer to disk */
 fwrite(&OutControl.Buffer[OutControl.Left],1,OutControl.Right-OutControl.Left,OutControl.FilePtr);
 /* close output file */
 fclose(OutControl.FilePtr);
}