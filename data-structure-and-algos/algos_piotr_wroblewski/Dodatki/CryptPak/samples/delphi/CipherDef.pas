

unit CipherDef;

interface
uses BasicTypes;


const
  CIPHER_NULL = Pointer(0);


const
  CIPHER_IS_XORSTREAM = 1;
  CIPHER_IS_BLOCK     = 2;
  CIPHER_IS_BLOCKLINK = 4;
  CIPHER_IS_NOBLOCK   = 8;
  CIPHER_IS_DEBUG     = 128;


const
  CIPHER_MAX_NAME_LEN = 32;


const
  CIPHER_MODE_ENCRYPT = 0;
  CIPHER_MODE_DECRYPT = 1;


type
  PCIPHERINFOBLOCK = ^TCIPHERINFOBLOCK;
  TCIPHERINFOBLOCK = packed record
    lSizeOf       : WORD32;
    lBlockSize    : WORD32;
    lKeySize      : WORD32;
    lInitDataSize : WORD32;
    lContextSize  : WORD32;
    bCipherIs     : WORD8;
    blOwnHasher   : BYTEBOOL;
  end;



type

TCipher_RandomGenerator = procedure(pTargetBuffer : Pointer;
                                    lNumOfRandomBytes : WORD32;
                                    pData : Pointer); stdcall;



implementation
end.













