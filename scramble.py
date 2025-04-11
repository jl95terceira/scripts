import argparse
import mmap
import operator
import os
import os.path
import random
import re
import shutil
import subprocess
import time
import typing
import uuid

FILENAME_MARKER         = 'da92c675-0e87-4073-9d02-c02afbece032'
FILENAME_MARKER_ENCODED = FILENAME_MARKER.encode()

class Scrambler:

    def __init__(self, key):

        self._key = key
        self._rng = random.Random()

    def _scramble(self, bb:bytes,op:typing.Callable[[int,int],int]):

        self._rng.seed(self._key)
        return bytes(op(b,self._rng.randint(0,256)) % 256 for b in bb)

    def scramble  (self, bb:bytes): return self._scramble(bb, operator.add)
    def unscramble(self, bb:bytes): return self._scramble(bb, operator.sub)

if __name__ == '__main__':

    p = argparse.ArgumentParser()
    class A:
        KEY       ='key'
        FILE_PATH ='file'
        UNSCRAMBLE='u'
        OPEN      ='o'
    p.add_argument(f'{A.KEY}')
    p.add_argument(f'{A.FILE_PATH}')
    p.add_argument(f'--{A.UNSCRAMBLE}', action='store_true')
    p.add_argument(f'--{A.OPEN}',       action='store_true')
    get = p.parse_args().__getattribute__
    # parse
    key       :str  = get(A.KEY)
    file_path :str  = get(A.FILE_PATH)
    unscramble:bool = get(A.UNSCRAMBLE)
    open_     :bool = get(A.OPEN)
    # do it
    file_dir,file_name_encoded = os.path.split(file_path)
    s = Scrambler(key)
    if open_ or unscramble:

        with open(file_path, mode='rb') as fr:

            content = fr.read()
            x = re.search(pattern=f'^(.*){FILENAME_MARKER}'.encode(), string=content)
            file_name_encoded = x.group(1)
            assert isinstance(file_name_encoded, bytes)
            file_stem,file_ext = os.path.splitext(file_name_encoded.decode())
            print(file_name_encoded)
            fr.seek(len(file_name_encoded)+len(FILENAME_MARKER_ENCODED))
            def write_unscrambled(fn:str):

                with open(fn, mode='wb') as fw:

                    fw.write(s.unscramble(fr.read()))

            fileout_name = f'{file_stem}_UNSCRAMBLED{file_ext}'
            if not open_:

                write_unscrambled(fileout_name)

            else:

                try:
                    write_unscrambled(fileout_name)
                    subprocess.run([fileout_name,],shell=True)
                    time.sleep(5)
                finally:
                    try:
                        while True:
                            os.remove(fileout_name)
                            break
                    except: pass

    else: 
        
        scrambled_file_name = str(uuid.uuid4())
        with open(file_path, mode='rb') as fr: 
            
            with open(os.path.join(file_dir, scrambled_file_name), mode='wb') as fw:

                fw.write(file_name_encoded.encode())
                fw.write(FILENAME_MARKER_ENCODED)
                fw.write(s.scramble(fr.read()))
