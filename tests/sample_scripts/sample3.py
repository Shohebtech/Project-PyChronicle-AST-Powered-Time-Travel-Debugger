def process_matrix(size):
    total = 0
    for row in range(size):
        for col in range(size):
            if row == col:
                total += 1
            elif row > col:
                total -= 1
            else:
                total = total
    return total


def double(n):
    result = n * 2
    return result


def quadruple(n):
    step1 = double(n)
    step2 = double(step1)
    return step2


count = 0
count += 1
count += 1
count *= 2

matrix_result = process_matrix(3)
final_value = quadruple(5)

print(matrix_result, final_value, count)