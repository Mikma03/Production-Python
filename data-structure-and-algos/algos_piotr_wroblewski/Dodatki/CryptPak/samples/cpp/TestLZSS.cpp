

#include <stdio.h>
#include <string.h>

#include "TestInterface.h"


#define TESTBUFSIZE     16384


WORD8 inbuf[TESTBUFSIZE];
WORD8 outbuf[TESTBUFSIZE * 2];


void TestLZSS
  (CTestStdOut* tso,
   const char* fname) 
{
    FILE *infile, *outfile;
    WORD8 bCond;
    WORD32 lRes, lRead, lWritten;
    BYTEBOOL blEOF;
    PLZSSCTX ctx;
	char fnameBuf[256];

    tso->Puts("opening files...");

    // open original file
    if ((infile = fopen(fname, "rb")) == NULL) 
    {
        tso->PrintF("cannot open input file %s\n", fname);
        return;
    }

    // open file for compressed data
    sprintf(fnameBuf, "%s.pak", fname);
    if ((outfile = fopen(fnameBuf, "wb")) == NULL) 
    {
        tso->PrintF("cannot open output file %s\n", fnameBuf);
        fclose(infile);
        return;
    }

    // create the context
    ctx = LZSS_Create();

    // start compression...
    tso->PrintF("compressing (%d bytes per hash)...\n", TESTBUFSIZE);
    lRead = 0;
    lWritten = 0;
    bCond = LZSS_START | LZSS_WORK;
    blEOF = BOOL_FALSE;
    do 
    {
      if ((lRes = fread(inbuf, 1, TESTBUFSIZE, infile)) < TESTBUFSIZE) 
        blEOF = BOOL_TRUE;
      lRead += lRes;
      if (blEOF == BOOL_TRUE) bCond |= LZSS_STOP;
      lRes = LZSS_Compress(ctx, 
		                   inbuf, 
						   outbuf, 
						   lRes, 
						   bCond);
      bCond &= ~LZSS_START;
      fwrite(outbuf, 1, lRes, outfile);
      lWritten += lRes;
      tso->PrintF("#");
    }
    while (blEOF == BOOL_FALSE);

    // close the files
    fclose(outfile);
    fclose(infile);

    // print the result
    tso->PrintF("\ncompressed %d bytes into %d bytes\n", lRead, lWritten);


    // open compressed file 
    if ((infile = fopen(fnameBuf, "rb")) == NULL) 
    {
        tso->PrintF("cannot open input file %s\n", fnameBuf);
        LZSS_Destroy(ctx);
        return;
    }

    // open file for decompressed data
    sprintf(fnameBuf, "%s.out", fname);
    if ((outfile = fopen(fnameBuf, "wb")) == NULL) 
    {
        tso->PrintF("cannot open output file %s\n", fnameBuf);
        fclose(infile);
        LZSS_Destroy(ctx);
        return;
    }

    // start decompression...
    tso->PrintF("decompressing (%d bytes per hash)...\n", TESTBUFSIZE);
    lRead = 0;
    lWritten = 0;
    bCond = LZSS_START | LZSS_WORK;
    blEOF = BOOL_FALSE;
    do 
    {
      if ((lRes = fread(inbuf, 1, TESTBUFSIZE, infile)) < TESTBUFSIZE) 
        blEOF = BOOL_TRUE;
      lRead += lRes;
      if (blEOF == BOOL_TRUE) bCond |= LZSS_STOP;

      BYTEBOOL blMustRepeat = BOOL_FALSE; // this is a must
      do 
      {
        WORD32 lDecomp = LZSS_Decompress(ctx, 
			                             inbuf, 
										 outbuf, 
										 lRes,
                                         TESTBUFSIZE, 
										 bCond, 
										 &blMustRepeat);
        bCond &= ~LZSS_START;
        fwrite(outbuf, 1, lDecomp, outfile);
        lWritten += lDecomp;
        tso->PrintF("#");
      }
      while (blMustRepeat == BOOL_TRUE);

    }
    while (blEOF == BOOL_FALSE);

    // close the files
    fclose(outfile);
    fclose(infile);

    // print the result
    tso->PrintF("\ndecompressed %d bytes into %d bytes\n", lRead, lWritten);

    LZSS_Destroy(ctx);
}
