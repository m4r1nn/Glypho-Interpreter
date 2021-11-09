import sys
from sys import argv, stderr, stdin
from collections import deque

queue = deque()
pairs = {}
base = 0


# convert a number from base b to base 10
def convert(n, b):
    if (n < 0):
        return ('-' + convert(-n, b))
    if n == 0:
        return '0'
    digits = []
    while n:
        if int(n % b) >= 10:
            digits.append(chr(ord('A') + int(n % b) - 10))
        else:
            digits.append(str(int(n % b)))
        n //= b
    return ''.join(digits[::-1])


# decode instruction
def decode(string):
    code = []
    counter = 0
    my_dict = {}
    for x in string:
        if not x in my_dict:
            code.append(str(counter))
            my_dict[x] = counter
            counter = counter + 1;
        else:
            code.append(str(my_dict[x]))
    return ''.join(code)
    

# handler for the instructions
def execute(i, instruction):
    global base
    if instruction == '0000': #NOP
        pass
    
    elif instruction == '0001': #Input
        try:
            x = int(stdin.readline(), base)
            queue.append(x)
        except:
            error_message = 'Exception:' + str(i)
            stderr.write(error_message)
            sys.exit(-2) 
        
    elif instruction == '0010': #Rot
        if len(queue) == 0:
            error_message = 'Exception:' + str(i)
            stderr.write(error_message)
            sys.exit(-2)
        queue.rotate(1)
    
    elif instruction == '0011': #Swap
        if len(queue) <= 1:
            error_message = 'Exception:' + str(i)
            stderr.write(error_message)
            sys.exit(-2)
        x = queue[-1]
        queue[-1] = queue[-2]
        queue[-2] = x
    
    elif instruction == '0012': #Push
        queue.append(1)
    
    elif instruction == '0100': #RRot
        if len(queue) == 0:
            error_message = 'Exception:' + str(i)
            stderr.write(error_message)
            sys.exit(-2)
        queue.rotate(-1)
    
    elif instruction == '0101': #Dup
        if len(queue) == 0:
            error_message = 'Exception:' + str(i)
            stderr.write(error_message)
            sys.exit(-2)
        queue.append(queue[-1])
    
    elif instruction == '0102': #Add
        if len(queue) <= 1:
            error_message = 'Exception:' + str(i)
            stderr.write(error_message)
            sys.exit(-2)
        x = queue[-1]
        y = queue[-2]
        queue.pop()
        queue[-1] = x + y
    
    elif instruction == '0110': #L-brace
        if len(queue) == 0:
            error_message = 'Exception:' + str(i)
            stderr.write(error_message)
            sys.exit(-2)
        if queue[-1] == 0:
            return pairs[i] + 1
    
    elif instruction == '0111': #Output
        if len(queue) == 0:
            error_message = 'Exception:' + str(i)
            stderr.write(error_message)
            sys.exit(-2)
        print(convert(queue[-1], base))
        queue.pop()
    
    elif instruction == '0112': #Multiply
        if len(queue) <= 1:
            error_message = 'Exception:' + str(i)
            stderr.write(error_message)
            sys.exit(-2)
        x = queue[-1]
        y = queue[-2]
        queue.pop()
        queue[-1] = x * y
    
    elif instruction == '0120': #Execute
        if len(queue) <= 3:
            error_message = 'Exception:' + str(i)
            stderr.write(error_message)
            sys.exit(-2)
        new_instruction = []
        for _ in range(0, 4):
            new_instruction.append(str(queue[-1]))
            queue.pop()
        new_instruction = decode(new_instruction)
        if new_instruction != '0110' and new_instruction != '0123':
            execute(i, new_instruction)
        else:
            error_message = 'Exception:' + str(i)
            stderr.write(error_message)
            sys.exit(-2)
        
    elif instruction == '0121': #Negate
        if len(queue) == 0:
            error_message = 'Exception:' + str(i)
            stderr.write(error_message)
            sys.exit(-2)
        queue[-1] = -queue[-1]
    
    elif instruction == '0122': #Pop
        if len(queue) == 0:
            error_message = 'Exception:' + str(i)
            stderr.write(error_message)
            sys.exit(-2)
        queue.pop()
    
    elif instruction == '0123': #R-brace
        return pairs[i]
    
    return i + 1
    

def main():
    global base
    file_name = argv[1]
    file = open(file_name, 'r')
    if len(argv) > 2:
        base = int(argv[2])
    else:
        base = 10
    
    # read text
    line = file.readline()
    code = ''.join(list(filter(lambda x: ord(x) >= 33 and ord(x) <=126, line)))
    
    # build instructions vector
    instructions = []
    instruction = []
    for letter in code:
        instruction.append(letter)
        if (len(instruction) == 4):
            instructions.append(''.join(instruction))
            instruction = []
    # check for syntax error
    if (len(instruction) != 0):
        error_message = 'Error:' + str(len(instructions))
        stderr.write(error_message)
        sys.exit(-1)
        
    # decode all instructions
    instructions = list(map(decode, instructions))
    
    # check for parentheses errors
    stack = []
    counter = 0
    for index, i in enumerate(instructions):
        if i == '0110':
            stack.append(index)
            counter = counter + 1
        elif i == '0123':
            if counter == 0:
                error_message = 'Error:' + str(index)
                stderr.write(error_message)
                sys.exit(-1)
            pairs[stack[-1]] = index
            pairs[index] = stack[-1]
            stack.pop()
            counter = counter - 1
    if counter > 0:
        error_message = 'Error:' + str(len(instructions))
        stderr.write(error_message)
        sys.exit(-1)
            
        
    # execute instructions
    i = 0
    while i < len(instructions):
        i = execute(i, instructions[i])

    file.close()
    sys.exit(0)
    pass


if __name__ == '__main__':
    main()