PROGRAM PackTest;

USES CRT,DOS,DOUGPACK;


{ This is a very simple example program using the "Dougpack" unit.  All this
   program does is allow you to compress 1 file, or decompress one file that
   has been compressed using this program. }




TYPE
  Compression_Header_Type = RECORD                   { 21 bytes in size. }
                               Name : String[12];
                               COmpressed_Bytes : Longint;   { Doesn't include header.}
                               Bits_Used : BYTE;
                               Clear_After_Table_Full : BOOLEAN;
                               CRC : WORD;
                            END;


VAR
  Ch : Char;
  Filename : String;
  Dir : DirStr;
  Name : NameStr;
  Ext : ExtStr;
  Header : Compression_Header_Type;
  FoundFile : SearchRec;
  Bytes_Written : Longint;
  Input_File_Name : Array[1..80] OF Char;
  INFile,OutFile,LZWFile : File;
  X,NumRead : Word;




Procedure DumpSyntax;
BEGIN
  CLRSCR;
  GotoXY(5,3); Writeln('Dougpack 1.01 Copywrite 1990,   All rights reserved.');
  GotoXY(5,5); Writeln('The correct syntax for this program is:');
  GotoXY(8,7); Writeln('DOUGPACK <Filename>');
  GotoXY(5,9); Writeln('If the file specified is not a DougPack file it will be compressed.');
  GotoXY(5,10); Writeln('If it is a DougPack file it will be decompressed.');
END;







{$F+}

Procedure GetBytesDisk(VAR Target; NBytes: WORD; VAR Bytes_Returned: WORD);
     { For reading from a file called InFile}

BEGIN
  Blockread(InFile,Target,NBytes,Bytes_Returned);
END;


Procedure PutBytesDisk(VAR Source; NBytes: WORD; VAR Bytes_Written: WORD);
BEGIN
  BlockWrite(OutFile,Source,NBytes,Bytes_Written);
END;

{$F-}





BEGIN
  IF Paramcount < 1 THEN
    BEGIN
      DumpSyntax;
      HALT;
    END;
  Filename := ParamStr(1);
  FSplit(Filename,Dir,Name,Ext);
  FOR X := 1 TO 4 DO
    Ext[X] := Upcase(Ext[X]);
  IF (Ext <> '.DPK') AND (Ext <> '.') AND(Ext <> '') THEN     { Compress. }
    BEGIN
      Header.Name := Name + Ext;
      Header.Bits_Used := Bits;
      Header.Clear_After_Table_Full := FALSE;
      Assign(Infile,Filename);
      Assign(LZWFile,Name + '.DPK');
      RESET(InFile,1);                { used for compression }
      REwrite(LZWFile,1);
      BlockWrite(LZWFile,Header,SizeOf(Header),NumRead);   { Save space for the header. }
      Header.CRC := Compress(LZWFile,Bytes_Written,GetBytesDisk);
      Header.Compressed_Bytes := Bytes_Written;
      Header.Bits_Used := Bits;
      Seek(LZWFile,0);
      BlockWrite(LZWFile,Header,SizeOf(Header),NumRead);   { Write header with CRC value. }
      Writeln('File compressed to ',100*Filesize(LZWFile) DIV FileSize(InFile),'% of original.');
      Close(Infile);
      Close(LZWfile);
    END
  ELSE                  { Decompress. }
    BEGIN
      Assign(LZWfile,Name + '.DPK');
      RESet(LZWFile,1);
      Blockread(LZWFile,Header,SizeOf(Header),Numread);
      IF Header.Bits_Used > 14 THEN
        BEGIN
          Writeln('Cannot decompress this file.');
          HALT;
        END;
      FindFirst(Header.Name,$27,Foundfile);    { See if the file to be decompressed }
      If DOSError = 0 THEN                     { already exists.                    }
        BEGIN
          Writeln(Header.Name,' already exists, decompress anyway ? (Y/N)');
          Ch := Readkey;
          IF NOT (Ch IN ['y','Y']) THEN HALT;
        END;
      Assign(OutFile,Header.Name);
      ReWrite(OutFile,1);                { used for decompression }
      IF decompress(LZWFile,Header.Bits_Used,Header.Compressed_Bytes,PutBytesDisk) <> Header.CRC THEN
        BEGIN                            { The arc file is corrupted! }
          Writeln;
          Writeln(#8,#8,#8);
          Writeln('CRC Error');
          Writeln('The Archive was corrupted in some way, the decompressed file');
          Writeln(' is not the same one that was compressed.');
        END;
      Close(Outfile);
      Close(LZWfile);
    END;
END.