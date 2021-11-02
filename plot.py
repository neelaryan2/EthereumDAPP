from collections import defaultdict

import matplotlib
matplotlib.use('Agg')
from matplotlib import style
style.use('ggplot')
import matplotlib.pyplot as plt

def getGas(lines):
    gases = defaultdict(lambda: [])
    for l in lines:
        for function in functions:
            if l.startswith(function):
                l1, l2 = l.split('  ')
                status = l1.split(': ')[1]
                gas = int(l2.split(': ')[1])
                if status == 'SUCCESS':
                    gases[function].append(gas)

    for function, gas in gases.items():
        print(function, max(gas), sep=': ')

functions = ['registerUser', 'createAcc', 'sendAmount', 'closeAccount']

with open('run.log.backup', 'r') as fp:
    lines = [l.strip() for l in fp]

getGas(lines)

values = []
for l in lines:
    if l.startswith(functions[2]):
        l1, l2 = l.split('  ')
        status = l1.split(': ')[1]
        status = int(status == 'SUCCESS')
        values.append(status)

step = 100
success, size = 0, 0
y = []
for i in range(0, len(values), step):
    chunk = values[i:i + step]
    success += sum(chunk)
    size += len(chunk)
    cur = sum(chunk) / len(chunk)
    # cur = success / size
    y.append(cur)

fig = plt.figure(dpi=300)
plt.plot(y)
plt.xlabel('Number')
plt.ylabel('Success Ratio')
plt.savefig('plot.png', bbox_inches='tight')
plt.close()
