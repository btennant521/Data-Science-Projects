import pandas as pd

def loadInvestments(filename):
    investOptions = []
    metro = pd.read_csv(filename)
    for i in range(1,5):
        name = metro.iloc[i][1]
        price = metro.iloc[i][-1]
        dif = metro.iloc[i][-1] - metro.iloc[i][-13]
        investOptions.append( (name,price,dif))
    return investOptions

#price in jan(option at 1) is our kg, dif(option at 2) is our profit
def optimizeInvestments(ops,money,inc):
    rows = (money//inc)+1
    cols = len(ops)+1
    mat = [[0 for i in range(rows)] for i in range(cols)]
    traceback = [[0 for i in range(rows)] for i in range(cols)]
    for i in range(cols):
        for j in range(rows):
            if i==0 or j==0:
                mat[i][j] = 0
                traceback[i][j] = None
            elif ops[i-1][1] <= j*inc:
                max = mat[i-1][j]
                val = ops[i-1][2]+mat[i-1][(j*inc-ops[i-1][1])//inc]
                if val > max:
                    mat[i][j] = val
                    if traceback[i-1][(j*inc-ops[i-1][1])//inc] != None:
                        traceback[i][j] = ops[i-1][0] + ' and ' + traceback[i-1][(j*inc-ops[i-1][1])//inc]
                    else:
                        traceback[i][j] = ops[i-1][0]
                else:
                    mat[i][j] = max
                    if traceback[i-1][j] != None:
                        traceback[i][j] = traceback[i-1][j] +' and '+ ops[i-1][0]
                    else:
                        traceback[i][j] = ops[i-1][0]


            else:
                mat[i][j] = mat[i-1][j]
                traceback[i][j] = traceback[i-1][j]

        res = (mat[cols-1][rows-1], traceback[cols-1][rows-1])
    return res

print(optimizeInvestments(loadInvestments('Metro.csv'),1000000,1000))
