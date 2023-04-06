
#ifndef __CPCONFIG_H
#define __CPCONFIG_H


#ifdef __cplusplus
extern "C" {
#endif


// import-export definitions, this allows CryptPak
// to be used in a DLL or even as a normal part
// of a program (like in Linux)


#ifdef WIN32

#ifdef CRYPTPAK_DLL

  #define CRYPTPAK_CALLCONV __stdcall

  #ifdef EXPORT_DLL
    #define CRYPTPAK_API __declspec(dllexport) CRYPTPAK_CALLCONV
  #else
    #define CRYPTPAK_API __declspec(dllimport) CRYPTPAK_CALLCONV
  #endif

#else

  #define CRYPTPAK_CALLCONV
  #define CRYPTPAK_API

#endif

#endif



#ifdef UNIX

  #define CRYPTPAK_CALLCONV
  #define CRYPTPAK_API

#endif

#ifdef __cplusplus
}
#endif

#endif
