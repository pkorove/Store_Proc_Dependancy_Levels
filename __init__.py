import pandas as pd


def findDependant(df):
    writeRows = df.query("OPERATION == 'WRITE'")
    readRows = df.query("OPERATION == 'READ'")

    writeTables = list(writeRows['TABLE_NAME'].unique())

    dependant = []

    for i in range(readRows.shape[0]):
        row = readRows.iloc[i]
        table = row['TABLE_NAME']
        if table in writeTables:
            dependant.append(row['PROC_NAME'])
    
    return dependant


def findNonDependant(df):
    dependant = findDependant(df)
    nonDepRows = df[~df['PROC_NAME'].isin(dependant)]
    nonDepProc = list(nonDepRows['PROC_NAME'].unique())
    depRows = df[df['PROC_NAME'].isin(dependant)]
    return nonDepProc, depRows




df = pd.read_excel('Input\Input.xlsx')
levels = []

unqProcs = list(df['PROC_NAME'].unique())

print(len(unqProcs))
nonDP = None
i = 0

while nonDP != []:
    print('Written L' + str(i))
    nonDP, dr = findNonDependant(df)
    if nonDP != []:
        levels.append(nonDP)
    else:
        depProc = list(dr['PROC_NAME'].unique())
        levels.append(depProc)

    df = dr
    i += 1

depths = []
for i in range(len(levels)):
    depths.append(len(levels[i]))

maxDepth = max(depths)

totalLength = 0
for i in range(len(levels)):
    curLen = len(levels[i])
    for x in range(maxDepth - curLen):
        levels[i].append(None)
    totalLength += curLen

print(totalLength)

d = {}

for i in range(len(levels)):
    if i != len(levels)-1:
        keyName = 'L' + str(i)
        d[keyName] = levels[i]
    else:
        d['Remaining'] = levels[i]


output = pd.DataFrame.from_dict(d)

output.to_excel('Output\output.xlsx')

