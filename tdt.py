import os.path
import subprocess
import sys

TRIP_DEVTOOLS_PATH = r'C:\Users\João\source\repos-cliente-efacec\trip-devtools'

if __name__ == '__main__':

    aa = iter(sys.argv[1:])
    tool_path = os.path.join(TRIP_DEVTOOLS_PATH, next(aa))
    print(tool_path)
    subprocess.run([tool_path, *aa], shell=True)
