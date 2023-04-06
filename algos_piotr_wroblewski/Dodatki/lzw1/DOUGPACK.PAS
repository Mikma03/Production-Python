unit DOUGPACK;


{----------------------------------------------------------------------}
{------  Turbo Pascal DOUGPACK unit written by Douglas Webb    --------}
{----------------------------------------------------------------------}
{------  DISCLAIMER:  There shall be no guarantee of the       --------}
{------   suitability of this software for any purpose.  The   --------}
{------   author shall not be liable for any damages arrising  --------}
{------   from the use of this software.                       --------}
{----------------------------------------------------------------------}


{ This unit was written to demonstrate how LZW compression can be used to
  compress files. It's ability to do so depends highly on the type of data
  being compressed.  Text files may compress to 30-50% their original size,
  .EXE files to 60-80% of their original size, database files to 20-40% of
  their original size, and unpatterned data may actually increase in size.

  This incarnation of the algorithm is optimized for speed, as much as is
  possible in a high level language like pascal, and to a lesser
  degree at this experimental stage, flexibility, not readability.

  CRC assembly language routines were furnished by:
       Edwin T. Floyd [76067,747]

   This unit allows the user to compress data using a variation on the
  standard LZW compression format, or conversely to decompress data that
  was previously compressed by this unit.
     This unit makes a few assumptions:
          1) Data being compressed is being sent to a file.
          2) Data being decompressed is coming from a file.
   There are however a number of options as to where the compressed data
  is coming from, and the decompressed data is going.

   In fact it requires that you pass the "Compress" procedure a procedural
  parameter of type 'GetBytesProc' (declared below) which will accept 3
  parameters and act in every way like a 'BlockRead' procedure call.
  Compress will ask for data in chunks of 4K or so at a time. Your
  procedure should return the data to be compressed:

  GetBytesProc = PROCEDURE(VAR DTA; NBytes:WORD; VAR Bytes_Got : WORD);

  DTA is the start of a memory location where the information returned
  should be.  NBytes is the number of bytes requested.  The actual number
  of bytes returned must be passed in Bytes_Got (if there is no more data
  then 0 should be returned).

    "Decompress" requires a procedural parameter of type 'PutBytesProc'
  which will accept 3 parameters, and must act in every way like a
  'BlockWrite' procedure call.  It must accept the decompressed data
  and do something with it.

  GetBytesProc = PROCEDURE(VAR DTA; NBytes:WORD; VAR Bytes_Got : WORD);

     Don't forget that as procedural parameters they must be compiled in the
  'F+' state to avoid a catastrophe.


  Unpleasant NOTE: My provisions for maintaining a CRC for the compressed
    file seem to get into trouble if you try to compress/decompress multiple
    runs of data successively.  You'll get a warning that the CRC is bad
    when in fact results appear to indicate that this is not so. So you may
    have to ignore the CRC unless you can figure out how it's broken.

}

interface
uses crt,Dos,CRC;

{#T The_LZW_Algorithm }
{     The compression algorithm :

          STRING = get input character
          WHILE there are still input characters DO
            CHARACTER = get input chracter
            IF STRING+CHARACTER is in the string table THEN
              STRING = STRING + character
            ELSE
              output the code for string
              add STRING+CHARACTER to the string table
              STRING = CHARACTER
            END of IF
          END of WHILE
          output the code for string

      The decompression algorithm:

          Read OLD_CODE
          output OLD_CODE
          WHILE there are still input characters DO
            Read New_CODE
            IF NEW_CODE is not in the translation table THEN
              STRING = get translation of OLD_CODE
              STRING = STRING+CHARACTER
            ELSE
              STRING = get translation of NEW_CODE
            END of IF
            output STRING
            CHARACTER = first character in STRING
            add OLD_CODE+CHARACTER to the translation table
            OLD_CODE = NEW_CODE
          END WHILE


    Wrinkles added to improve compression:
     1: Sliding dictionary size, Always start with a 9 bit table, then
       when it's full increase the table size to 10 bits, and so on until
       the dictionary is as big as you intend to support (say 12-14 bits).
     2: Empty the library after it fills up and start again.  This is useful
       in files where the repetative elements in them may change positionally,
       such as in picture files of one sort or another, and many .EXE files.
       In some cases this may actually cost you some compression, but not often
       and not very much in any event. Even smarter (but not implemented)
       would be to monitor compression and clear/partial clear if compression
       appears to be dropping.

}




CONST                    
  Bits = 12;           { This constant reflects the number of bits used to
                         generate the dictionary to compress the data. Data
                         must be decmpressed using the same dictionary size
                         as was used when it was compressed. Setting the
                         number of bits to 12, 13 or 14 affects several
                         constants.
                         Larger Files tend to compress better with a larger
                         dictionaries.

                         Memory used by this unit is a function of Bits &
                          and the associated constant Table_Size:
                            14 : 110K; 13 : 65K;  12 : 45K
                         All but about 5-10K of this is heap and is not
                           needed (or in use) when the unit is not actually
                         compressing or decompressing data.

                         If you change this value, change the value of
                         Table_Size appropriately.
                         }



TYPE
  PutBytesProc = PROCEDURE(VAR DTA; NBytes:WORD; VAR Bytes_Put : WORD);
  {#X GetBytesProc}
  {  "Decompress" requires a procedural parameter of type 'PutBytesProc'
  which will accept 3 parameters, and must act in every way like a
  'BlockWrite' procedure call.  It must accept the decompressed data
  and do something with it (like save it to a file).

   Don't forget that as procedural parameters they must be compiled in the
  'F+' state to avoid a catastrophe. }


  GetBytesProc = PROCEDURE(VAR DTA; NBytes:WORD; VAR Bytes_Got : WORD);
 {#X PutBytesProc}
 { The "Compress" procedure, requires that it be passed a procedural
  parameter of type 'GetBytesProc' which will accept 3
  parameters and act in every way like a 'BlockRead' procedure call.
  Compress will ask for data in chunks of 4K or so at a time. Your
  procedure should return the data to be compressed.

  DTA is the start of a memory location where the information returned
  should be.  NBytes is the number of bytes requested.  The actual number
  of bytes returned must be passed in Bytes_Got (if there is no more data
  then 0 should be returned).

  Don't forget that as procedural parameters they must be compiled in the
  'F+' state to avoid a catastrophe.
  }


Function Compress(VAR OutFile : File; VAR Bytes_Written:LongInt; GetBytes:GetBytesProc): Word;
{#X Decompress The_LZW_Algorithm}
{ This function uses LZW compression to compress the contents of InFile,
  and write them to OutFile, a CRC value for the original value is returned.
  The size of the compressed output is returned in 'Bytes_Written'. }

Function Decompress(VAR InFile : File; UsedBits: Word; NoBytes : Longint; PutBytes: PutBytesProc): Word;
{#X Compress The_LZW_Algorithm}
{ This is the decompression routine.  It takes a LZW format file, and
    expands it to an output file.  The code here should be a fairly close
    match to the algorithm above.

    Usedbits - How many bits was the dictionary used during compression
               (this is to make sure decompression is the same.)
    NoBytes  - How many bytes are being decompressed
}


implementation

{$R-}                    { Error checking slows things down by 200% }

CONST
  Hashing_Shift = Bits - 8;
  Max_Value = PRED((1 SHL Bits));     { Code indicating end of data. }
  Max_Code = PRED(Max_Value);         { The maximum amount of table entries allowed. }
  Buffer_Size = 4096;                 { Buffer for file I/O }
  Terminator : Array[10..14] OF WORD = (1023,2047,4095,8191,16383);


{ IF Bits = 14 then define table size as 18041 }  { The string table size   }
{ IF Bits = 13 then define table size as 9029  }  {  must be a prime number }
{ IF Bits = 12 then define table size as 5021  }  {  about 25% larger than  }
  Table_Size = 5021;                             {  2^Bits.                }




TYPE


  Buffer_Type = Array[1..Buffer_Size] of Byte;  { I/O buffers. }
  Buffer_Ptr  = ^Buffer_Type;

  Stack_Array = Array[1..4000] of Byte;         { Decompression stack. }
  Stack_Ptr   = ^Stack_Array;

  Word_Array  = Array[0..Table_Size] OF Integer;
  Word_Ptr    = ^Word_Array;
  Char_Array  = Array[0..Table_Size] OF BYTE;
  Char_Ptr    = ^Char_Array;




VAR
  InBuf,OutBuf : Buffer_Ptr;
  Code_Value,Prefix_Code : Word_Ptr;
  Append_Character : Char_Ptr;

  Stack_Position : Word;
  Stringy : Stack_Ptr;
  NumRead : Word;
  BitsC : Word;




Function Input_Code(VAR InFile : File; BitsC : WORD; Resetf : BOOLEAN): WORD;

{ This function feeds data to the decompression routine. }


CONST
  Input_Bit_Count : Integer = 0;
  Input_Bit_Buffer : Longint = 0;
  IBuffer_Count : Integer = SUCC(Buffer_Size);

VAR
  Return_Value : Word;
  Temp : LongInt;
  Numread : WORD;

BEGIN
  IF Resetf THEN                                { Reset everything to initial values. }
    BEGIN
      Input_Bit_Count := 0;
      Input_Bit_Buffer  := 0;
      IBuffer_Count := SUCC(Buffer_Size);
    END;
  While Input_Bit_Count < 25 DO                 {  Input_Bit_Count <= 24 }
    BEGIN
      IF IBuffer_Count < SUCC(Buffer_Size) THEN
        BEGIN
          Temp := InBuf^[IBuffer_Count];
          INC(IBuffer_Count);
        END
      ELSE
        BEGIN
          BlockRead(InFile,InBuf^,Buffer_Size,NumRead);
          Temp := InBuf^[1];
          IBuffer_Count := 2;
        END;

      Input_Bit_Buffer := Input_Bit_Buffer OR (Temp SHL (24-Input_Bit_Count));
      INC(Input_Bit_Count,8);
    END;
  Return_Value := Input_Bit_Buffer SHR (32-BitsC);
  Input_Bit_Buffer := Input_Bit_Buffer SHL BitsC;
  DEC(Input_Bit_Count,BitsC);
  Input_Code := Return_Value;
END;                                     {  end of the compressed data.    }





Procedure Output_Code(VAR OutFile: File; _Code,BitsC : Word; VAR Bytes_Written: Longint);

  { This procedure dumps the output of the compression routine to disk. }

CONST
  Output_Bit_Count : Integer = 0;
  Output_Bit_Buffer : Longint = 0;
  OBuffer_Count : Integer = 1;

VAR
  Code : LongInt;
  temp : LongInt;
  A    : Byte;


BEGIN
  Code := _Code;                { Convert form Word to LONGINT. }
  Output_Bit_Buffer := Output_Bit_Buffer OR (Code SHL (32-BitsC-Output_Bit_Count));
  INC(Output_Bit_Count,BitsC);
  WHILE Output_Bit_Count >= 8 DO
    BEGIN
      OutBuf^[OBuffer_Count] := OutPut_Bit_Buffer SHR 24;
      IF (OBuffer_Count <> Buffer_Size) AND (Code <> Max_Value) THEN  
        INC(OBuffer_Count)
      ELSE
        BEGIN
          IF _Code <> Max_Value THEN
            BEGIN
              BlockWrite(OutFile,OutBuf^,Buffer_Size,NumRead);
              OBuffer_Count := 1;
              INC(Bytes_Written,NumRead);
            END
          ELSE
            BEGIN              (* Flushing out the last few bytes *)
              WHILE Output_Bit_Count > Bits - BitsC DO
                BEGIN
                  DEC(Output_Bit_Count,8);
                  INC(OBuffer_Count);
                  Output_Bit_Buffer := Output_Bit_Buffer SHL 8;
                  OutBuf^[OBuffer_Count] := OutPut_Bit_Buffer SHR 24;
                END;
              BlockWrite(OutFile,OutBuf^,PRED(OBuffer_Count),NumRead);
              INC(Bytes_Written,NumRead);
              Output_Bit_Buffer := 0;        { Reset for next time. }
              Output_Bit_Count := 8;         { Reset for next time. }
            END;
          OBuffer_Count := 1;
        END;
      Output_Bit_Buffer := Output_Bit_Buffer SHL 8;
      DEC(Output_Bit_Count,8);
    END;
END;





Function Compress(VAR OutFile : File; VAR Bytes_Written:LongInt; GetBytes:GetBytesProc): Word;

{ This function uses LZW compression to compress the contents of InFile,
  and write them to OutFile, a CRC value for the original value is returned. }

LABEL
  1;


VAR
  NumRead,String_Code,Next_Code : WORD;
  I,J : INTEGER;
  Character,Temp: Byte;
  IBuffer_Count : WORD;
  X : Longint;
  Index,Offset : Integer;
  CRCVal : WORD;
  NotPacked : BOOLEAN;


BEGIN
  New(InBuf);                   { Create all the structures that will }
  New(OutBuf);                  {  be needed to compress the data.    }
  New(Code_Value);
  New(Prefix_Code);
  New(Append_Character);


  NotPacked := TRUE;
  Bytes_Written :=  0;
  BitsC := 9;                    { Starting size of library. }
  CRCVal := 0;                   { Initialize the CRC value. }
  Next_Code := 256;
  FOR I := 0 TO Table_Size DO    { Clear the string table before starting. }
    Code_Value^[I] := -1;
  GetBytes(Temp,1,Numread);      { Get the first Code.   }
  GetBytes(InBuf^,1,Numread);
  IBuffer_Count := Numread;  { Set Byte buffer empty. }
  CRCVal := UpdateCRCArc(CRCVal,Temp,1);               { Update CRC value. }
  CRCVal := UpdateCRCArc(CRCVal,InBuf^,NumRead);       { Update CRC value. }
  String_Code := Temp;

  { This is the main loop where it all happens.  This loop runs until all
     of the input file has been read.  Note that it clears the table
     and restarts once all possible codes have been defined.       }

  While NotPacked DO
    BEGIN
      IF IBuffer_Count <> Numread THEN
        BEGIN
          Character := InBuf^[IBuffer_Count];
          INC(IBuffer_Count);
        END
      ELSE
        BEGIN
           Character := InBuf^[IBuffer_Count];
           GetBytes(InBuf^,Buffer_Size,Numread);
           CRCVal := UpdateCRCArc(CRCVal,InBuf^,NumRead);   { Update CRC value. }
           IBuffer_Count := 1;
           If Numread = 0 THEN NotPacked := FALSE;          { If there is no more data then stop.}
        END;

{ This is the hashing code routine.  It tries to find a match for prefix+char
   string in the string table.  If it finds it, the index is returned.  IF
   the string is not found, the first available index in the string table is
   returned instead.
}
      Index := (Character SHL Hashing_Shift) XOR String_Code;
      IF Index = 0 THEN Offset := 1
      ELSE Offset := Table_Size - Index;
      WHILE TRUE DO
        BEGIN
          IF Code_Value^[Index] = -1 THEN
            Goto 1;
          IF (Prefix_Code^[Index] = String_Code) AND
                        (Append_Character^[Index] = Character) THEN
            Goto 1;
          DEC(Index,Offset);
          IF Index < 0 THEN INC(Index,Table_Size);
        END;

                                                  { See if it's already in }
1:    IF Code_Value^[Index] <> -1 THEN            { the table. If it is,   }
        String_Code := Code_Value^[Index]         { get the code value. If }
      ELSE                                        { the string is not in   }
        BEGIN                                     { table try to add it.   }
          IF Next_Code < Max_Code THEN    { Actually this IF is redundant, will NEVER be false. }
            BEGIN
              Code_Value^[Index] := Next_Code;
              INC(Next_Code);
              Prefix_Code^[Index] := String_Code;
              Append_Character^[Index] := Character;
              Output_Code(OutFile,String_Code,BitsC,Bytes_Written);     { When a string is found    }
              IF (Next_Code DIV (1 SHL BitsC)) = 1 THEN
                INC(BitsC);                         { Sliding window.     }
              String_Code := Character;             { that is not in the table  }
              IF Next_Code = Max_Code THEN       { Table is full. }
                BEGIN
                  BitsC := 9;                    { Reset the sliding dictionary. }
                  Next_Code := 256;
                  FOR J := 0 TO Table_Size DO    { Clear the string table before }
                    Code_Value^[J] := -1;        {  starting to fill it again.   }
                END;
            END;

        END;                                    { I output the last string  }
    END;                                        { after adding the new one. }

  { End of the main loop }

  Output_Code(OutFile,String_Code,BitsC,Bytes_Written); { Output the last code.                }
  BitsC := Bits;
  Output_Code(OutFile,Max_Value,BitsC,Bytes_Written);   { Output the end of buffer code.       }

  Dispose(OutBuf);                  { Deallocate all our structures. }
  Dispose(InBuf);
  Dispose(Code_Value);
  Dispose(Prefix_Code);
  Dispose(Append_Character);

  Compress := CRCVal;
END;








Function Decompress(VAR InFile : File; UsedBits: Word; NoBytes : LongInt; PutBytes: PutBytesProc): Word;

{ This is the decompression routine.  It takes a LZW format file, and
    expands it to an output file.  The code here should be a fairly close
    match to the algorithm above.
}



VAR
  Next_Code,Code,New_Code,Old_Code : WORD;
  I,Character : Integer;
  Temp : Byte;
  OBuffer_Count : WORD;
  CRCVal : WORD;
  CarryBits : Word;
  BytesDeCompressed : LongInt;




BEGIN
  If UsedBits <> Bits THEN       { If compressed with different # bits }
    BEGIN                        {   abort now.                        }
      Decompress := 0;
      Exit;
    END;


  New(InBuf);                     { Create all the structure which }
  New(OutBuf);                    {  will allow me to decompress   }
  New(Stringy);                   {  the data.                     }
  New(Code_Value);
  New(Prefix_Code);
  New(Append_Character);

  BytesDeCompressed := 0;
  CarryBits := 0;
  BitsC := 9;                     { Initialize a few variables.    }
  CRCVal := 0;
  OBuffer_Count := 1;
  Stack_Position := 1;
  Next_Code := 256;           { This is the next available code to define. }
  Old_Code := Input_Code(InFIle,BitsC,TRUE); { Read in the first code, initialize the }
  BytesDeCompressed := BytesDeCompressed + (CarryBits + BitsC) DIV 8;
  CarryBits := (CarryBits + BitsC) MOD 8;
  Character := Old_Code;                { character variable, and send the first }
  Temp := Old_Code;
  PutBytes(Temp,1,NumRead);             { code to the output file.   }
  CRCVal := UpdateCRCArc(CRCVal,Temp,1);       { Update CRC value. }


 { This is the main decompression loop.  It read characters from the LZW file
   until it sees the special code used to indicate the end of the data.
 }

  New_Code := Input_Code(InFile,BitsC,FALSE);
  BytesDeCompressed := BytesDeCompressed + (CarryBits + BitsC) DIV 8;
  CarryBits := (CarryBits + BitsC) MOD 8;
  While (New_Code <> Terminator[BitsC]) OR (BytesDeCompressed < NoBytes -2) DO
    BEGIN

      { This code checks for special STRING+CHARACTER+STRING+CHARACTER+STRING
         case which generates an undefined code.  It handles it by decoding
         the last code, adding a single character to the end of the decode string.
      }
      IF New_Code = Next_Code THEN
        BEGIN
          Stringy^[Stack_Position] := Character;
          INC(Stack_Position);

      { This routine simply decodes a string from the string table, storing
         it in a buffer.  The buffer can then be output in reverse order by the
         expansion routine (below).
      }
          Code := Old_Code;
          While Code > 255 DO
            BEGIN
              Stringy^[Stack_Position] := Append_Character^[Code];
              INC(Stack_Position);
              Code := Prefix_Code^[Code];
              IF Stack_Position >= 4000 THEN
                BEGIN
                  Writeln('Fatal Error during code decompression.');
                  Halt;
                END;
            END;
          Stringy^[Stack_Position] := Code;
        END
      { Otherwise do a straight decode of the new code. }
      ELSE
        BEGIN
          Code := New_Code;
          While Code > 255 DO
            BEGIN
              Stringy^[Stack_Position] := Append_Character^[Code];
              INC(Stack_Position);
              Code := Prefix_Code^[Code];
              IF Stack_Position >= 4000 THEN
                BEGIN
                  Writeln('Fatal Error during code decompression.');
                  Halt;
                END;
            END;
          Stringy^[Stack_Position] := Code;
        END;

      { Now output the decoded string in reverse order. }
      Character := Stringy^[Stack_Position];
      While (Stack_Position >= 1) DO
        BEGIN
          IF (OBuffer_Count <> Buffer_Size) THEN
            BEGIN
              OutBuf^[OBuffer_Count] := Stringy^[Stack_Position];
              INC(OBuffer_Count);
            END
          ELSE
            BEGIN
              OutBuf^[Buffer_Size] := Stringy^[Stack_Position];
              PutBytes(OutBuf^,Buffer_Size,NumRead);
              CRCVal := UpdateCRCArc(CRCVal,OutBuf^,NumRead);       { Update CRC value. }
              OBuffer_Count := 1;
            END;

          DEC(Stack_Position);
        END;
      INC(Stack_Position);

      { Finally, if possible add a new code to the string table. }
      IF Next_Code < Max_Code-1 THEN
        BEGIN
          Prefix_Code^[Next_Code] := Old_Code;
          Append_Character^[Next_Code] := Character;
          INC(Next_Code);
          IF (SUCC(Next_Code)  DIV (1 SHL BitsC)) = 1 THEN
            IF BitsC < Bits THEN INC(BitsC);
        END;
      IF Next_Code = Max_Code-1 THEN          { Table is now full. }
        BEGIN
          BitsC := 9;                         { Reset sliding dictionary. }
          Stack_Position := 1;
          Next_Code := 256;                   { This is the next available code to define. }
          New_Code := Input_Code(InFile,BitsC,FALSE);
          BytesDeCompressed := BytesDeCompressed + (CarryBits + BitsC) DIV 8;
          CarryBits := (CarryBits + BitsC) MOD 8;
          Character := New_Code;              { Reinitialize the decode process. }
          IF (OBuffer_Count <> Buffer_Size) THEN
            BEGIN
              OutBuf^[OBuffer_Count] := New_Code;
              INC(OBuffer_Count);
            END
          ELSE
            BEGIN
              OutBuf^[Buffer_Size] := New_Code;
              CRCVal := UpdateCRCArc(CRCVal,OutBuf^,Buffer_Size);       { Update CRC value. }
              PutBytes(OutBuf^,Buffer_Size,NumRead);
              OBuffer_Count := 1;
            END;
        END;
      Old_Code := New_Code;
      New_Code := Input_Code(Infile,BitsC,FALSE);
      BytesDeCompressed := BytesDeCompressed + (CarryBits + BitsC) DIV 8;
      CarryBits := (CarryBits + BitsC) MOD 8;
   END;
  CRCVal := UpdateCRCArc(CRCVal,OutBuf^,PRED(OBuffer_Count));       { Update CRC value. }
  PutBytes(OutBuf^,PRED(OBuffer_Count),NumRead);

  Dispose(OutBuf);                   { Deallocate all our structures. }
  Dispose(InBuf);
  Dispose(Stringy);
  Dispose(Code_Value);
  Dispose(Prefix_Code);
  Dispose(Append_Character);
  Decompress := CRCVal;
END;




END.