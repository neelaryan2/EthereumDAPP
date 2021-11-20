from collections import defaultdict
import os, sys
from glob import glob

import matplotlib
matplotlib.use('Agg')
from matplotlib import style
style.use('ggplot')
import matplotlib.pyplot as plt

functions = ['registerUser', 'createAcc', 'sendAmount', 'closeAccount']

def parse(line):
    line = [l.split(': ') for l in line.split('  ')]
    call, status = line.pop(0)
    function, args = call.split('(')
    args = eval('(' + args)
    ret = {'function': function, 'args':args, 'status':status}
    for k, v in line:
        ret[k] = v
    return ret

def getGas(lines):
    gases = defaultdict(lambda: [])
    for row in lines:
        function = row['function']
        gas = int(row['gasUsed'])
        if row['status'] == 'SUCCESS':
            gases[function].append(gas)

    for function, gas in gases.items():
        print(function, max(gas), sep=': ')


def plot(x, y):
    image_file = os.path.join('output', 'plot.png')
    fig = plt.figure(dpi=300)
    plt.plot(x, y)
    plt.xlabel('Number of txns')
    plt.ylabel('Success Ratio')
    plt.savefig(image_file, bbox_inches='tight')
    plt.close()

folder = 'output'

if len(sys.argv) <= 1:
    logfile = os.path.join(folder, 'run.log')
    max_counter = -1
    for file in glob(os.path.join(folder, 'run_*.log')):
        counter = int(file.split('_')[-1][:-4])
        if counter >  max_counter:
            max_counter = counter
            logfile = file
else:
    logfile = os.path.join(folder, sys.argv[1])

with open(logfile, 'r') as fp:
    lines = [parse(l.strip()) for l in fp if l.strip()]

getGas(lines)

values = []
for l in lines:
    if l['function'] == functions[2]:
        status = int(l['status'] == 'SUCCESS')
        values.append(status)

step = 100
success, size = 0, 0
x, y = [], []
print('Successful transaction summary')
print('success_txn\ttotal_txn\tratio')
for i in range(0, len(values), step):
    chunk = values[:i + step]
    success = sum(chunk)
    size = len(chunk)
    cur = success / size
    y.append(cur)
    x.append(size)
    print('%s\t\t%s\t\t%.4f' % (success, size, cur))

plot(x, y)
