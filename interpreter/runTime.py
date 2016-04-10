symbolTableStack = []
functionExecutionValueStack = []
functionReturnAddressStack = []

def read_program():
    program = []
    i=0
    try:
        #'recursive.am'

        with open('local_global.am') as f:
            for line in f:
                line = line.strip()
                program.append(line)
                i = i + 1
    except IOError as e:
        print "I/O error -", e.strerror
        exit(-1)
    return program

def display_program(data):
    if type(data) is list:
        for line in data:
            print line
    elif type(data) is dict:
        for key, val in data.items():
            print key, '->', val
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
    line = 0
    whichTable = 'global'
    nestedLevel = 0
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

        elif contents[0] == 'FCAL':
            funcSymbolTable = {}
            funcName = contents[1]
            line = line + 1
            find = None
            sub = False
            contents = program[line].split(' ')
            while line < noOfLines and contents[0] == "PUSH":
                if contents[1] == "DEC1":
                    find = contents[2]
                    sub = True
                else:
                    find = contents[1]
                noOfParameters += 1
                if find not in symbolTableStack[-1]:
                    print 'ERROR: variable ',contents[1], 'is not defined'
                    exit(-1)
                funcSymbolTable[find] = symbolTableStack[-1][find]
                if(sub):
                    funcSymbolTable[find] -= 1
                line += 1
                contents = program[line].split(' ')
            functionReturnAddressStack.append(line)
            symbolTableStack.append(funcSymbolTable)
            line = symbolTableStack[0][funcName]
            line = line -1

        elif contents[0] == 'ISTR':
            ifExecuted = False
            found = False
            line += 1
            contents = program[line].split(' ')
            if contents[0] == 'CEQL':
                for i in range(len(symbolTableStack)-1, -1, -1):
                    if contents[1] in symbolTableStack[i]:
                        found = True
                        result = compare_values(symbolTableStack[i][contents[1]], contents[2])
                        break;
                if not found:
                    print "ERROR: variable", contents[1], 'is not defined'
                    exit(-1)

                if result != 0:
                    while not program[line].startswith('SEND'):
                        line += 1
                    while program[line].startswith('SEND'):
                        line += 1
                    line -= 1
                else:
                    ifExecuted = True
                    ifSymbolTable = {}
                    symbolTableStack.append(ifSymbolTable)

        elif contents[0] == 'IEND':
            symbolTableStack.pop()

        elif contents[0] == 'SEND':
            val = None
            try:
                val = int (contents[1])
            except:
                val = look_up(contents[1])
            symbolTableStack.pop()
            symbolTableStack.append(val)
            line = functionReturnAddressStack[-1]
            functionReturnAddressStack.pop()
            line = line -1

        elif contents[0] == 'LOAD': # for return value only
            val = symbolTableStack[-1]
            val = int(val)
            #print 'val: ',val
            symbolTableStack.pop()
            symbolTableStack[-1][contents[1]] = val

        elif contents[0] == 'MULT':
            n1 = look_up(contents[2])
            n2 = look_up(contents[3])
            v = n1 * n2
            symbolTableStack[-1][contents[1]] = v

        elif contents[0] == 'PRNT':
            val = look_up(contents[1])
            print val
        elif contents[0] == 'FEND':
            symbolTableStack.pop()
            line = functionReturnAddressStack[-1]
            line -= 1
        line += 1


if __name__ == "__main__":
    program = read_program()
    #display_program(program)
    execute_program(program)
    #display_program(symbolTableStack)
