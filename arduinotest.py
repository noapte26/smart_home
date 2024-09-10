test = [ 
  501, 519, 536, 552,
  399, 425, 448, 470,
  248, 287, 323, 355,
  0,    67, 126, 178]

plus = []
minus = []

ran = 8

for key in test:
    plus.append(key+ran)
    minus.append(key-ran)

if any(item in plus for item in test):
    print('shit')
else:
    print('plus is good')

if any(item in minus for item in test):
    print('shit')
else:
    print('minus is good')

if any(item in minus for item in plus):
    print('shit')
else:
    print('all is good')

print(plus)
print(minus)

tru = 0
fls = 0

for i in range(len(test)-1):
    if (plus[i]>minus[i+1]):
       tru += 1
    else:
       fls += 1

print(tru,fls)