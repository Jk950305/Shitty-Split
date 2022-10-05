from flask import Flask, render_template, request, flash, session, redirect, url_for
import random
import math

app = Flask(__name__)
app.secret_key = "tjdwlsldlqslek_9595959595"

@app.route('/')
def search():

    return render_template('index.html')

@app.route('/trans', methods = ['GET', 'POST'])
def trans():
    if request.method == 'GET':
        return redirect(url_for('search'))
    else:
        users = request.form.getlist('input_text[]')
        session['users'] = users
        return render_template('trans.html',
                               users = users)


@app.route('/result', methods = ['GET', 'POST'])
def results():
    if request.method == 'GET':
        return redirect(url_for('search'))
    else:
    	users = session.get('users', None)
    	lenders = request.form.getlist('lenders')
    	amounts = request.form.getlist('amount[]')
    	borrowers = []

    	for i in range(len(lenders)):
    		string = 'checkboxes'+str(i+1)+'[]'
    		borrowers.append(request.form.getlist(string))
    		total = 0.0
    		for j in range(len(amounts)):
    			total = total+float(amounts[j])

    	trans = []
    	summary = []

    	num = len(lenders)
    	if ( num!=len(borrowers) or num!=len(borrowers) or num!=len(borrowers) ):
    		result=['FAILED']
    	else:
	    	for i in range(len(lenders)):
	    		tmp = []
	    		if(lenders[i]):tmp.append(lenders[i])
	    		if(amounts[i]):tmp.append(float(amounts[i]))
	    		if(borrowers[i]):tmp.append(borrowers[i])
	    		trans.append(tmp)

	    	graph = createGraph(users, trans)
	    	texts = minCashFlow(graph,users)
	    	arr = texts.split(',')
	    	result = arr[:-1]
	    	if len(result)==0:
	    		result= ['You guys are quits!']
	    	else:
	    		result.sort();

	    	summary = totalExpenses(users,graph)
	    	
    	return render_template('result.html',result=result, total=("%.2f" % total), summary=summary)





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

    res = str(users[mxDebit])+" gives $"+str("%.2f" % round(min,2))+" to "+str(users[mxCredit])+","
    return res+str(minCashFlowRec(amount,users))
    


def minCashFlow(graph,users):
 
    amount = [0 for i in range(len(graph))]
    for p in range(len(graph)):
        for i in range(len(graph)):
            amount[p] += (graph[i][p] - graph[p][i])

    return minCashFlowRec(amount,users)


def createGraph(users, trans):
    graph = [[0]*len(users) for _ in range(len(users))]

    pq = sorted(users, key = lambda x: random.random())

    for aTran in trans:
        giver = aTran[0]
        total = aTran[1]
        borrowers = aTran[2]
        len_borrowers = len(borrowers)
        split = total/len_borrowers

        a = 100 * total
        lo_val = math.floor(a/len_borrowers)
        hi_val =  lo_val+1
        num_hi = round(a%len_borrowers)
        num_low = len_borrowers-num_hi

        col = users.index(giver)

        cur_pq = pq.copy()
        for aUser in cur_pq:
            if aUser in borrowers:
                row = users.index(aUser)
                if num_hi>0 :
                    graph[row][col] = graph[row][col]+hi_val/100
                    num_hi = num_hi-1
                    pq.append(pq.pop(0))
                else :
                    graph[row][col] = graph[row][col]+lo_val/100
                
    return graph 


def totalExpenses(users, graph):
    lst = [[0]*2 for _ in range(len(users))]
    count = 0
    for row in graph:
        for col in row:
            lst[count][0] = users[count]
            lst[count][1] = round(sum(graph[count]),2)
        count = count + 1

    return lst
     


if __name__ == '__main__':
    app.run(debug = True)