from p5Dict import declareVar, printLabels, printVariables
from Executor import Executor
import sys, os, re


'''                                                                      
     Purpose:                                                            
        Parses the BEEP source file to stores labels and variables.
        Creates an executor to execute the source code and
        prints the variables and labels parsed from the file.                                    

    Parameters:                                                          
        argv  -  Command line arguments

    Notes:                                                                            
        Main must be called with the following arguments:
        p6Driver.py <BEEP source> [-v]
                       
    Return:                                                              
'''

def main(argv):

    varTypeD  = {}  # dictionary for variable types

    varValueD = {}  # dictionary for variable values

    labelD    = {}  # dictionary for labels

    source = []     # source code

    lineNum = 1     # file line number

    NUM_ARGS = 2    # Minimum number of args

    MAX_ARGS = 3    # Maximum number of args

    verbose = False # Flag for -v option

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
    varRE = re.compile(r'^VAR\s([\w]+)\s([\w]+)\s"?(.*?)"?$')

    # parse file for labels and variables and print contents

    file = open(filename, "r", encoding='latin-1')

    print('BEEP source code in %s:' %(filename))

    while True:

        line = file.readline()

        if line == "":
            break

        if labelRE.match(line) != None:

            labelMO = labelRE.match(line)

            label = labelMO.group(1).upper()

            if labelD.get(label, None) != None:
                print("***Error: label '%s' appears on multiple lines: %d and %d" % (label, labelD[label], lineNum))

            else:
                labelD[label] = lineNum

        elif varRE.match(line) != None:

            varMO = varRE.match(line)

            declareVar(varMO, varTypeD, varValueD)

        source.append(line)

        # print line and line number
        print("%d. %s" %(lineNum, line))

        lineNum += 1

    # print labels and variables
    printVariables(varTypeD, varValueD)

    printLabels(labelD)

    executor = Executor(varTypeD, varValueD, labelD, source)

    # execute the source
    if verbose:
        executor.execute(source, verbose=True)

    else:
        executor.execute(source)


if __name__ == "__main__":
    main(sys.argv)
