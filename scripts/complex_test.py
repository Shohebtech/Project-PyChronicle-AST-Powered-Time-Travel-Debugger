def calculate_total(numbers):
    total = 0

    for number in numbers:
        if number > 0:
            total += number
        else:
            total -= number

    return total


def divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return None


numbers = [10, -5, 20, -2]

total = calculate_total(numbers)

result1 = divide(total, 5)
result2 = divide(total, 0)

print("Total:", total)
print("Result 1:", result1)
print("Result 2:", result2)