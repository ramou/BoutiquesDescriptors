from boutiques import bosh
import glob
import fnmatch
import sys
import os
import tempfile
import traceback
from shutil import copyfile, rmtree, copytree

log = ""
def testTools(target):
    path, file = os.path.split(target)
    tool = file[0:-5]
    tmp = tempfile.mkdtemp()
    toolTestSrc = os.path.join(path, tool)
    toolTestDes = os.path.join(tmp, tool)
    old_wd = os.getcwd()
    try:
        if os.path.isdir(toolTestSrc):
            copytree(toolTestSrc, toolTestDes)
        else:
            os.mkdir(toolTestDes)
        copyfile(target, os.path.join(toolTestDes, file))
        os.chdir(toolTestDes)
        bosh(["validate", os.path.join(toolTestDes, file)])
        bosh(["test", os.path.join(toolTestDes, file)])
    finally:
        os.chdir(old_wd)
        rmtree(tmp)

def processTools(target):
    global log
    dir = os.path.realpath(os.path.dirname(target))
    newtar = os.path.join(dir,"*.json")
    message = "\033[94mProcessing Tools in " + dir + " \033[0m"
    print(message)
    log = log+"\n"+message
    successful = 0
    tried = 0;
    for f in glob.iglob(newtar):
        tried += 1
        try:
            testTools(f)
            successful += 1
            message="\t\033[92mSuccess on \t" + f + " \033[0m"
        except:
            message="\t\033[91mError on \t" + f + " \033[0m"
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("".join(traceback.format_exception(exc_type, exc_value,
                                                     exc_traceback)))
        print(message)
        log = log+"\n"+message
    message = "\033[94m"+str(successful)+" of " +str(tried)+" tools successfully validated/tested against bosh in " + dir + " \033[0m\n"
    print(message)
    log = log+"\n"+message
    return tried!=successful

failing = False

if sys.version_info >= (3, 4):
    for f in glob.iglob('**/__test__.py', recursive=True):
        failing |= processTools(f)
else:
    for root, dirnames, filenames in os.walk('.'):
        for f in fnmatch.filter(filenames, '__test__.py'):
            failing |= processTools(os.path.join(root, f))
print("")
print("\033[94mFinal Results:\033[0m")
print(log)
if failing:
    sys.exit(1)
