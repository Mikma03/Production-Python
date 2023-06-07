
{
  defines basic primitive data types to avoid system independencies
}


unit BasicTypes;

interface

// basic unsigned integer types
type
  WORD8  = Byte;      // unsigned 8bit integer, prefix "b"
  WORD16 = Word;      // unsigned 16bit integer, prefix "w"
  WORD32 = Longword;  // unsigned 32bit integer, prefix "l"
  WORD64 = Int64;     // unsigned 64bit integer, prefix "q"

// pointer types for unsigned integers
type
  PWORD8  = ^Byte;      // prefix "pb"
  PWORD16 = ^Word;      // prefix "pw"
  PWORD32 = ^Longword;  // prefix "pl"
  PWORD64 = ^Int64;     // prefix "ql"

// to pack two WORD32 into one WORD64 (Delphi 4+ only)
// -> the low 32bit half
// -> the high 32bit half
// <- the assembled 64bit integer
function MakeWORD64(lLoWord : WORD32;
                    lHiWord : WORD32) : WORD64;

// to extract the lower 32bit of a WORD64
// -> 64bit integer
// <- the lower 32bit of it
function GetWORD64Lo(lValue : WORD64) : WORD32;

// to extract the higher 32bit of a WORD64
// -> 64bit integer
// <- the higher 32bit of it
function GetWORD64Hi(lValue : WORD64) : WORD32;



// just a NULL definition
const
  NULL = Pointer(0);

// boolean definitions
type
  BYTEBOOL  = Byte;    // 8bit boolean, prefix "bl"
  PBYTEBOOL = ^Byte;   // prefix "pbl"
const
  BOOL_FALSE = 0;
  BOOL_TRUE  = 1;


// array pointers (we cannot use PByteArray or PWordArray because they are
// restricted to arrays with the size of 32kB max., using dynamic arrays is
// also no standard solution because sometimes a pure pointer has to been
// converted into an byte array pointer e.g.)
const
  MAXDATA = $7fffffff;  // (max size of a data element equals 2GB - 1)
type
  PWORD8Buf  = ^TWORD8Buf;
  PWORD16Buf = ^TWORD16Buf;
  PWORD32Buf = ^TWORD32Buf;

  // (only the pointer types are usable)
  TWORD8Buf  = array[0..MAXDATA - 1] of WORD8;
  TWORD16Buf = array[0..(MAXDATA div 2) - 1] of WORD16;
  TWORD32Buf = array[0..(MAXDATA div 4) - 1] of WORD32;


implementation

function MakeWORD64(lLoWord : WORD32; lHiWord : WORD32) : WORD64;
begin
  Result:= (WORD64(lHiWord) shl 32) or WORD64(lLoWord);
end;

function GetWORD64Lo(lValue : WORD64) : WORD32;
begin
  Result:=lValue and $0ffffffff;
end;

function GetWORD64Hi(lValue : WORD64) : WORD32;
begin
  Result:=(lValue shr 32) and $0ffffffff;
end;


end.

