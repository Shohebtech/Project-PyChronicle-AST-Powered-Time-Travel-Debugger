def track(name, value, line):
    print(f'[TRACK] Line {line}: {name} = {value}')
x = 10
track('x', x, line=1)
y = 20
track('y', y, line=2)
a = b = 5
track('a', a, line=3)
track('b', b, line=3)
p, q = (1, 2)
track('p', p, line=5)
track('q', q, line=5)
if x > 5:
    z = 20
    track('z', z, line=8)
for i in range(3):
    w = i
    track('w', w, line=11)

def greet(name):
    message = 'hello'
    track('message', message, line=14)
    return message
greet('world')
x += 5
track('x', x, line=19)

class Counter:

    def __init__(self):
        self.count = 0
counter = Counter()
track('counter', counter, line=25)
counter.count = 99
track('counter.count', counter.count, line=26)
arr = [0, 0, 0]
track('arr', arr, line=28)
arr[0] = 42
track('arr[0]', arr[0], line=29)
print(x + y)