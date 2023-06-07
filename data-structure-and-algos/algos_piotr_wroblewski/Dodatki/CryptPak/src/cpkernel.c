

#ifdef WIN32
  #include <windows.h>
#endif


#include "cpkernel.h"
#include "Twofish.h"


void CRYPTPAK_API CryptPak_Init()
{
  Twofish_PreCompMDS();
}



#ifdef CRYPTPAK_DLL

BOOL APIENTRY DllMain
  (HANDLE hModule, 
   DWORD ul_reason_for_call, 
   LPVOID lpReserved) 
{
  if (DLL_PROCESS_ATTACH == ul_reason_for_call)
  {
      CryptPak_Init();
  }

  return TRUE;
}

#endif


