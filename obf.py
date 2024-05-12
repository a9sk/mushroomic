import sys
import os

def help():
    print("""
          Mushroomic 1.0.0 (Git v1.0.0 packaged an 1.0.0-1)
          Interactively do something maybe
          See https://github.com/a9sk/mushroomic for more information.

          Usage: python3 obf.py [file to obfuscate] ...

          Required:
                  -c, code                pass the whole name of the code you want to obfuscate
  
          Obfuscation:
                  -a, all                 uses all of the tecniques implemented
                  -f, functions           modify functions names
                  -v, variables           modify variables names (pay attention to local variables)
                  -b, binary              uses binary to obfuscate (deobfuscated from added code)
                  -e, exadecimal          uses hex to obfuscate (deobfuscated from added code) 

          Miscellaneous:
                  -h, --h*                 display this help and exit 
""")
def banner():
    print("""
                                ____                      
                _.-'78o `\"`--._               
            ,o888o.  .o888o,   ''-.          
            ,88888P  `78888P..______.]         
            /_..__..----""        __.'
            `-._       /""| _..-''
                "`-----\  `\
                        |   ;.-""--..
                        | ,8o.  o88. `.
                        `;888P  `788P  :
                .o""-.|`-._         ./
                J88 _.-/    ";"-P----'
                `--'\`|     /  /
                    | /     |  |
                    \|     /   |   https://github.com/a9sk/mushroomic
                    `-----`---' 

            Mushroomic v1.0.0 @a9sk
""")


if __name__ == '__main__':
    args = sys.argv[1:]

    if '-h' in args:
        help()
        exit()

    
    if '-c' in args: 
        index_code = args.index('-c')
        original_name = args[index_code + 1]
        file_name, file_extension = original_name.rsplit('.', 1)
        if file_extension != 'py':
            print('[!] The obfuscation only works with python scripts for now')
            print('[*] Pass a .py script as an argument after -c')
            exit()
        if os.path.exists(original_name):
            print('[*] File found in the directory')
            with open(original_name, 'r') as original:
                original_code=original.read()
                print('[*] File opened correctly')
        else:
                print("[!] The file does not exist")
                exit()     
    else:
        print("[!] Missing '-c' flag followed by a file name.")
        exit()

    #! Should be done only after the whole code is obfuscated 

    out = f"{file_name}.obf.{file_extension}"

    with open(out, "w") as output:
        print('[*] Saving the obfuscated code in')
        print(out)
        output.write(modified_code)

        

    
    