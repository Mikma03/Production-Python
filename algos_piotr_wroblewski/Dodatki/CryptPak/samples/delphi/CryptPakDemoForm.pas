
{
  application showing the capabilities of CryptPak.dll
}


unit CryptPakDemoForm;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  ComCtrls, StdCtrls;

type
  TTestForm = class(TForm)
    CryptPakVersionButton: TButton;
    CRC32Button: TButton;
    TestMD5Button: TButton;
    TestSHA1Button: TButton;
    OpenDialog: TOpenDialog;
    TestRandomPoolBtn: TButton;
    TestLZSSBtn: TButton;
    ProgressBar: TProgressBar;
    TestCipherServerBtn: TButton;
    AboutBtn: TButton;
    TestYarrowBtn: TButton;
    procedure CryptPakVersionButtonClick(Sender: TObject);
    procedure CRC32ButtonClick(Sender: TObject);
    procedure TestMD5ButtonClick(Sender: TObject);
    procedure TestSHA1ButtonClick(Sender: TObject);
    procedure TestRandomPoolBtnClick(Sender: TObject);
    procedure TestLZSSBtnClick(Sender: TObject);
    procedure AboutBtnClick(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure TestCipherServerBtnClick(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  TestForm: TTestForm;

implementation
uses BasicTypes, CipherDef, CryptPak;

{$R *.DFM}


procedure TTestForm.CryptPakVersionButtonClick(Sender: TObject);
var
  lVer  : WORD32;
  sMess : String;
  sTemp : String;
begin
  // show version of CryptPak.dll
  lVer:=Support_GetVersion;
  sMess:=IntToStr(lVer shr 24) + '.';
  sTemp:=IntToStr((lVer shr 16) and $00ff);
  sMess:=sMess + Copy('00', 1 , 2 - Length(sTemp)) + sTemp + '.';
  sTemp:=IntToStr(lVer and $00ffff);
  sMess:=sMess + Copy('0000', 1 , 4 - Length(sTemp)) + sTemp;
  ShowMessage(sMess);
end;

procedure TTestForm.CRC32ButtonClick(Sender: TObject);
var
  lCRC32 : WORD32;
  sMess  : String;
begin
  // test CRC32 with reference string
  sMess:=InputBox('Testing CRC32',
                  'Something to checksum please:',
                  'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789');
  lCRC32:=CRC32_INITVALUE;
  lCRC32:=CRC32_Update(lCRC32, PChar(sMess), Length(sMess));
  lCRC32:=lCRC32 xor CRC32_DONEVALUE;
  ShowMessage(IntToHex(lCRC32, 8));
end;


procedure TTestForm.TestMD5ButtonClick(Sender: TObject);
var
  lI      : Integer;
  pCtx     : PMD5CTX;
  sRefStr : String;
  sMess   : String;
  digest  : array[0..MD5_DIGESTSIZE] of WORD8;
begin
  // run selftest
  if (MD5_SelfTest = BOOL_FALSE) then begin
    ShowMessage('MD5 selftest failed!');
    Exit;
  end;

  // MD5 test with reference string
  sRefStr:=InputBox('Testing MD5',
                    'Something to hash please:',
                    'ABCDEFG - Marshmellows for you and me!');
  pCtx:=MD5_Create;
  MD5_Update(pCtx, PChar(sRefStr), Length(sRefStr));
  MD5_Final(@digest, pCtx);
  MD5_Destroy(pCtx);
  sMess:='';
  for lI:=0 to (MD5_DIGESTSIZE - 1) do
    sMess:=sMess + IntToHex(digest[lI], 2);
  ShowMessage(sMess);
end;

procedure TTestForm.TestSHA1ButtonClick(Sender: TObject);
var
  lI      : Integer;
  pCtx    : PSHA1CTX;
  sRefStr : String;
  sMess   : String;
  digest  : array[0..SHA1_DIGESTSIZE] of WORD8;
begin
  // run selftest
  if (SHA1_SelfTest = BOOL_FALSE) then begin
    ShowMessage('SHA-1 selftest failed!');
    Exit;
  end;

  // SHA1 test with reference string
  sRefStr:=InputBox('Testing SHA-1',
                    'Something to hash please:',
                    'ABCDEFG - Marshmellows for you and me!');
  pCtx:=SHA1_Create;
  SHA1_Update(pCtx, PChar(sRefStr), Length(sRefStr));
  SHA1_Final(@digest, pCtx);
  SHA1_Destroy(pCtx);
  sMess:='';
  for lI:=0 to (SHA1_DIGESTSIZE - 1) do
    sMess:=sMess + IntToHex(digest[lI], 2);
  ShowMessage(sMess);
end;

procedure TTestForm.TestRandomPoolBtnClick(Sender: TObject);
const
  // (same as above...)
  RNDBUFSIZE = 128;
var
  lI     : Integer;
  rndctx : PYARROWCTX;
  buf    : array[0..RNDBUFSIZE - 1] of WORD8;
  sMess  : String;
  sSeed  : String;
begin
  sMess:='some secure random bytes made by Yarrow:' + #13#10;
  rndctx:=Yarrow_Create(nil, 0);
  Yarrow_GetData(rndctx, @buf, RNDBUFSIZE);
  for lI:=1 to RNDBUFSIZE do begin
    sMess:=sMess + IntToHex(buf[lI - 1], 2);
    if ((lI mod 20) = 0) then
      sMess:=sMess + #13#10
    else
      sMess:=sMess + ' ';
  end;
  sMess:=sMess + #13#10#13#10 + 'with additional seed:' + #13#10;
  sSeed:='This is additional random seed.';
  Yarrow_Destroy(rndctx);

  rndctx:=Yarrow_Create(PChar(sSeed), Length(sSeed));
  Yarrow_GetData(rndctx, @buf, RNDBUFSIZE);
  for lI:=1 to RNDBUFSIZE do begin
    sMess:=sMess + IntToHex(buf[lI - 1], 2);
    if ((lI mod 20) = 0) then
      sMess:=sMess + #13#10
    else
      sMess:=sMess + ' ';
  end;
  ShowMessage(sMess);
  Yarrow_Destroy(rndctx);
end;

procedure TTestForm.TestLZSSBtnClick(Sender: TObject);
const
  BUFSIZE = 6789;
  EXT_PAK = '.pak';
  EXT_OUT = '.out';
var
  nResult   : Integer;
  nFileSize : Integer;
  lCounter  : WORD32;
  lDeComp   : WORD32;
  inhandle  : File;
  outhandle : File;
  sFileName : String;
  inbuf     : array[0..BUFSIZE - 1] of WORD8;
  outbuf    : array[0..BUFSIZE + (BUFSIZE shr 1) - 1] of WORD8;
  lzssctx   : PLZSSCTX;
  bCond     : WORD8;
  blRepeat  : BYTEBOOL;
  blEOF     : Boolean;
begin
  // test LZSS compression with a selectable file
  with OpenDialog do begin
    Filter:='All files (*.*)|*.*';
    Title:='Select file for compression';

    FileName:='d:\test\test.dat';

    if (not Execute) then
      Exit
    else
      sFileName:=FileName;
  end;
  Application.ProcessMessages;
  AssignFile(inhandle, sFileName);
{$I-}
  Reset(inhandle, 1);
{$I+}
  if (IOResult <> 0) then begin
    ShowMessage('Cannot open original file "' + sFileName + '".');
    Exit;
  end;
  AssignFile(outhandle, sFileName + EXT_PAK);
{$I-}
  Rewrite(outhandle, 1);
{$I+}
  if (IOResult <> 0) then begin
    ShowMessage('Cannot open compressed file "' + sFileName + EXT_PAK + '".');
    CloseFile(inhandle);
    Exit;
  end;
  Application.ProcessMessages;
  lCounter:=0;
  nFileSize:=FileSize(inhandle);
  ProgressBar.Max:=nFileSize;
  ProgressBar.Position:=0;
  lzssctx:=LZSS_Create;
  bCond:=LZSS_START or LZSS_WORK;
  blEOF:=False;  // (we need a "manual" eof detection here)
  repeat
    BlockRead(inhandle, inbuf, BUFSIZE, nResult);
    ProgressBar.Position:=ProgressBar.Position + nResult;
    if (nResult <> BUFSIZE) then begin
      bCond:=bCond or LZSS_STOP;
      blEOF:=True;
    end;
    lDeComp:=LZSS_Compress(lzssctx, @inbuf, @outbuf, nResult, bCond);
    Inc(lCounter, lDeComp);
    BlockWrite(outhandle, outbuf, lDeComp);
    bCond:=bCond and (not LZSS_START);
  until (blEOF);
  System.CloseFile(outhandle);
  System.CloseFile(inhandle);
  ShowMessage('Compressed ' + IntToStr(nFileSize) + ' bytes into ' +
              IntToStr(lCounter) + ' bytes,' + #13#10 + 'put out into "' +
              sFileName + EXT_PAK + '".');

  // decompress to get a copy of the original file
  AssignFile(inhandle, sFileName + EXT_PAK);
{$I-}
  Reset(inhandle, 1);
{$I+}
  if (IOResult <> 0) then begin
    ShowMessage('Cannot open compressed file "' + sFileName + EXT_PAK + '".');
    LZSS_Destroy(lzssctx);
    Exit;
  end;
  AssignFile(outhandle, sFileName + EXT_OUT);
{$I-}
  Rewrite(outhandle, 1);
{$I+}
  if (IOResult <> 0) then begin
    ShowMessage('Cannot open output file "' + sFileName + EXT_OUT + '".');
    CloseFile(inhandle);
    LZSS_Destroy(lzssctx);
    Exit;
  end;
  lCounter:=0;
  nFileSize:=FileSize(inhandle);
  ProgressBar.Max:=nFileSize;
  ProgressBar.Position:=0;
  bCond:=LZSS_START or LZSS_WORK;
  blEOF:=False;
  repeat
    BlockRead(inhandle, inbuf, BUFSIZE, nResult);
    ProgressBar.Position:=ProgressBar.Position + nResult;
    if (nResult <> BUFSIZE) then begin
      bCond:=bCond or LZSS_STOP;
      blEOF:=True;
    end;
    blRepeat:=BOOL_FALSE;
    repeat
      lDeComp:=LZSS_Decompress(lzssctx, @inbuf, @outbuf, nResult,
                               BUFSIZE, bCond, @blRepeat);
      BlockWrite(outhandle, outbuf, lDeComp);
      Inc(lCounter, lDeComp);
      bCond:=bCond and (not LZSS_START);
    until (blRepeat = BOOL_FALSE);
  until (blEOF);
  System.CloseFile(outhandle);
  System.CloseFile(inhandle);
  ShowMessage('Decompressed ' + IntToStr(nFileSize) + ' bytes into ' +
              IntToStr(lCounter) + ' bytes,' + #13#10 + 'put out into "' +
              sFileName + EXT_OUT + '".');
  LZSS_Destroy(lzssctx);
end;

procedure TTestForm.AboutBtnClick(Sender: TObject);
begin
  // show copyright information
  Application.MessageBox(PChar('CryptPak Test' + #13#10 +
                         'Copyright © 1998-2002 Markus Hahn' +
                         #13#10 + 'Open source. All rights reserved.'),
                         'About',
                         MB_ICONINFORMATION);
end;

procedure TTestForm.FormCreate(Sender: TObject);
begin
  // place us in the middle of the screen
  Left:=(Screen.Width - Width) shr 1;
  Top:=(Screen.Height - Height) shr 1;
end;

procedure TTestForm.TestCipherServerBtnClick(Sender: TObject);
const
  BLOCKSPERBUF    = 10000;
  BENCHLOOPS_BASE = 8192;
var
  lI            : WORD32;
  lNumOfBlocks  : WORD32;
  lKeySize      : WORD32;
  lResult       : WORD32;
  lTicks        : WORD32;
  lBenchLoops   : WORD32;
  pInitData     : PChar;
  pInitDataShow : PChar;
  pBenchBuf     : Pointer;
  sInBuf        : String;
  sOutBuf       : String;
  sLastBuf      : String;
  sCipherName   : String;
  sMessage      : String;
  key           : array[0..65535] of WORD8;
  rndbuf        : array[0..7] of WORD8;
  qRate         : WORD64;
  infoblock     : TCIPHERINFOBLOCK;
  pCtx          : PCIPHERCTX;
  csess         : PCIPHERSESSION;
begin

  // get the cipher name
  sCipherName:='Blowfish';
  if (not InputQuery('Test CipherServer', 'Enter the cipher name:',
                     sCipherName)) then Exit;

  // get cipher information
  infoblock.lSizeOf:=SizeOf(TCIPHERINFOBLOCK);
  lResult:=CipherServer_GetCipherInfo(PChar(sCipherName), @infoblock);
  if (lResult <> CIPHERSERVER_ERROR_NOERROR) then begin
    ShowMessage('ERROR #' + IntToStr(lResult));
    Exit;
  end;

  // show cipher characteristics
  with infoblock do begin
    sMessage:='Block Size : '      + IntToStr(lBlockSize) + #13#10 +
	      'Key Size : '        + IntToStr(lKeySize) + #13#10 +
	      'Init. Data Size : ' + IntToStr(lInitDataSize) + #13#10 +
	      'Context Size : '    + IntToStr(lContextSize) + #13#10 +
	      'SizeOf : '          + IntToStr(lSizeOf) + #13#10 +
	      'Cipher is : $'      + IntToHex(bCipherIs, 2) +  #13#10 +
	      'Hashes Key : '      + IntToStr(blOwnHasher) + #13#10 +
              #13#10;
  end;

  // open the cipher (using the built-in random generator with no extra seed)
  sMessage:=sMessage + 'creating context';
  lResult:=CipherServer_Create(PChar(sCipherName), pCtx, Nil, Nil, Nil, 0);
  if (lResult <> CIPHERSERVER_ERROR_NOERROR) then begin
    ShowMessage(sMessage + ', ERROR #' + IntToStr(lResult));
    Exit;
  end;
  sMessage:=sMessage + ', done.' + #13#10;

  // execute the cipher's self test
  sMessage:=sMessage + 'executing (extended) selftest';
  lResult:=CipherServer_ExecuteSelfTest(pCtx, BOOL_TRUE);
  if (lResult <> CIPHERSERVER_ERROR_NOERROR) then begin
    ShowMessage(sMessage + ', ERROR #' + IntToStr(lResult));
    CipherServer_Destroy(pCtx);
    Exit;
  end;
  sMessage:=sMessage + ', done.' + #13#10;

  // show cipher characteristics
  FillChar(infoblock, SizeOf(infoblock), 0);  // (just to be sure)
  lResult:=CipherServer_getInfoBlock(pCtx, @infoblock);
  if (lResult <> CIPHERSERVER_ERROR_NOERROR) then begin
    ShowMessage(sMessage + 'ERROR #' + IntToStr(lResult));
    CipherServer_Destroy(pCtx);
    Exit;
  end;
  with infoblock do begin
    sMessage:=sMessage +
              'Direct information block readout:' + #13#10 +
 	      '* Block Size: '      + IntToStr(lBlockSize) + #13#10 +
	      '* Key Size: '        + IntToStr(lKeySize) + #13#10 +
	      '* Init. Data Size: ' + IntToStr(lInitDataSize) + #13#10 +
	      '* Context Size: '    + IntToStr(lContextSize) + #13#10 +
	      '* Size Of: '         + IntToStr(lSizeOf) + #13#10 +
	      '* Cipher is: $'      + IntToHex(bCipherIs, 2) + #13#10 +
	      '* Hashes Key: '      + IntToStr(blOwnHasher) + #13#10 +
              #13#10;
  end;

  // open a new session for encryption, using a simply created key
  if (infoblock.blOwnHasher = BOOL_TRUE) then
    lKeySize:=1024
  else
    lKeySize:=infoblock.lKeySize;
  for lI:=0 to lKeySize - 1 do
    key[lI]:=lI and $0ff;
  GetMem(pInitData, infoblock.lInitDataSize);
  lResult:=CipherServer_OpenSession(CIPHERSERVER_MODE_ENCRYPT,
		                    @key,
                                    lKeySize,
                                    pCtx,
				    pInitData,
                                    csess);
  if (lResult <> CIPHERSERVER_ERROR_NOERROR) then begin
    ShowMessage(sMessage + 'ERROR #' + IntToStr(lResult));
    CipherServer_Destroy(pCtx);
    FreeMem(pInitData);
    Exit;
  end;

  // show the created init. data, i.n.
  if (infoblock.lInitDataSize <> 0) then begin
    sMessage:=sMessage + 'init. data returned by the cipher: ';
    pInitDataShow:=pInitData;
    for lI:=0 to infoblock.lInitDataSize - 1 do begin
      sMessage:=sMessage + IntToHex(Ord(pInitDataShow^), 2) + ' ';
      Inc(pInitDataShow);
    end;
    sMessage:=sMessage + #13#10;
  end;

  // get some test data from the user
  sInBuf:=InputBox('Testing ' + sCipherName,
                   'Something to encrypt please:',
                   'Enter your message to scramble right here.');
  lNumOfBlocks:=Length(sInBuf);
  if (lNumOfBlocks mod infoblock.lBlockSize <> 0) then
    lNumOfBlocks:=lNumOfBlocks div infoblock.lBlockSize + 1
  else
    lNumOfBlocks:=lNumOfBlocks div infoblock.lBlockSize;
  if (infoblock.lBlockSize > 1) then
    sMessage:=sMessage + 'number of ' + IntToStr(infoblock.lBlockSize) +
              ' byte blocks = ' + IntToStr(lNumOfBlocks) + #13#10;

  // encrypt this data (we use strings here for an easier buffer handling)
  SetLength(sInBuf, 65536);
  SetLength(sOutBuf, 65536);
  CipherServer_EncryptBlocks(csess,
                             PChar(sInBuf),
                             PChar(sOutBuf),
                             lNumOfBlocks);
  sMessage:=sMessage + 'encrypted message: ';
  for lI:=1 to lNumOfBlocks * infoblock.lBlockSize do begin
    if (sOutBuf[lI] < ' ') then
      sMessage:=sMessage + Chr(255)  // (show non-printable chars, too)
    else
      sMessage:=sMessage + sOutBuf[lI];
    if ((lI mod infoblock.lBlockSize = 0) and (infoblock.lBlockSize > 1)) then
      sMessage:=sMessage + ' ';
  end;
  sMessage:=sMessage + #13#10;

  // close the session
  lResult:=CipherServer_CloseSession(csess);
  if (lResult <> CIPHERSERVER_ERROR_NOERROR) then begin
    ShowMessage(sMessage + 'ERROR #' + IntToStr(lResult));
    CipherServer_Destroy(pCtx);
    FreeMem(pInitData);
    Exit;
  end;

  // open a session for decryption
  lResult:=CipherServer_OpenSession(CIPHERSERVER_MODE_DECRYPT,
                                    @key,
                                    lKeySize,
                                    pCtx,
                                    pInitData,
                                    csess);
  if (lResult <> CIPHERSERVER_ERROR_NOERROR) then begin
    ShowMessage(sMessage + 'ERROR #' + IntToStr(lResult));
    CipherServer_Destroy(pCtx);
    FreeMem(pInitData);
    Exit;
  end;

  // reset three times before decrypting, just for fun here
  for lI:=1 to 3 do
    CipherServer_ResetSession(csess, pInitData);

  // decrypt the data, interrupt after the first block, if possible
  SetLength(sLastBuf, 65536);
  if (lNumOfBlocks < 2) then
    CipherServer_DecryptBlocks(csess,
                               PChar(sOutBuf),
                               PChar(sLastBuf),
                               lNumOfBlocks,
                               CIPHER_NULL)
  else begin
    CipherServer_DecryptBlocks(csess,
                               PChar(sOutBuf),
                               PChar(sLastBuf),
                               1,
                               CIPHER_NULL);
    CipherServer_DecryptBlocks(csess,
                               @sOutBuf[infoblock.lBlockSize + 1],
    	                       @sLastbuf[infoblock.lBlockSize + 1],
			       lNumOfBlocks - 1,
                               PChar(sOutBuf));
  end;
  sMessage:=sMessage + 'decrypted message: ' + PChar(sLastBuf) + #13#10;

  // get some random bytes
  CipherServer_GetRandomData(pCtx, @rndbuf, 8);
  sMessage:=sMessage + 'Some random bytes: ' +
            IntToHex(rndbuf[0], 2) + ' ' +  IntToHex(rndbuf[1], 2) + ' ' +
            IntToHex(rndbuf[2], 2) + ' ' +  IntToHex(rndbuf[3], 2) + ' ' +
            IntToHex(rndbuf[4], 2) + ' ' +  IntToHex(rndbuf[5], 2) + ' ' +
            IntToHex(rndbuf[6], 2) + ' ' +  IntToHex(rndbuf[7], 2) + #13#10;
  ShowMessage(sMessage);

  // close the session
  lResult:=CipherServer_CloseSession(csess);
  if (lResult <> CIPHERSERVER_ERROR_NOERROR) then begin
    ShowMessage(sMessage + 'ERROR #' + IntToStr(lResult));
    CipherServer_Destroy(pCtx);
    FreeMem(pInitData);
    Exit;
  end;

  // execute benchmark, i.n.
  if (Application.MessageBox('Execute benchmark?', 'Confirm',
                             MB_ICONQUESTION or MB_YESNO) = IDYES) then begin
    GetMem(pBenchBuf, BLOCKSPERBUF * infoblock.lBlockSize);
    lResult:=CipherServer_OpenSession(CIPHERSERVER_MODE_ENCRYPT,
	                              @key,
                                      lKeySize,
                                      pCtx,
	     		              pInitData,
                                      csess);
    if (lResult <> CIPHERSERVER_ERROR_NOERROR) then begin
      ShowMessage('ERROR #' + IntToStr(lResult));
      CipherServer_Destroy(pCtx);
      FreeMem(pInitData);
      Exit;
    end;

    // (remember that this benchmark only works with ciphers of a block size
    //  smaller than BENCHLOOPS_BASE)
    lBenchLoops:=BENCHLOOPS_BASE div infoblock.lBlockSize;
    ProgressBar.Max:=lBenchLoops;
    ProgressBar.Position:=0;
    lTicks:=GetTickCount;
    for lI:=1 to lBenchLoops do  begin
      CipherServer_EncryptBlocks(csess, pBenchBuf, pBenchBuf, BLOCKSPERBUF);
      ProgressBar.Position:=lI;
    end;
    lTicks:=GetTickCount - lTicks;
    qRate:=WORD64(BLOCKSPERBUF) *
           WORD64(infoblock.lBlockSize) *
           WORD64(lBenchLoops) *
           WORD64(1000);
    qRate:=qRate div WORD64(lTicks);
    FreeMem(pBenchBuf);
    ShowMessage(IntToStr(qRate) + ' bytes/sec');
    lResult:=CipherServer_CloseSession(csess);
    if (lResult <> CIPHERSERVER_ERROR_NOERROR) then begin
      ShowMessage('ERROR #' + IntToStr(lResult));
      CipherServer_Destroy(pCtx);
      FreeMem(pInitData);
      Exit;
    end;
  end;

  // free the init. data buffer
  FreeMem(pInitData);

  // close the cipher
  lResult:=CipherServer_Destroy(pCtx);
  if (lResult <> CIPHERSERVER_ERROR_NOERROR) then begin
    ShowMessage(sMessage + 'ERROR #' + IntToStr(lResult));
    Exit;
  end;

end;


end.
