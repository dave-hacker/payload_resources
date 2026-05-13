import pefile
import optparse
import os

def test(path):
    if not os.path.exists(path):
        print("[-] File Not Found: {}".format(path))
        return

    # Strip the .dll extension (case-insensitive) to get the bare module name
    base = path
    if base.lower().endswith(".dll"):
        base = base[:-4]

    pe = pefile.PE(path)
    print("EXPORTS")
    for sym in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        if sym.name is None:
            # Ordinal-only export, skip (no name to forward by)
            continue
        name = sym.name.decode()
        print('{name}="{base}.{name}" @{ordinal}'.format(
            name=name, base=base, ordinal=sym.ordinal
        ))

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f', dest="file", help="Dll Path")
    (option, args) = parser.parse_args()
    if option.file:
        test(option.file)
    else:
        print(r"Usage: python comment.py -f C:\path\to\your.dll")
        parser.print_help()