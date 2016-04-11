symbolTableStack = []
functionExecutionValueStack = []
functionReturnAddressStack = []
debug = 0
def read_program():
    debug = 1;
    program = []
    i=0
    try:
        #'factorial.am'
        # fibonaci.am
        # while_loop.am
        # local_global.am
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
    try:
        key = int(key)
        return key
    except:
        for i in range(len(symbolTableStack)-1, -1, -1):
            if key in symbolTableStack[i]:
                    value = symbolTableStack[i][key]
                    return int(value)

        report_error(key)

def get_end_of_block():
    search = None
    if symbolTableStack[-1]['type'] == 'IF':
        search = 'IEND'
    elif symbolTableStack[-1]['type'] == 'WHILE':
        search = 'WEND'
    else:
        report_error(None)
    return search

def report_error(var):
    if var == None:
        print "ERROR: syntax error in the program"
    else:
        print "ERROR: variable", var, 'is not defined'
    exit(-1)

def get_comparision_result(v1, v2):
    v1 = look_up(v1)
    v2 = look_up(v2)
    result = compare_values(v1, v2)
    return result

def update_symbol_table(key, val):
    try:
        for i in range(len(symbolTableStack) - 1, -1, -1):
            if key in symbolTableStack[i]:
                symbolTableStack[i][key] = val
                return
        report_error(key)
    except:
        print 'Exception in look up function'

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

        elif contents[0] == 'ISTR' or contents[0] == 'WSTR':
            symTable = {}
            if contents[0] == 'ISTR':
                symTable['type'] = 'IF'
                symTable['ifExecuted'] = False
            else:
                symTable['type'] = 'WHILE'
                symTable['start_loop'] = line  #loop start
            symbolTableStack.append(symTable)
            consol_log(symbolTableStack)

        elif contents[0] == 'CEQL' or contents[0] == 'CLES' or contents[0] == 'CGTR':
            result = get_comparision_result(contents[1], contents[2])
            search = get_end_of_block()
            if (result == 0 and contents[0] == 'CEQL') or (result == 1 and contents[0] == 'CGTR') or (result == -1 and contents[0] == 'CLES'):
                if symbolTableStack[-1]['type'] == 'IF':
                    symbolTableStack[-1]['ifExecuted'] = True
            else:
                while not program[line].startswith(search):
                    if (search == 'WEND'):
                        symbolTableStack[-1]['exit_loop'] = True
                    line += 1
                line -= 1

        elif contents[0] == 'IEND':
            symbolTableStack.pop()
            consol_log(symbolTableStack)
        elif contents[0] == 'WEND':
            if 'exit_loop' not in symbolTableStack[-1]:
                line = symbolTableStack[-1]['start_loop']
            else:
                symbolTableStack.pop()
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
            update_symbol_table(contents[1], v)
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
            update_symbol_table(contents[1], v)
            consol_log(symbolTableStack)
        elif contents[0] == 'SUB':
            n1 = look_up(contents[2])
            n2 = look_up(contents[3])
            v = n1 - n2
            update_symbol_table(contents[1], v)
            consol_log(symbolTableStack)

        line += 1


if __name__ == "__main__":
    program = read_program()
    consol_log(program)
    execute_program(program)
    consol_log(symbolTableStack)
