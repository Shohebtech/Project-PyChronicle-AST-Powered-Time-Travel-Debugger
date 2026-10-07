x = 10

try:
    y = x / 0
except ZeroDivisionError:
    y = -1

print(y)