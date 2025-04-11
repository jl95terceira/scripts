import json
import subprocess
import sys

if __name__ == '__main__':

    cmd = sys.argv[1:]
    out = subprocess.run(cmd,shell=True,capture_output=True).stdout.decode()
    print(json.dumps(json.loads(out), indent=2))
