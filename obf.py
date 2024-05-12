import sys
import os
import random
import string
import ast #? Abstract Syntax Tree
import re
import threading
import time

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
                  -f, functions           modify functions names (only defined ones)
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
def obf_functions(code):
    print('[*] Searching for functions, all will be renamed')
    
    duration = 5
    progress_bar_thread = threading.Thread(target=progress_bar, args=(duration,))
    progress_bar_thread.start()

    used_names=set()
    name_mapping={}
    pattern = r'def\s+(\w+)\s*\('
    matches = re.findall(pattern, code)

    def random_name():
        while True:
            new_name = ''.join(random.choices(string.ascii_letters, k=10)) # Generate random names (might be changed to just strange names)
            if new_name not in used_names:
                used_names.add(new_name)
                return new_name 

    for old_name in matches:
        new_name = random_name()
        name_mapping[old_name] = new_name
        modified_functions_code = code.replace(f'def {old_name}', f'def {new_name}')

    for old_name, new_name in name_mapping.items():
        modified_functions_code = re.sub(r'\b' + re.escape(old_name) + r'\b(?=\()', new_name, modified_functions_code)

    progress_bar_thread.join()

    return modified_functions_code
def progress_bar(duration):
    start_time = time.time()
    end_time = start_time + duration
    progress_width = 50

    while time.time() < end_time:
        elapsed_time = time.time() - start_time
        progress = int((elapsed_time / duration) * progress_width)

        sys.stdout.write("\r[{}] {:.2f}%".format("=" * progress + " " * (progress_width - progress), (elapsed_time / duration) * 100))
        sys.stdout.flush()

        time.sleep(0.1)
    sys.stdout.write("\r[{}] {:.2f}%".format("=" * progress + " " * (progress_width - progress), 100))
    sys.stdout.flush()
    sys.stdout.write("\n")
def obf_variables(code):
    print('[*] Searching for variables, all will be renamed (functions might be renamed as well if -f not used before)')

    duration = 3
    progress_bar_thread = threading.Thread(target=progress_bar, args=(duration,))
    progress_bar_thread.start()

    used_names=set()
    variable_mapping = {}
    functions = set()

    def random_name():
        while True:
            new_name = ''.join(random.choices(string.ascii_lowercase, k=10))
            if new_name not in used_names:
                used_names.add(new_name)
                return new_name 

    tree = ast.parse(code)
    # print(ast.dump(tree)) #? for debugging purpose

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.add(node.name)
            for arg in node.args.args:
                variable_mapping[arg.arg] = random_name()

    
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            if node.id not in variable_mapping and node.id not in functions:
                variable_mapping[node.id] = random_name()

    modified_variables_code = code
    for old_name, new_name in variable_mapping.items():
        # Replace variable names only when they are standalone words, probably can be optimized :)
        modified_variables_code = modified_variables_code.replace(' ' + old_name + ' ', ' ' + new_name + ' ')
        modified_variables_code = modified_variables_code.replace(' ' + old_name + ')', ' ' + new_name + ')')
        modified_variables_code = modified_variables_code.replace(' ' + old_name + '[', ' ' + new_name + '[')
        modified_variables_code = modified_variables_code.replace(' ' + old_name + ':', ' ' + new_name + ':')
        modified_variables_code = modified_variables_code.replace(' ' + old_name + ',', ' ' + new_name + ',')
        modified_variables_code = modified_variables_code.replace(' ' + old_name + '\n', ' ' + new_name + '\n')

        modified_variables_code = modified_variables_code.replace('(' + old_name + ')', '(' + new_name + ')')
        modified_variables_code = modified_variables_code.replace('(' + old_name + ',', '(' + new_name + ',')

        modified_variables_code = modified_variables_code.replace('\n' + old_name + ' ', '\n' + new_name + ' ')

        modified_variables_code = modified_variables_code.replace('(' + old_name + '*', '(' + new_name + '*')
        modified_variables_code = modified_variables_code.replace('(' + old_name + '+', '(' + new_name + '+')
        modified_variables_code = modified_variables_code.replace('(' + old_name + '/', '(' + new_name + '/')
        modified_variables_code = modified_variables_code.replace('(' + old_name + '-', '(' + new_name + '-')

        modified_variables_code = modified_variables_code.replace('*' + old_name + ')', '*' + new_name + ')')
        modified_variables_code = modified_variables_code.replace('*' + old_name + '*', '*' + new_name + '*')
        modified_variables_code = modified_variables_code.replace('*' + old_name + '-', '*' + new_name + '-')
        modified_variables_code = modified_variables_code.replace('*' + old_name + '/', '*' + new_name + '/')
        modified_variables_code = modified_variables_code.replace('*' + old_name + '+', '*' + new_name + '+')

        modified_variables_code = modified_variables_code.replace('-' + old_name + ')', '-' + new_name + ')')
        modified_variables_code = modified_variables_code.replace('-' + old_name + '*', '-' + new_name + '*')
        modified_variables_code = modified_variables_code.replace('-' + old_name + '-', '-' + new_name + '-')
        modified_variables_code = modified_variables_code.replace('-' + old_name + '/', '-' + new_name + '/')
        modified_variables_code = modified_variables_code.replace('-' + old_name + '+', '-' + new_name + '+')

        modified_variables_code = modified_variables_code.replace('+' + old_name + ')', '+' + new_name + ')')
        modified_variables_code = modified_variables_code.replace('+' + old_name + '*', '+' + new_name + '*')
        modified_variables_code = modified_variables_code.replace('+' + old_name + '-', '+' + new_name + '-')
        modified_variables_code = modified_variables_code.replace('+' + old_name + '/', '+' + new_name + '/')
        modified_variables_code = modified_variables_code.replace('+' + old_name + '+', '+' + new_name + '+')

        modified_variables_code = modified_variables_code.replace('/' + old_name + ')', '/' + new_name + ')')
        modified_variables_code = modified_variables_code.replace('/' + old_name + '*', '/' + new_name + '*')
        modified_variables_code = modified_variables_code.replace('/' + old_name + '-', '/' + new_name + '-')
        modified_variables_code = modified_variables_code.replace('/' + old_name + '/', '/' + new_name + '/')
        modified_variables_code = modified_variables_code.replace('/' + old_name + '+', '/' + new_name + '+')
        

    progress_bar_thread.join()

    return modified_variables_code

if __name__ == '__main__':
    args = sys.argv[1:]

    if '-h' in args:
        help()
        exit()

    
    if '-c' in args: 
        index_code = args.index('-c')
        if index_code + 1 < len(args):
            original_name = args[index_code + 1]
            file_name, file_extension = original_name.rsplit('.', 1)
            if file_extension != 'py':
                print('[!] The obfuscation only works with python scripts for now')
                print('[*] Pass a .py script as an argument after -c')
                exit()
            if os.path.exists(original_name):
                print('[*] File found in the directory')
                with open(original_name, 'r') as original:
                    modified_code=original.read()
                    print('[*] File opened correctly')
            else:
                    print("[!] The file does not exist")
                    exit()     
        else:
            print("[!] Missing a valid file name after '-c' flag")
            exit()
    else:
        print("[!] Missing '-c' flag followed by a file name.")
        exit()

    if '-a' in args or '-f' in args or '-b' in args or '-v' in args or '-e' in args:
        print("")
    else:
        print("[!] None of the flags (-a, -f, -b, -v, -e) are present.")
        exit()

    if '-f' in args:
        print('[*] Obfuscating function names')
        modified_code=obf_functions(modified_code)

    if '-v' in args:
        print('[*] Obfuscating variables names')
        modified_code=obf_variables(modified_code)

    #! Should be done only after the whole code is obfuscated 

    out = f"{file_name}.obf.{file_extension}"

    with open(out, "w") as output:
        print('[*] Saving the obfuscated code in')
        print(out)
        output.write(str(modified_code))

        

    
    