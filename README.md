# BoutiquesDescriptors
This is an open repository for Boutiques Descriptors that are under development.

Descriptors may be developed here, where members of this communicty can give feedback and see examples of issues that come up, and their solution. Additionally, best practices for the management of descriptors can be communicated here.

Requests for new features for Boutiques or Boutiques Descriptors should be made at the [boutiques github](https://github.com/boutiques/boutiques).

## Structure
```
.
+-- <TOOL_NAME>
    +-- <TOOL_VERSION>
        +-- __test__.py
        +-- executable1.json # descriptor
        +-- executable1.txt  # optional help/info
        +-- executable1
            +-- any_files
            +-- used_by
            +-- executable1_tests
        +-- executable2.json # descriptor
        +-- executable2.txt  # optional help/info
        +-- executable2
            +-- any_files
            +-- used_by
            +-- executable2_tests
```

The top-level is a list of directories representing major tool names, like `ncbi-blast`. Some tools may just have a single executable and/or no defined version, but at the very least they will get their own directory and a descriptor will be placed within. I propose naming the descriptors after what they will execute e.g. `blastx` would have its descriptor called `blastx.json`, `testerfoo.py` would get a descriptor `testerfoo.py.json`. As a convenience, having a similarly named text file that contains the help output or documentation for the particular executable element is nice, but definitely optional. 

If there are files needed to run any tests for an executable, they should go in a directory by that name, but assume that the descriptor will be copied into the same location as all the files/directories in that test folder before it is run, thus we don't want the added path structure included in the tests. For example, tests in `executable2.json` should refer to `any_files` instead of `executable2/any_files`, since when the test suite runs for `executable2.json` it'll be in a working directory like:

```
.
+-- tmp
    +-- executable2
        +-- executable2.json
        +-- any_files
        +-- used_by
        +-- executable2_tests
```

Tools cab have multiple versions with different descriptors for different versions. This format reflects this in the directory structure, currently the least-bad approach I can think of to do it.

`__test__.py` identifies a directory that should be searched for descriptors/tests by the testing tool

## Testing
Once you clone the Descriptor Repo, you can run `python test.py` from its main directory and it will search out occurrences of `__test__.py` and attempt to validate and execute tests in any descriptors it finds. The tests will be run in a temp directory with all the provided test files and the descriptor in the same spot.


