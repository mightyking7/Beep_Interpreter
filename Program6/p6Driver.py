from p5Dict import declareVar, printLabels, printVariables
from p6Exec import Executor
import sys, os, re

'''
Parses the BEEP source file, stores lables, vars,
and excutes the source code.
'''


def main(argv):
    fileL = []  # lines of file stored as entry in list

    lineNum = 1  # line number in file

    NUM_ARGS = 2  # Minimum number of args

    MAX_ARGS = 3  # Maximum number of args

    verbose = False  # Flag for -v option

    numArgs = len(argv)

    # check for correct number of arguments
    if numArgs < NUM_ARGS or numArgs > MAX_ARGS:
        print("Usage: %s <BEEP source> [-v]" % (argv[0]))

        sys.exit(1)

    # validate filename and optional command line arguments
    filename = argv[1]

    if '-v' in argv:
        verbose = True

    elif numArgs == MAX_ARGS:
        print("Usage: %s <BEEP source> [-v]" % (argv[0]))

        sys.exit(1)

    if os.path.isfile(filename) == False:
        print("Error: %s is not a file" % (filename))

        sys.exit(1)

    # compile the regular expressions
    labelRE = re.compile(r'\s*(\w+):')
    varRE = re.compile(r'^VAR\s([a-zA-Z]+)\s([a-zA-Z]+)\s"?(.*?)"?$')

    # parse the file for labels and variables

    executor = Executor()

    file = open(filename, 'r', encoding='latin-1')

    while True:

        line = file.readline()

        if line == "":
            break

        if labelRE.match(line) != None:

            labelMO = labelRE.match(line)

            label = labelMO.group(1).upper()

            if executor.labelD.get(label, None) != None:
                print("***Error: label '%s' appears on multiple lines: %d and %d" % (label, labelD[label], lineNum))

            else:
                executor.labelD[label] = lineNum

        elif varRE.match(line) != None:

            varMO = varRE.match(line)

            declareVar(varMO, executor.varTypeD, executor.varValueD)

        fileL.append(line)

        # print line and line number
        print(lineNum, line)

        lineNum += 1

    # print labels and variables
    printVariables(executor.varTypeD, executor.varValueD)

    printLabels(executor.labelD)

    # execute the source
    if verbose:
        executor.execute(fileL, verbose=True)
    else:
        executor.execute(fileL)


if __name__ == "__main__":
    main(sys.argv)
