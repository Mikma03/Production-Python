
CC   = bcc32
LINK = ilink32
RC   = brc32

CCFLAGS = -c -O2 -tW -DWIN32 -DCRYPTPAK_DLL -I..\..\src
LINKFLAGS= -ap
LINKSTART = C0X32.OBJ
LINKLIBS = import32.lib cw32mt.lib ..\..\bin\CryptPak.lib 
BINDIR=..\..\bin

allobjs =               \
    TestCipherServer.obj\
    TestCRC32.obj       \
    TestCrunchKey.obj   \
    TestCryptPak.obj    \
    TestLZSS.obj        \
    TestMD5.obj         \
    TestRandomPool.obj  \
    TestSHA1.obj        \
    TestYarrow.obj

all: TestCryptPak.exe

TestCryptPak.exe: $(allobjs)
    $(LINK) $(LINKFLAGS) $(LINKSTART) $(allobjs),$(BINDIR)\$*,,$(LINKLIBS),,

TestCipherServer.obj: TestCipherServer.cpp
    $(CC) $(CCFLAGS) $?

TestCRC32.obj: TestCRC32.cpp
    $(CC) $(CCFLAGS) $?

TestCrunchKey.obj: TestCrunchKey.cpp
    $(CC) $(CCFLAGS) $?

TestLZSS.obj: TestLZSS.cpp
    $(CC) $(CCFLAGS) $?

TestCryptPak.obj: TestCryptPak.cpp
    $(CC) $(CCFLAGS) $?

TestMD5.obj: TestMD5.cpp
    $(CC) $(CCFLAGS) $?

TestRandomPool.obj: TestRandomPool.cpp
    $(CC) $(CCFLAGS) $?

TestSHA1.obj: TestSHA1.cpp
    $(CC) $(CCFLAGS) $?

TestYarrow.obj: TestYarrow.cpp
    $(CC) $(CCFLAGS) $?
