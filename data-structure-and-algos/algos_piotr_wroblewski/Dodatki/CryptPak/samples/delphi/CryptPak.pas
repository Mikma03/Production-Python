
unit CryptPak;

interface
uses Windows,
     BasicTypes,
     CipherDef;


function Support_GetVersion : WORD32; stdcall; external 'CryptPak.dll';


const CRUNCHKEY_METHOD_SHAEXTENDER   = 0;
const CRUNCHKEY_METHOD_SHAEXTXORLOOP = 1;


function Support_GetCrunchKeyBuildBufSize(lPasswLen : WORD32;
   			         	  lSaltLen : WORD32;
					  lOutputLen : WORD32;
  					  bMethod : WORD8) : WORD32;
                                            stdcall; external 'Cryptpak.dll';

function Support_CrunchKey(pPassw : Pointer;
             	    	   lPasswLen : WORD32;
			   pSalt : Pointer;
			   lSaltLen : WORD32;
			   pOutput : Pointer;
			   lOutputLen : WORD32;
                           bMethod : WORD8;
			   pBuildBuf : Pointer = Nil) : BYTEBOOL;
                             stdcall; external 'Cryptpak.dll';



const
  MD5_DIGESTSIZE = 16;

type
  PMD5CTX = Pointer;


function MD5_SelfTest : BYTEBOOL; stdcall; external 'CryptPak.dll';

function MD5_Create : PMD5CTX; stdcall; external 'CryptPak.dll';

procedure MD5_Destroy(pCtx : PMD5CTX); stdcall; external 'CryptPak.dll';

procedure MD5_Reset(pCtx : PMD5CTX); stdcall; external 'CryptPak.dll';

procedure MD5_Update(pCtx : PMD5CTX;
                     pData : Pointer;
                     lNumOfBytes : WORD32); stdcall; external 'CryptPak.dll';

procedure MD5_Final(pDigest : Pointer;
                    pCtx : PMD5CTX); stdcall; external 'CryptPak.dll';


const
  SHA1_DIGESTSIZE = 20;

type
  PSHA1CTX = Pointer;


function SHA1_SelfTest : BYTEBOOL; stdcall; external 'CryptPak.dll';

function SHA1_Create : PSHA1CTX; stdcall; external 'CryptPak.dll';

procedure SHA1_Destroy(pCtx : PSHA1CTX); stdcall; external 'CryptPak.dll';

procedure SHA1_Reset(pCtx : PSHA1CTX); stdcall; external 'CryptPak.dll';

procedure SHA1_Update(pCtx : PSHA1CTX;
                      pData : Pointer;
                      lNumOfBytes : WORD32); stdcall; external 'CryptPak.dll';

procedure SHA1_Final(pDigest : Pointer;
                     pCtx : PSHA1CTX); stdcall; external 'CryptPak.dll';


const
  CRC32_INITVALUE = $ffffffff;
  CRC32_DONEVALUE = $ffffffff;

function CRC32_Update(lOldCRC32 : WORD32;
                      pData : Pointer;
                      lNumOfBytes : WORD32) : WORD32;
                        stdcall; external 'CryptPak.dll';


type
  PRANDOMPOOLCTX = Pointer;


function RandomPool_Create(pAddSeed : Pointer;
                           lAddSeedLen : WORD32) : PRANDOMPOOLCTX;
                             stdcall; external 'CryptPak.dll';

procedure RandomPool_Destroy(pCtx : PRANDOMPOOLCTX);
                               stdcall; external 'CryptPak.dll';

procedure RandomPool_Reseed(pCtx : PRANDOMPOOLCTX;
	                    pSeed : pointer;
                            lSeedLen : WORD32);
                              stdcall; external 'CryptPak.dll';

procedure RandomPool_GetData(pCtx : PRANDOMPOOLCTX;
			     pDataTarget : Pointer;
			     lNumOfBytes : WORD32);
                               stdcall; external 'CryptPak.dll';



type
  PYARROWCTX = Pointer;


function Yarrow_Create(pAddSeed : Pointer;
                           lAddSeedLen : WORD32) : PYARROWCTX;
                             stdcall; external 'CryptPak.dll';

procedure Yarrow_Destroy(pCtx : PYARROWCTX);
                               stdcall; external 'CryptPak.dll';

procedure Yarrow_Reseed(pCtx : PYARROWCTX;
	                    pSeed : pointer;
                            lSeedLen : WORD32);
                              stdcall; external 'CryptPak.dll';

procedure Yarrow_GetData(pCtx : PYARROWCTX;
			     pDataTarget : Pointer;
			     lNumOfBytes : WORD32);
                               stdcall; external 'CryptPak.dll';

const
     LZSS_START = 1;
     LZSS_WORK  = 2;
     LZSS_STOP  = 4;


type
  PLZSSCTX = Pointer;


function LZSS_Create : PLZSSCTX; stdcall; external 'CryptPak.dll';

procedure LZSS_Destroy(pCtx : PLZSSCTX);  stdcall; external 'CryptPak.dll';

function LZSS_Compress(pCtx : PLZSSCTX;
		       pSource : Pointer;
	               pTarget : Pointer;
	               lNumOfBytes : WORD32;
	               bCondition : WORD8) : WORD32;
                         stdcall; external 'CryptPak.dll';

function LZSS_Decompress(pCtx : PLZSSCTX;
		         pSource : Pointer;
	                 pTarget : Pointer;
	                 lNumOfBytes : WORD32;
	                 lSizeOfOutputBuffer : WORD32;
	                 bCondition : WORD8;
                         pblRepeatMe : PBYTEBOOL) : WORD32;
                           stdcall; external 'CryptPak.dll';



const
  CIPHERSERVER_ERROR_NOERROR            = 0;
  CIPHERSERVER_ERROR_ERROR	        = 1;
  CIPHERSERVER_ERROR_INVALIDCIPHER      = 2;
  CIPHERSERVER_ERROR_OUTOFMEMORY	= 3;
  CIPHERSERVER_ERROR_WEAKKEY    	= 4;
  CIPHERSERVER_ERROR_CIPHERNOTFOUND     = 5;

  
const
  CIPHERSERVER_MODE_ENCRYPT = CIPHER_MODE_ENCRYPT;
  CIPHERSERVER_MODE_DECRYPT = CIPHER_MODE_DECRYPT;


type
  PCIPHERCTX = Pointer;

type
  PCIPHERSESSION = Pointer;

  
function CipherServer_GetCipherNames(var ppList : Pointer) : WORD32;
                                       stdcall; external 'CryptPak.dll';

function CipherServer_GetCipherInfo(pCipherName : PChar;
	                            pInfoBlock : PCIPHERINFOBLOCK) : WORD32;
                                      stdcall; external 'CryptPak.dll';

function CipherServer_Create(pCipherName : PChar;
   	                     var pCtxPtr : PCIPHERCTX;
			     RandGenFunc : TCipher_RandomGenerator
                                             = CIPHER_NULL;
			     pRandGenData : Pointer = CIPHER_NULL;
                             pRandSeed : Pointer = CIPHER_NULL;
                             lRandSeedLen : WORD32 = 0) : WORD32;
                               stdcall; external 'CryptPak.dll';

function CipherServer_Destroy(pCtx : PCIPHERCTX) : WORD32;
                                stdcall; external 'CryptPak.dll';

function CipherServer_ExecuteSelfTest(pCtx : PCIPHERCTX;
	                              blExtendedTest : BYTEBOOL) : WORD32;
                                        stdcall; external 'CryptPak.dll';

function CipherServer_GetInfoBlock(pCtx : PCIPHERCTX;
	                           pInfoBlock : PCIPHERINFOBLOCK) : WORD32;
                                     stdcall; external 'CryptPak.dll';

function CipherServer_OpenSession(lMode : WORD32;
                                  pKey : Pointer;
                                  lKeyLen : WORD32;
                                  pCtx : PCIPHERCTX;
                                  pInitData : Pointer;
                                  var pSessionHandle : PCIPHERSESSION) : WORD32;
                                    stdcall; external 'CryptPak.dll';

procedure CipherServer_ResetSession (pSessionHandle : PCIPHERSESSION;
                                     pInitData : Pointer); stdcall;
                                       external 'CryptPak.dll';

function CipherServer_CloseSession (pSessionHandle : PCIPHERSESSION) : WORD32;
                                      stdcall; external 'CryptPak.dll';

procedure CipherServer_EncryptBlocks(pSessionHandle : PCIPHERSESSION;
  				     pSource : Pointer;
                                     pTarget : Pointer;
                                     lNumOfBlocks : WORD32);
                                       stdcall; external 'CryptPak.dll';

procedure CipherServer_DecryptBlocks(pSessionHandle : PCIPHERSESSION;
				     pSource : Pointer;
                                     pTarget : Pointer;
                                     lNumOfBlocks : WORD32;
                                     pPreviousBlock : Pointer);
                                       stdcall; external 'CryptPak.dll';

procedure CipherServer_GetRandomData(pCtx : PCIPHERCTX;
                                     pTarget : Pointer;
                                     lNumOfBytes : WORD32);
                                       stdcall; external 'CryptPak.dll';


implementation

end.
