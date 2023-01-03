import pandas as pd


def findDependant(df):
    writeRows = df.query("OPERATION == 'WRITE'")
    readRows = df.query("OPERATION == 'READ'")
    dependant = []
    print(readRows.shape[0])

    for i in range(readRows.shape[0]):
        print(i)
        row = readRows.iloc[i]
        table = row['TABLE_NAME']
        pNameRead = row['PROC_NAME']
        keyRead = row['GP2KEY']
        toPop = []
        skipNumComparison = False
        try:
            nameNumRead = int(pNameRead[-3:])
        except Exception:
            skipNumComparison = True

        if not skipNumComparison:
            batchProc = writeRows.query("PROC_NAME != '" + pNameRead + "'") 
            batchProc = batchProc.query("GP2KEY == '" + keyRead + "'")
            batchProc = batchProc['PROC_NAME'].unique()
            for y in range(len(batchProc)):
                try:
                    curNum = int(batchProc[y][-3:])
                    if curNum > nameNumRead:
                        toPop.append(batchProc[y])
                except Exception:
                    h = 0

            for v in range(len(toPop)):
                writeRows = writeRows.query("PROC_NAME != '" + toPop[v] + "'") 
        
        writeTables = writeRows.query("PROC_NAME != '" + pNameRead + "'") 
        writeTables = list(writeTables['TABLE_NAME'].unique())
        if table in writeTables:
            dependant.append(row['PROC_NAME'])


        # for x in range(writeRows.shape[0]):
        #     #print(x)
        #     rowWrite = writeRows.iloc[x]
        #     tableWrite = rowWrite['TABLE_NAME']
        #     if table == tableWrite:
        #         pNameRead = row['PROC_NAME']
        #         pNameWrite = rowWrite['PROC_NAME']
        #         if pNameRead != pNameWrite:
        #             keyRead = row['GP2KEY']
        #             keyWrite = rowWrite['GP2KEY']
        #             if keyRead == keyWrite:
        #                 nameNumRead = int(pNameRead[-3:])
        #                 nameNumWrite = int(pNameWrite[-3:])
        #                 if nameNumWrite > nameNumRead:
        #                     dependant.append(row['PROC_NAME'])
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

