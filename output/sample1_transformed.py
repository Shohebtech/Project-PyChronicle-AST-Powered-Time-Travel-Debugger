def track(name, value, line):
    print(f'[TRACK] Line {line}: {name} = {value}')
x = 10
track('x', x, line=1)
y = 20
track('y', y, line=2)
a = b = 5
track('a', a, line=3)
track('b', b, line=3)
if x > 5:
    z = 20
    track('z', z, line=6)
for i in range(3):
    w = i
    track('w', w, line=9)

def greet(name):
    message = 'hello'
    track('message', message, line=12)
    return message
greet('world')
x += 5
track('x', x, line=17)
print(x + y)