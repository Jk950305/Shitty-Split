from flask import Flask, render_template, request, flash, session

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"

@app.route('/')
def search():
    return render_template('index.html')

@app.route('/trans', methods = ['GET', 'POST'])
def trans():
    if request.method == 'GET':
        return redirect(url_for('/'))
    else:
        users = request.form.getlist('input_text[]')
        session['users'] = users
        return render_template('trans.html',
                               users = users)


@app.route('/result', methods = ['GET', 'POST'])
def results():
    if request.method == 'GET':
        return redirect(url_for('/'))
    else:
    	users = session.get('users', None)
    	lenders = request.form.getlist('lenders')
    	amounts = request.form.getlist('amount[]')
    	borrowers = []

    	for i in range(len(users)):
    		string = 'checkboxes'+str(i+1)+'[]'
    		borrowers.append(request.form.getlist(string))

    	trans = []

    	for i in range(len(lenders)):
    		tmp = []
    		tmp.append(lenders[i])
    		tmp.append(float(amounts[i]))
    		tmp.append(borrowers[i])
    		trans.append(tmp)

    	texts = minCashFlow(createGraph(users, trans),users)
    	arr = texts.split(',')
    	result = arr[:-1]


    	return render_template('result.html',users=users, lenders = lenders, amounts = amounts, borrowers=borrowers, result=result)





def getMin(arr):
     
    minInd = 0
    for i in range(1, len(arr)):
        if (arr[i] < arr[minInd]):
            minInd = i
    return minInd

def getMax(arr):
 
    maxInd = 0
    for i in range(1, len(arr)):
        if (arr[i] > arr[maxInd]):
            maxInd = i
    return maxInd

def minOf2(x, y):
 
    return x if x < y else y
 
def minCashFlowRec(amount,users):

    mxCredit = getMax(amount)
    mxDebit = getMin(amount)
 
    if (amount[mxCredit] == 0 and amount[mxDebit] == 0):
        return ""
    prev = amount.copy()

    min = minOf2(-amount[mxDebit], amount[mxCredit])
    amount[mxCredit] -=min
    amount[mxDebit] += min

    count = 0
    for i in amount:
        for j in prev:
            if i==j:
                count = count+1
                break

    if round(min,2)==0.0 :
        return ""

    res = str(users[mxDebit])+" gives $"+str(round(min,2))+" to "+str(users[mxCredit])+","
    return res+str(minCashFlowRec(amount,users))
    


def minCashFlow(graph,users):
 
    amount = [0 for i in range(len(graph))]
    for p in range(len(graph)):
        for i in range(len(graph)):
            amount[p] += (graph[i][p] - graph[p][i])

    return minCashFlowRec(amount,users)



def createGraph(users, trans):
    #graph = [[0]*len(users)]*len(users)
    graph = [[0]*len(users) for _ in range(len(users))]

    for aTran in trans:
        giver = aTran[0]
        total = aTran[1]
        borrowers = aTran[2]
        split = total/(len(borrowers))
        col = users.index(giver)
        for aBorrower in borrowers:
            row = users.index(aBorrower)
            graph[row][col] = split
    return graph 



     


if __name__ == '__main__':
    app.run(debug = True)