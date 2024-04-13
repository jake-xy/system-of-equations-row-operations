import os, math
from fraction import Fraction

def get_row_operation():
    while True:
        row_operation_input = input("row operation > ")

        if '=' in row_operation_input:
            row_operation = row_operation_input.split('=')[1].strip()
            if 'R' in row_operation or 'r' in row_operation:
                return row_operation_input

        elif row_operation_input == 'q' or row_operation_input == 'b':
            return row_operation_input

        else:
            print(" ")
            print('Please enter a valid row operation...')
            print(" ")


def print_matrix(matrix, size):
    # get the longest sequence of number in terms of length
    longestLen = 0
    for row in range(size[0]):
        for col in range(size[1]):
            num_str = str(matrix[row][col])
            if len(num_str) > longestLen:
                longestLen = len(num_str)

    print(" ")
    for row in range(size[0]):
        row_str = ''
        for col in range(size[1]):
            num_str = str(matrix[row][col])
            # If it's a whole number (denominator is 1):
            if num_str.split('/')[1] == '1':
                # Print only the numerator
                num_str = num_str.split('/')[0]
        
            row_str += center_text(num_str, 7)

            # add another space for the next numbers
                # space before a new number
            row_str += '  '

        print(row_str)
    print(" ")


def get_matrix():
    # prompt user for matrix size
    while True:
        try:
            size = input("matrix size > ").split(" ")
            size = [int(num) for num in size]
            if len(size) == 2:
                print(size)
                break
        except ValueError:
            print('not a valid input bruh')

    # prompt for the actual matrix
    while True:
        userInput = input("Enter your matrix > ").split(" ")
        oneDimArray = [item for item in userInput if item != '']

        if len(oneDimArray) == size[0]*size[1]:
            break
        else:
            print(f'Error!: Got a (1, {len(oneDimArray)}) array. Expected (1, {size[0]*size[1]})')

    # change this so it can accomodate fractions
    # array = [int(num) for num in array]
    array = []
    for item in oneDimArray:
        # if it's a whole number
        try:
            array.append(Fraction(int(item),1))
        # except if it's a fraction
        except ValueError:
            frac = item.split('/')
            array.append(Fraction(int(frac[0]), int(frac[1])) )

    # convert the matrix into it's appropriate size
    matrix = []
    for row in range(size[0]):
        row = row * size[1]
        matrix.append(array[row:row+size[1]])
    
    return matrix, size


def get_arithmetic(row_operation_input = "R1 = -3/4R1 + -1/2R2"):
    row_operation = row_operation_input.split('=')[1].strip()
    operators = ['*','/', '+','-']

    for i, char in enumerate(row_operation):
        # if there's an arithmetic operator and there are spaces on each of its side
        if char in operators and row_operation[i-1] == ' ' and row_operation[i+1] == ' ':

            return char
    
    return None


def get_multipliers(row_operation_input = "R1 = -3/4R1 + -1/2R2"):
    row_operation = row_operation_input.split('=')[1].strip()
    multipliers = []
    row_ids = []
    # get the location of R in the row operation
    R_ids = [i for i, char in enumerate(row_operation) if char.upper() == 'R']
    # R1 > -3/4R1 + -1/2R2
    nums = [1, 1]
    # if there is a multiplier before the first row operation,
    if R_ids[0] > 0:
        operationStr = row_operation[0:R_ids[0]].strip()
        # if the multiplier is a fraction
        if '/' in operationStr:
            nums = [int(n) for n in operationStr.split('/')]
        else:
            nums[0] = int(operationStr)

    row_ids.append(int(row_operation[R_ids[0]+1]) - 1)
    multipliers.append(Fraction(nums[0], nums[1]))

    # if there 2 rows are involved
    if len(R_ids) == 2:
        nums = [1, 1]
        # get the arithmetic opration
        arithmetic = get_arithmetic(row_operation_input)
        # if there is a multiplier before the second row operation
        if row_operation[R_ids[1]-1] != ' ':
            operationStr = row_operation[row_operation.find(arithmetic)+1:R_ids[1]].strip()
            # if the multiplier is a fraction
            if '/' in operationStr:
                nums = [int(n) for n in operationStr.split('/')]
            else:
                nums[0] = int(operationStr)
        
        row_ids.append(int(row_operation[R_ids[1]+1]) - 1)
        multipliers.append(Fraction(nums[0], nums[1]))

    return multipliers, row_ids



def get_which_row(row_operation):
        row_operation = row_operation.split('=')[0].strip()
        row = int(row_operation[1]) - 1
        return row


def get_arithmetic_value(row_operation_input = "R1 = -3/4R1 + -1/2R2"):
    row_operation = row_operation_input.split('=')[1].strip()
    arithmetic = get_arithmetic(row_operation_input)

    if arithmetic != None:
        valStr = row_operation.split(arithmetic)[1].strip()
        # if the value is a number only, and no row operation involved
        if 'R' not in valStr and 'r' not in valStr:
            # if it's a fraction
            if '/' in valStr:
                return Fraction(int(valStr.split('/')[0]), int(valStr.split('/')[1]))
            else:
                return Fraction(int(valStr), 1)

    return Fraction(0)


def perform_row_operation(matrix, size, whichRow, multipliers, row_ids, arithmetic, arithmeticVal):
    for col in range(size[1]):
        out = Fraction(0)
        out = matrix[row_ids[0]][col] * multipliers[0]
        if arithmetic != None:
            if len(row_ids) == 2:
                if arithmetic == '+':
                    out += matrix[row_ids[1]][col] * multipliers[1]
                if arithmetic == '-':
                    out -= matrix[row_ids[1]][col] * multipliers[1]
            if arithmeticVal != 0:
                if arithmetic == '+':
                    out += arithmeticVal
                if arithmetic == '-':
                    out -= arithmeticVal

        matrix[whichRow][col] = out

    return matrix


def center_text(text="aaa", containerSize=5):
    out = ''
    # start index is center of the container minus text's length divided by 2
    startIndex = math.ceil(containerSize/2) - math.ceil(len(text)/2)
    # add space until the start index is reached
    out += ' ' * startIndex
    # add the actual text
    out += text
    # add the remaining space left on the container
    out += ' ' * (containerSize - len(out))

    return out


# def step_back():
#     global matrixHistory
#     prevMatrix = matrixHistory[len(matrixHistory)-2]
#     print('---------')
#     print(len(matrixHistory)-2)
#     print(matrixHistory)
#     print('---------')
#     matrixHistory.pop()

#     return prevMatrix



# MAIN LOOP
while True:
    os.system('cls')
    matrix, size = get_matrix()
    # matrix = [[Fraction(1,1), Fraction(2,1)], [Fraction(4,1), Fraction(5,1)]]
    # size = [2, 2]
    print_matrix(matrix, size)

    while True:
        # GET THE ROW OPERATION (prompt the user)
        print('q - quit')
        row_operation = get_row_operation()

        # if the user wants to quit
        if row_operation == 'q':
            print(' ')
            print('DONE!')
            print(' ')
            os.system('pause')
            break
        
        else:
            # GET WHICH ROW WILL THE OPERATION OCCUR
            whichRow = get_which_row(row_operation)
            # print('row = ', whichRow)

            # GET THE MULTIPLIERS
                # w/ its corresponding row
            multipliers, row_ids = get_multipliers(row_operation)

            # GET THE ARITHMETIC OPERATOR IF THERE IS ANY
            arithmetic = get_arithmetic(row_operation)

            # GET THE VALUE AFTER THE ARITHMETIC OPERATOR IF THERE IS ANY
            arithmeticVal = get_arithmetic_value(row_operation)

            # perform row operation
            matrix = perform_row_operation(matrix, size, whichRow, multipliers, row_ids, arithmetic, arithmeticVal)


        print_matrix(matrix, size)


# just do prev copy. not histpry