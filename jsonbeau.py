import argparse
import json
import subprocess
import sys

def do_it(args      :str|list[str],
          is_command:bool,
          indent    :int|None):
    
    if isinstance(args,str):

        args = [args,]

    if not is_command:

        out=args[0]

    else:

        out = subprocess.run(args,shell=True,capture_output=True).stdout.decode()

    print(json.dumps(json.loads(out), indent=indent))

def main_maker(indent:int|None=2):

    def main():

        class A:
            ARGS    = 'args'
            COMMAND = 'c'
        ap = argparse.ArgumentParser(description='JSON beautifier for literals and command outputs')
        ap.add_argument(f'--{A.COMMAND}', 
                        help='interpret argument(s) as a command',
                        action='store_true')
        ap.add_argument(f'{A.ARGS}', 
                        help='arguments - JSON literal or command token(s)',
                        nargs='+')
        get = ap.parse_args().__getattribute__
        do_it(args      =get(A.ARGS),
              is_command=get(A.COMMAND),
              indent=indent)
    
    return main

def main():
    main_maker()()

if __name__ == '__main__': main()
