
CC   = bcc32
LINK = ilink32
RC   = brc32
LIB  = implib

CCFLAGS = -c -O2 -tW -P -DWIN32 -w-8057 -DCRYPTPAK_DLL -DEXPORT_DLL
LINKFLAGS= -Gz -Tpd
LINKSTART = c0d32x.obj
LINKLIBS = import32.lib cw32mt.lib
BINDIR=..\bin

allobjs = 				\
	Blowfish.obj		\
	cast.obj			\
	CipherServer.obj	\
	Cobra128.obj		\
	cpkernel.obj		\
	CRC32.obj			\
	IDEA.obj			\
	LZSS.obj			\
	MARS.obj			\
	MD5.obj				\
	PC1.obj				\
	RandomPool.obj		\
	RC6.obj				\
	Rijndael.obj		\
	Serpent.obj			\
	SHA1.obj			\
	Support.obj			\
	TMS.obj				\
	TripleDES.obj		\
	Twofish.obj			\
	Yarrow.obj

all: CryptPak.dll CryptPak.lib

CryptPak.lib: CryptPak.dll
    $(LIB) $(BINDIR)\CryptPak.lib $(BINDIR)\CryptPak.dll 

CryptPak.dll: $(allobjs) CryptPak.res
    $(LINK) $(LINKFLAGS) $(LINKSTART) $(allobjs),$(BINDIR)\$*,,$(LINKLIBS),CryptPak.def,CryptPak.res

CryptPak.res: CryptPak.rc
    $(RC) -r $?

Blowfish.obj: Blowfish.c
    $(CC) $(CCFLAGS) $?
    
cast.obj: cast.c
    $(CC) $(CCFLAGS) $?

CipherServer.obj: CipherServer.c
    $(CC) $(CCFLAGS) $?

Cobra128.obj: Cobra128.c
    $(CC) $(CCFLAGS) $?

cpkernel.obj: cpkernel.c
    $(CC) $(CCFLAGS) $?

CRC32.obj: CRC32.c
    $(CC) $(CCFLAGS) $?

IDEA.obj: IDEA.c
    $(CC) $(CCFLAGS) $?

LZSS.obj: LZSS.c
    $(CC) $(CCFLAGS) $?

MARS.obj: MARS.c
    $(CC) $(CCFLAGS) $?

MD5.obj: MD5.c
    $(CC) $(CCFLAGS) $?

PC1.obj: PC1.c
    $(CC) $(CCFLAGS) $?

RandomPool.obj: RandomPool.c
    $(CC) $(CCFLAGS) $?

RC6.obj: RC6.c
    $(CC) $(CCFLAGS) $?

Rijndael.obj: Rijndael.c
    $(CC) $(CCFLAGS) $?

Serpent.obj: Serpent.c
    $(CC) $(CCFLAGS) $?

SHA1.obj: SHA1.c
    $(CC) $(CCFLAGS) $?

Support.obj: Support.c
    $(CC) $(CCFLAGS) $?

TMS.obj: TMS.c
    $(CC) $(CCFLAGS) $?

TripleDES.obj: TripleDES.c
    $(CC) $(CCFLAGS) $?

Twofish.obj: Twofish.c
    $(CC) $(CCFLAGS) $?

Yarrow.obj: Yarrow.c
    $(CC) $(CCFLAGS) $?
