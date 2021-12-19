import os
import sys

def fail(msg:str, exitCode=0):
    COLOR_FAIL = '\033[91m'
    print('', file=sys.stderr)
    print(f"{COLOR_FAIL}FAIL: {msg}", file=sys.stderr)
    print('', file=sys.stderr)
    exit(exitCode)

if __name__=="__main__":
    daysDir = sys.argv[1]
    file = sys.argv[2]

    print(daysDir, file)
    if not file.startswith(daysDir):
        fail(f"Current file \"{file}\" is not inside \"{daysDir}\"")

    relFile = file[len(daysDir):].lstrip(os.path.sep)
    pathElems = relFile.partition(os.path.sep)

    if len(pathElems) > 1:
        # File is in a "day" subdir
        day = pathElems[0]
        moduleDir = os.path.join(daysDir, day)
        moduleName = day

    else:
        # File is directly inside `srcDir` and not in a "day" subdir
        if not relFile.endswith('.py'):
            fail("Current file is not a python file (has no \".py\" extension)")

        moduleDir = daysDir
        moduleName = os.path.splitext(relFile)[0]

    os.chdir(moduleDir)

    import runpy
    sys.path.append(moduleDir)
    runpy.run_module(moduleName, run_name='__main__')
