/*
**  DIR_IO.C
**
**  Compile with Microsoft C, Borland Turbo C, or MIX Power C.  You may
**  need to modify the following code for your specfic compiler. Some
**  older versions of Microsoft C do not support directory I/O.
*/

#include <stdio.h>
#include <dos.h>
#include <string.h>

#ifndef FALSE
#define FALSE 0
#endif

#ifndef TRUE
#define TRUE !FALSE
#endif

/*** define compiler specfic includes ***/

#ifdef __POWERC
/* MIX Power C compiler */
#define TURBO_OR_POWERC
#define SUPPORTED_COMPILER
#include <direct.h>
#endif

#ifdef __TURBOC__
/* Borland Turbo C compiler */
#define TURBO_OR_POWERC
#define SUPPORTED_COMPILER
#include <dir.h>
#endif

#ifdef _MSC_VER
/* Microsoft C compiler */
#define SUPPORTED_COMPILER
static struct _find_t DirStruct;
#endif

#ifdef TURBO_OR_POWERC
static char DTAbuffer[256];
static struct ffblk DirStruct;
#endif

/*** FindFirst() and FindNext() functions ***/

int FindFirst(char *FileSpec,char *Buffer)
{
#ifndef SUPPORTED_COMPILER
 /* compiler doesn't support directory I/O ! */
 strncpy(Buffer,FileSpec,13);
#endif

#ifdef _MSC_VER
 if(_dos_findfirst(FileSpec,_A_NORMAL,&DirStruct)==0)
   {
    strncpy(Buffer,DirStruct.name,13);
    return(TRUE);
   }
 return(FALSE);
#endif

#ifdef TURBO_OR_POWERC
 setdta(DTAbuffer);
 if( findfirst(FileSpec,&DirStruct,0)==0)
   {
    strncpy(Buffer,DirStruct.ff_name,13);
    return(TRUE);
   }
 return(FALSE);
#endif
}

int FindNext(char *Buffer)
{int Result;

#ifndef SUPPORTED_COMPILER
 /* compiler doesn't support directory I/O ! */
 return(FALSE);
#endif

#ifdef _MSC_VER
Result = _dos_findnext(&DirStruct);
if(Result==0)
   {
    strncpy(Buffer,DirStruct.name,13);
    return(TRUE);
   }
 return(FALSE);
#endif

#ifdef TURBO_OR_POWERC
 if( findnext(&DirStruct)==0 )
   {
    strncpy(Buffer,DirStruct.ff_name,13);
    return(TRUE);
   }
 return(FALSE);
#endif
}
