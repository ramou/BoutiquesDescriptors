from boutiques import bosh
import glob
import fnmatch
import sys
import os
import tempfile
import traceback
from shutil import copyfile, rmtree, copytree

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
    dir = os.path.realpath(os.path.dirname(target))
    newtar = os.path.join(dir,"*.json")
    print("\033[94mProcessing Tools in " + dir + " \033[0m")
    successful = 0
    tried = 0;
    for f in glob.iglob(newtar):
        tried += 1
        try:
            testTools(f)
            successful += 1
            print("\t\033[92mSuccess on " + f + " \033[0m")
        except:
            print("\t\033[91mError on " + f + " \033[0m")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("".join(traceback.format_exception(exc_type, exc_value,
                                                     exc_traceback)))

    print("\033[94m"+str(successful)+" of " +str(tried)+" tools successfully validated/tested against bosh in " + dir + " \033[0m")

if sys.version_info >= (3, 4):
    for f in glob.iglob('**/__test__.py', recursive=True):
        processTools(f)
else:
    for root, dirnames, filenames in os.walk('.'):
        for f in fnmatch.filter(filenames, '__test__.py'):
            processTools(os.path.join(root, f))

