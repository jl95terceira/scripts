import json
import sys

if __name__ == '__main__':

    fn = sys.argv[1]
    print(json.dumps(json.load(open(fn, mode='r'))))