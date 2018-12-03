'''
    Purpose:
        tores a variable's value and type in a dictionary

    Parameters:
        tokenM    - Match object that contains a variable's
                    type, name, and value.
        varTypeD  -  Dictionary with mapping of var name to data type
        varValueD -  Dictionary with mapping of var name to value

    Return:
        Void
'''


def declareVar(tokenMO, varTypeD, varValueD):
    varType = tokenMO.group(1).upper()

    varName = tokenMO.group(2).upper()

    varValue = tokenMO.group(3)

    varTypeD[varName] = varType

    if varType == 'INT':
        varValueD[varName] = int(varValue)

    else:
        varValueD[varName] = varValue




'''
    Purpose: 
        Prints the type and value of variable in the BEEP source code. 

    Parameters:
        varTypeD  -  Dictionary with mapping of var name to data type
        varValueD -  Dictionary with mapping of var name to value

    Notes:
        Sorts keys in the varTypeD and varValueD dictionaries
        in ascending order.

    Return:
        Void
'''


def printVariables(varTypeD, varValueD):
    print("Variables:")

    print("%12s %8s %8s" % ("Variable", "Type", "Value"))

    for name in sorted(varTypeD):
        print("    %-10s   %-8s %-8s" % (name, varTypeD[name], varValueD[name]))


'''
    Purpose: 
        Prints the name and line number of a label in the BEEP source code. 

    Parameters:
        labelD  -  Dictionary with mapping of label name to line number

    Notes:
        Sorts keys in the labelD dictionary in ascending order.

    Return:
        Void
'''


def printLabels(labelD):
    print("Labels:")

    print("%9s %16s" % ("Label", "Statement"))

    for name in sorted(labelD):
        print("    %-10s   %-8s" % (name, labelD[name]))

