import re, sys
from p5Dict import printVariables

'''
Responsible for executing BEEP source code,
storing runtime variables, tokens, and values
'''


class Executor:

    EXECUTION_LIMIT = 5000

    '''
    Constructor for Executor
    '''

    def __init__(self):

        self.varTypeD = {}  # dictionary for var data type

        self.varValueD = {}  # dictionary for var value

        self.labelD = {}  # dictionary for labels

        self.source = []  # list of source code to execute

        self.lineNum = 1  # current line being executed

        self.execCount = 0  # count of lines executed

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

    def execute(self, fileList, verbose=False):

        printRE = re.compile(r'\s*[\w:]*\s*PRINT\s(.*)$')
        gotoRE = re.compile(r'\s*[\w:]*\s*GOTO\s(\w+)$')
        assignRE = re.compile(r'\s*ASSIGN\s(\w+)\s([+*\-&>=]+)?\s?(\w+)?\s?(\w+)?$')
        ifRE = re.compile(r'\s*([\w\W]*)[Ii][fF]\s(([><=]+)\s(\w+)\s(\w+))\s(\w+)$')

        #TODO Fix nasty code
        self.source = fileList

        print("execution begins ...")

        while self.lineNum <= len(self.source):

            line = self.source[self.lineNum - 1]

            if self.execCount == Executor.EXECUTION_LIMIT:
                print("Infinite loop most likely encountered")

                sys.exit(1)

            if assignRE.match(line) != None:

                assignMO = assignRE.match(line)

                varName = assignMO.group(1).upper()

                op = assignMO.group(2)

                val1 = assignMO.group(3).upper()

                val2 = assignMO.group(4).upper()

                try:
                    self.assignVar(varName, op, val1, val2)
                except(InvalidValueType, TooFewOperands, InvalidExpression, VarNotDefined) as e:
                    print("*** line %d error detected ***" % (self.lineNum))
                    print("%-10s %d *** %s ***" % (" ", self.lineNum, str(e.args[0])))
                    break

                except Exception as e:
                    print("*** line %d error detected ***" % (self.lineNum))
                    print("%-10s %d *** %s ***" % (" ", self.lineNum, str(e.args[0])))
                    break

            elif printRE.match(line) != None:

                printMO = printRE.match(line)

                args = printMO.group(1).split()

                try:
                    self.bPrint(args)

                except(VarNotDefined) as e:
                    print("*** line %d error detected ***" % (self.lineNum))
                    print("%-10s %d *** %s ***" % (" ", self.lineNum, str(e.args[0])))
                    break


            elif gotoRE.match(line) != None:

                gotoMO = gotoRE.match(line)

                label = gotoMO.group(1).upper()

                try:
                    self.goto(label)

                    continue

                except(LabelNotDefined) as e:
                    print("*** line %d error detected ***" % (self.lineNum))
                    print("%-10s %d *** %s ***" % (" ", self.lineNum, str(e.args[0])))
                    break

            elif ifRE.match(line) != None:

                ifMO = ifRE.match(line)

                op = ifMO.group(3)

                op1 = ifMO.group(4).upper()

                op2 = ifMO.group(5).upper()

                label = ifMO.group(6).upper()

                try:
                    self.evalIf(op, op1, op2, label)

                except(InvalidExpression) as e:
                    print("*** line %d error detected ***" % (self.lineNum))
                    print("%-10s %d *** %s ***" % (" ", self.lineNum, str(e.args[0])))
                    break

                except(LabelNotDefined) as e:
                    print("*** line %d error detected ***" % (self.lineNum))
                    print("%-10s %d *** %s ***" % (" ", self.lineNum, str(e.args[0])))
                    break

                except Exception as e:
                    print("*** line %d error detected ***" % (self.lineNum))
                    print("%-10s %d *** %s ***" % (" ", self.lineNum, str(e.args[0])))
                    break

            self.execCount += 1

            self.lineNum += 1

        print("execution ends, %d lines executed" % (self.execCount))

        printVariables(self.varTypeD, self.varValueD)

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

    def assignVar(self, varName, op, var1, var2):

        varRE = re.compile(r'"(.*)"|^\d+$')

        # expression is a varLiteral
        if op == None and var1 != None and var2 == None:

            # verify varName is declared
            if self.varValueD.get(varName, None) == None:
                raise VarNotDefined("%s is not defined" % (varName))

            # obtain the value of the varLiteral
            val1 = self.evalVar(var1)

            if val1 != None:
                self.varValueD[varName] = val1

            # var1 is not a string or int constant or declared variable
            else:
                raise VarNotDefined("%s is not defined" % (var1))

        # expression has an operator
        else:

            if op == '*':
                try:
                    self.varValueD[varName] = self.replicate(var1, var2)

                except(TooFewOperands) as e:
                    raise e


            elif op == '+':
                self.varValueD[varName] = self.varValueD[var1] + int(var2)

            elif op == '-':
                self.varValueD[varName] = self.varValueD[var1] - var2

            elif op == '>':

                try:
                    self.varValueD[varName] = self.evalGreater(var1, var2)

                except(InvalidValueType) as e:
                    raise e

            elif op == '>=':

                try:
                    self.varValueD[varName] = self.evalGreater(var1, var2, True)

                except(InvalidValueType) as e:
                    raise e

            elif op == '&':

                try:
                    self.varValueD[varName] = self.concat(var1, var2)

                except(TooFewOperands) as e:
                    print("*** line %d error detected ***" % (self.lineNum))
                    print("%-10s %d *** %s ***" % (" ", self.lineNum, str(e.args[1])))
                    raise e

            else:
                raise InvalidExpression("%s is not a valid operator" % (op))

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

    def replicate(self, var1, var2):

        val1 = self.evalVar(var1)

        val2 = self.evalVar(var2)

        if val1 != None and val2 != None:
            return val1 * int(val2)

        else:
            raise TooFewOperands("Replication operation expects two operands")

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

    def evalGreater(self, var1, var2, equal=False):

        try:
            iVal1 = int(var1)
        except:
            raise InvalidValueType("'%s' is not numeric" % (var1))
        try:
            iVal2 = int(var2)
        except:
            raise InvalidValueType("'%s' is not numeric" % (var2))

        return iVal1 > iVal2 if not equal else iVal1 >= iVal2

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

    def evalLess(self, var1, var2, equal=False):

        try:
            iVal1 = int(var1)
        except:
            raise InvalidValueType("'%s' is not numeric" % (var1))
        try:
            iVal2 = int(var2)
        except:
            raise InvalidValueType("'%s' is not numeric" % (var2))

        return iVal1 < iVal2 if not equal else iVal1 <= iVal2

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

    def concat(self, var1, var2):

        val1 = self.evalVar(var1)
        val2 = self.evalVar(var2)

        if val1 != None and val2 != None:
            return val1 + val2

        else:
            raise TooFewOperands("Concatenation operation expects two operands")

    '''
         Purpose: 
            Evaluates the expression of an if statement.
            If the expression is true, branch to the specified
            label, otherwise continue. 
    
        Parameters:
            op  -  Operator used for comparison. Can be one of >, >=, <, <=
            op1 -  First Operand
            op2 -  Second Operand
            label - Label to branch to if expression is true
    
        Notes:
            expression has the form:
                op op1 op2
                
            example: >= tick count
            
            true if value of tick greater than or equal to count 
    
        Return:
            Void
    '''

    def evalIf(self, op, op1, op2, label):

        val1 = self.evalVar(op1)
        val2 = self.evalVar(op2)

        try:

            if op == '>' and self.evalGreater(val1, val2):
                self.goto(label)

            elif op == '>=' and self.evalGreater(val1, val2, True):
                self.goto(label)

            elif op == '<' and self.evalLess(val1, val2):
                self.goto(label)

            elif op == '<=' and self.evalLess(val1, val2, True):
                self.goto(label)

        except (InvalidExpression, LabelNotDefined, Exception) as e:
            raise e

    '''
        Evaluates the value of var, whether a variable
        numeric constant or string constant and returns the
        value. If var  None is returned.
    '''

    def evalVar(self, var):

        stringRE = re.compile(r'"(.*)"')
        intRE = re.compile(r'^\d+$')

        # check if varLiteral is a variable
        if self.varValueD.get(var, None) != None:
            return self.varValueD[var]

        # Var Literal is String
        elif stringRE.match(var) != None:
            return stringRE.match(var).group()

        # Var Literal is an Int
        elif intRE.match(var) != None:
            return intRE.match(var).group()

        else:
            return None

    '''
    Sets the BEEP source line to execute
    '''
    def goto(self, label):

        if self.labelD.get(label, None) == None:
            raise LabelNotDefined("Label %s is not defined" %(label))

        else:
            self.lineNum = self.labelD.get(label, None)

    '''
    
    '''
    def bPrint(self, args):

        # iterate over arguments to print
        for arg in args:

            if re.search('"', arg):
                val = self.evalVar(arg)

            else:
                val = self.evalVar(arg.upper())

            # value is not a string const, numeric const, or variable
            if val == None:
                raise InvalidValueType("%s is not a variable, numeric constant, or string constant" % (arg))

            print(val, end=" ")

        print("")



'''
Custom Exception classes
'''


class TooFewOperands(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class VarNotDefined(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class LabelNotDefined(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class InvalidExpression(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class InvalidValueType(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
