{$A+,B-,D-,E-,F-,I-,L-,N-,O-,R-,S-,V+}
Unit Crc;
{ This unit provides a speed-optimized function to compute (or continue
  computation of) a Cyclic Redundency Check (CRC).  This routines is
  contributed to the public domain (with the limitations noted by the
  original authors in the TASM sources).

  The function takes three parameters:

  InitCRC - The initial CRC value.  This may be the recommended
  initialization value if this is the first or only block to be checked,
  or this may be a previously computed CRC value if this is a continuation.

  InBuf - An untyped parameter specifying the beginning of the memory area
  to be checked.

  InLen - A word indicating the length of the memory area to be checked.  If
  InLen is zero, the function returns the value of InitCRC.

  The function result is the updated CRC.  The input buffer is scanned under
  the limitations of the 8086 segmented architecture, so the result will be
  in error if InLen > 64k - Offset(InBuf).

  These conversions were done on 10-29-89 by:

  Edwin T. Floyd [76067,747]
  #9 Adams Park Court
  Columbus, GA 31909
  (404) 576-3305 (work)
  (404) 322-0076 (home)
}
Interface


Function UpdateCRCArc(InitCRC : Word; Var InBuf; InLen : Word) : Word;
{ This function computes the CRC used by SEA's ARC utility.  Initialize
  with zero. }


Implementation
Function UpdateCRCArc(InitCRC : Word; Var InBuf; InLen : Word) : Word;
External;
{$L CRCARC.OBJ }
End.