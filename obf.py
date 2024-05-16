import sys
import os
import random
import string
import ast 
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
                  -v, variables           modify variables names (pay attention to local variables, still has some problems)
                  -b, binary              uses binary to obfuscate (deobfuscated from added code)
                  -e, hexadecimal         uses hex to obfuscate (deobfuscated from added code) 
                  -m, mask                adds random stuff to the code (if not specified uses '@@@@')
          
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
def obf_functions(code):
    print('[*] Searching for functions, all will be renamed')
    time.sleep(0.5)
    
    duration = 3
    progress_bar_thread = threading.Thread(target=progress_bar, args=(duration,))
    progress_bar_thread.daemon = True
    progress_bar_thread.start()

    used_names=set()
    name_mapping={}
    pattern = r'def\s+(\w+)\s*\('
    matches = re.findall(pattern, code)
    modified_functions_code=code

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
def obf_variables(code):
    print('[*] Searching for variables, all will be renamed (might modify comments and strings, working on it)')
    time.sleep(0.5)

    duration = 3
    progress_bar_thread = threading.Thread(target=progress_bar, args=(duration,))
    progress_bar_thread.daemon = True
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
def obf_mask(code, char):
    print(f'[*] Masking the code using {char}. ')
    time.sleep(0.5)

    if len(code) < 20000:
        duration = 3
    else:
        duration = len(code)/5500
    progress_bar_thread = threading.Thread(target=progress_bar, args=(duration,))
    progress_bar_thread.daemon = True
    progress_bar_thread.start()

    modified_code=str(code)
    for i in range (len(modified_code)):
        pos = random.randint(0, len(modified_code))
        modified_code = modified_code[:pos] + char + modified_code[pos:]


    modified_code = f"mushroomic=\"\"\"{modified_code}\"\"\"\nexec(mushroomic.replace('{char}',''))"
    progress_bar_thread.join()
    return modified_code
def obf_hexify(code):
    print('[*] Replacing your code with the hexfied version')
    time.sleep(0.5)

    duration = 3
    progress_bar_thread = threading.Thread(target=progress_bar, args=(duration,))
    progress_bar_thread.daemon = True
    progress_bar_thread.start()

    modified_code = str(code).encode('utf-8')
    modified_code_hex = modified_code.hex()
    modified_code_hex_final=f"mushroomic=\"{modified_code_hex}\"\noriginal_bytes = bytes.fromhex(mushroomic)\noriginal_string = original_bytes.decode('utf-8')\nexec(original_string)"
    
    progress_bar_thread.join()

    return modified_code_hex_final
def obf_binary(code):
    print('[*] Replacing your code with the binary version')
    time.sleep(0.5)

    duration = 3
    progress_bar_thread = threading.Thread(target=progress_bar, args=(duration,))
    progress_bar_thread.daemon = True
    progress_bar_thread.start()

    modified_code = str(code).encode('utf-8')
    modified_code_binary = ' '.join(format(x, '08b') for x in modified_code)
    modified_code_binary_final = f"mushroomic = '{modified_code_binary}'\noriginal_bytes = bytes([int(i, 2) for i in mushroomic.split()])\noriginal_string = original_bytes.decode('utf-8')\nexec(original_string)"

    progress_bar_thread.join()

    return modified_code_binary_final
def obf_total(code):

    print ('[!] Might take some time...')
    time.sleep(0.5)
    
    modified_1_code=obf_functions(code)
    modified_2_code=obf_variables(modified_1_code)
    modified_3_code=obf_hexify(modified_2_code)
    modified_4_code=obf_binary(modified_3_code)
    modified_5_code=obf_mask(modified_4_code, '@@@@')
    modified_6_code=obf_functions(modified_5_code)
    modified_7_code=obf_variables(modified_6_code)

    return modified_7_code


def main():
    args = sys.argv[1:]

    banner()
    time.sleep(0.5)
    if '-h' in args:
        time.sleep(0.5)
        help()
        time.sleep(0.5)
        exit()

    if '-c' in args: 
        index_code = args.index('-c')
        if index_code + 1 < len(args):
            original_name = args[index_code + 1]
            file_name, file_extension = original_name.rsplit('.', 1)
            if file_extension != 'py':
                print('[!] The obfuscation only works with python scripts for now')
                time.sleep(0.5)
                print('[*] Pass a .py script as an argument after -c')
                time.sleep(0.5)
                exit()
            if os.path.exists(original_name):
                print('[*] File found in the directory')
                time.sleep(0.5)
                with open(original_name, 'r') as original:
                    modified_code=original.read()
                    print('[*] File opened correctly')
                    time.sleep(0.5)
            else:
                    print("[!] The file does not exist")
                    time.sleep(0.5)
                    exit()     
        else:
            print("[!] Missing a valid file name after '-c' flag")
            time.sleep(0.5)
            exit()
    else:
        print("[!] Missing '-c' flag followed by a file name.")
        exit()

    if '-a' in args or '-f' in args or '-b' in args or '-v' in args or '-e' in args  or '-m' in args:
        print("")
    else:
        print("[!] None of the flags (-a, -f, -b, -v, -e, -m) are present.")
        exit()

    if '-a' in args:
        print('[*] Obfuscating the whole code')
        time.sleep(0.5)
        modified_code=obf_total(modified_code)
    else:
        if '-f' in args:
            print('[*] Obfuscating function names')
            time.sleep(0.5)
            modified_code=obf_functions(modified_code)

        if '-v' in args:
            print('[*] Obfuscating variables names')
            time.sleep(0.5)
            modified_code=obf_variables(modified_code)

        if '-m' in args:
            mask_char=input('[*] Enter the char you want to use for the masking, if not entered will use @ (will be multipled by 4): ')
            time.sleep(0.5)
            if mask_char == '':
                mask_char='@@@@'
            else:
                mask_char+=mask_char+mask_char+mask_char
                
            print('[*] Masking the code')
            time.sleep(0.5)
            modified_code=obf_mask(modified_code, mask_char)

        if '-e' in args:
            print('[*] Hexifying the code')
            time.sleep(0.5)
            modified_code=obf_hexify(modified_code)
        
        if '-b' in args:
            print('[*] Obfuscating with binary')
            time.sleep(0.5)
            modified_code = obf_binary(modified_code)

    out = f"{file_name}.obf.{file_extension}"

    with open(out, "w") as output:
        print('[*] Saving the obfuscated code in')
        time.sleep(0.5)
        print(out)
        time.sleep(0.5)
        output.write(str(modified_code))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('[!] KeyboardInterrupt, exiting...')
        time.sleep(0.5)
        exit()
        

    
    