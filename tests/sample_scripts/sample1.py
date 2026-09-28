x = 10
y = 20
a = b = 5

p, q = 1, 2

if x > 5:
    z = 20

for i in range(3):
    w = i

def greet(name):
    message = "hello"
    return message

greet("world")

x += 5

class Counter:
    def __init__(self):
        self.count = 0

counter = Counter()
counter.count = 99

arr = [0, 0, 0]
arr[0] = 42

score = 75

if score >= 90:
    grade = "A"
elif score >= 75:
    grade = "B"
else:
    grade = "C"

try:
    ratio = 10 / 0
except ZeroDivisionError:
    ratio = -1
else:
    ratio = ratio + 1
finally:
    finished = True

print(x + y)