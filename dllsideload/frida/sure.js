// to make sure the dll is loaded before the function intercept is introduced
const dllName = "{DLL_FULL_PATH}";
Module.load(dllName);

// find the address of the function
const pPrintUIEntryW = Process.getModuleByName("{DLL_NAME}").getExportByName("{FUNC_NAME}");

// intercept the call
Interceptor.attach(pPrintUIEntryW, {
    onEnter: function (args) {
        send("The function was called");
    },
    onLeave: function (retval) {
    }
});