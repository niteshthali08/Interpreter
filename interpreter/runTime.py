symbolTableStack = []
functionExecutionValueStack = []
functionReturnAddressStack = []
debug = 0
def read_program():
    debug = 1;
    program = []
    i=0
    try:
        #'recursive.am'
        with open('fibonaci.am') as f:
            for line in f:
                line = line.strip()
                program.append(line)
                i = i + 1
    except IOError as e:
        print "I/O error -", e.strerror
        exit(-1)
    return program

def consol_log(data):
    if debug:
        print data
def compare_values(val1, val2):
    try:
        val1 = int(val1)
        val2 = int(val2)
        if val1 > val2:
            return 1
        elif val1 < val2:
            return -1
        else:
            return 0
    except :
        print "ERROR: Found Boolean data type"
        # write code to handle booleans
def look_up(key):
    found = False
    try:
        for i in range(len(symbolTableStack)-1, -1, -1):
            if key in symbolTableStack[i]:
                    found = True
                    value = symbolTableStack[i][key]
                    return int(value)
        if not found:
            print "ERROR: variable", key, 'is not defined'
            exit(-1)
    except:
        print "ERROR: variable", key, 'is not defined'
        exit(-1)


def execute_program(program):
    symbolTableStack.append({}) # global symbol table
    symbolTableStack[0]['type'] = 'GLOBAL'
    line = 0
    noOfLines = len(program)
    noOfParameters = 0
    while line < noOfLines:
        contents = program[line].split(' ')
        if (contents[0] == 'FSTR'):
            symbolTableStack[-1][contents[1]] = line+1
            line  = line + 1
            while(line < noOfLines and not program[line].startswith('FEND')):
                line = line + 1

        elif contents[0] == 'MOVE': #when assigning
            symbolTableStack[-1][contents[1]] = int(contents[2])
            consol_log(symbolTableStack)

        elif contents[0] == 'FCAL':
            funcSymbolTable = {}
            funcSymbolTable['type'] = 'FUNCTION'
            funcName = contents[1]
            line = line + 1
            find = None
            sub1= False
            sub2 = False
            contents = program[line].split(' ')
            while line < noOfLines and contents[0] == "PUSH":
                if contents[1] == 'DEC1':
                    find = contents[2]
                    sub1 = True
                elif contents[1] == 'DEC2':
                    find = contents[2]
                    sub2 = True
                else:
                    find = contents[1]
                noOfParameters += 1

                funcSymbolTable[find] = look_up(find)
                if(sub1):
                    funcSymbolTable[find] -= 1
                elif (sub2):
                    funcSymbolTable[find] -= 2
                line += 1
                contents = program[line].split(' ')
            functionReturnAddressStack.append(line)
            symbolTableStack.append(funcSymbolTable)
            line = symbolTableStack[0][funcName]
            line = line -1
            consol_log(symbolTableStack)

        elif contents[0] == 'ISTR':
            ifSymbolTable = {}
            ifSymbolTable['type'] = 'IF'
            ifSymbolTable['ifExecuted'] = False
            symbolTableStack.append(ifSymbolTable)
            consol_log(symbolTableStack)

        elif contents[0] == 'CEQL':
            found = False
            result = None
            for i in range(len(symbolTableStack)-1, -1, -1):
                if contents[1] in symbolTableStack[i]:
                    found = True
                    result = compare_values(symbolTableStack[i][contents[1]], contents[2])
                    break;

            if not found:
                print "ERROR: variable", contents[1], 'is not defined'
                exit(-1)

            if result != 0:
                while not program[line].startswith('IEND'):
                    line += 1
                line -= 1
            else:
                symbolTableStack[-1]['ifExecuted'] = True

        elif contents[0] == 'IEND':
            symbolTableStack.pop()
            consol_log(symbolTableStack)

        elif contents[0] == 'SEND':
            val = None
            try:
                val = int (contents[1])
            except:
                val = look_up(contents[1])
            index = len(symbolTableStack) - 1;
            while (symbolTableStack[index]['type'] != 'FUNCTION'):
                symbolTableStack.pop()
                index -= 1
            if index >=0 and symbolTableStack[index]['type'] == 'FUNCTION':
                line = functionReturnAddressStack[-1]
                functionReturnAddressStack.pop()
                symbolTableStack.pop()
                line = line -1
                symbolTableStack.append(val)
            else:
                print "ERROR: Illegal return statement in the scope"
            consol_log(symbolTableStack)
        elif contents[0] == 'LOAD': # for return value only
            val = symbolTableStack[-1]
            val = int(val)
            #print 'val: ',val
            symbolTableStack.pop()
            symbolTableStack[-1][contents[1]] = val
            consol_log(symbolTableStack)

        elif contents[0] == 'MULT':
            n1 = look_up(contents[2])
            n2 = look_up(contents[3])
            v = n1 * n2
            symbolTableStack[-1][contents[1]] = v
            consol_log(symbolTableStack)
        elif contents[0] == 'PRNT':
            val = look_up(contents[1])
            print val
        elif contents[0] == 'FEND':
            symbolTableStack.pop()
            line = functionReturnAddressStack[-1]
            line -= 1
            consol_log(symbolTableStack)
        elif contents[0] == 'ADD':
            n1 = look_up(contents[2])
            n2 = look_up(contents[3])
            v = n1 + n2
            symbolTableStack[-1][contents[1]] = v
            consol_log(symbolTableStack)
        line += 1


if __name__ == "__main__":
    program = read_program()
    consol_log(program)
    execute_program(program)
    consol_log(symbolTableStack)
