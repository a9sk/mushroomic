# Mushroomic

Command Line Tool for the obfuscation of python code.

## Installation

To install Mushroomic, follow this steps:

1. Clone this repository on your machine: 
   ```bash
   git clone https://github.com/a9sk/mushroomic
   ```
2. Change directory into the one you just downloaded:
   ```bash
   cd mushroomic
   ```
3. Run the obf.py script:
   ```bash
   python3 obf.py -c [file to obfuscate] [-a, -f, -v, -m, -e, -b, -h]
   ```

## Usage

    Usage: python3 obf.py -c [file to obfuscate] [flags]

          Required:
                  -c, code                pass the whole path or name of the code you want to obfuscate
  
          Obfuscation:
                  -a, all                 uses all of the tecniques implemented
                  -f, functions           modify functions names (only defined ones)
                  -v, variables           modify variables names (pay attention to comments and output strings)
                  -b, binary              uses binary to obfuscate (deobfuscated from added code)
                  -e, hexadecimal         uses hex to obfuscate (deobfuscated from added code) 
                  -m, mask                adds random chars to the code (if not specified uses '@@@@')
          
          Miscellaneous:
                  -h, --h*                 display help and exit 

                  
## Licence

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).

## Contacts

To report bugs, request new features, or ask questions, contact the project author:

- Email: 920a9sk765@proton.me
- GitHub: [@a9sk](https://github.com/a9sk)