import numpy as np
import pandas as pd
import os
os.chdir('/Users/andy/Documents/Spring17/291/project/data') # Set working directory
# Import the necessary modules and libraries
from sklearn import tree
import numpy as np
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt

from sklearn.utils import shuffle
from sklearn.metrics import r2_score

# Create a random dataset

os.chdir('/Users/andy/Documents/Spring17/291/project/data') # Set working directory

train_data_stride = pd.read_csv("stride_result.csv")    # Read the data
train_data_random = pd.read_csv("random_result.csv")
train_data_seq = pd.read_csv("seq_result.csv")

print len(train_data_stride)
print len(train_data_random)
print len(train_data_seq)
train_data = pd.concat([train_data_seq, train_data_random,train_data_stride])

print len(train_data)

train_data = shuffle(train_data)

MAE_all = []
MRE_all = []
R2_all = []

for index in range(1, 4):
    if index == 1:
        print "iops"
    elif index == 2:
        print "bandwidth"
    else:
        print "latency"
    X = []
    y = []
    for i in range(len(train_data)*9/10):
        line = train_data[i:i+1].values.tolist()[0]
        X.append(line[:-3])
        y.append(line[-index])

    print "Train size: ", len(X), len(y)
    X_test = []
    y_test = []
    for i in range(len(train_data)*9/10, len(train_data)):
        line = train_data[i:i+1].values.tolist()[0]
        X_test.append(line[:-3])
        y_test.append(line[-index])

    print "Test size:", len(X_test), len(y_test)

    # Fit regression model
    MAE = []
    MRE = []
    R2 = []
    for i in range(2,11):
        regr = DecisionTreeRegressor(max_depth=i)
        regr.fit(X, y)
        # Predict
        y_p = regr.predict(X_test)

        # Plot the results
        mae = np.mean(abs(y_test-y_p))
        MAE.append(mae)
        mre = np.mean(abs(y_test-y_p)/y_test)
        MRE.append(mre)
        r2 = r2_score(y_test, y_p) 
        R2.append(r2)
        print "depth = ",i,"  MRE: ", mre, "  R2: ", r2
    MAE_all.append(MAE)
    MRE_all.append(MRE)
    R2_all.append(R2)

plt.plot([2,3,4,5,6,7,8,9,10],R2_all[0])
plt.plot([2,3,4,5,6,7,8,9,10],R2_all[1])
plt.plot([2,3,4,5,6,7,8,9,10],R2_all[2])
plt.ylabel('R2')
plt.xlabel('tree depth')
plt.legend(['iops','bandwidth','latency'])
plt.show()

plt.plot([2,3,4,5,6,7,8,9,10],MAE_all[2])
plt.ylabel('MAE_latency')
plt.xlabel('tree depth')
plt.legend(['latency'])
plt.show()

plt.plot([2,3,4,5,6,7,8,9,10],MAE_all[1])
plt.ylabel('MAE_bandwidth')
plt.xlabel('tree depth')
plt.legend(['bandwidth'])
plt.show()


plt.plot([2,3,4,5,6,7,8,9,10],MAE_all[0])
plt.ylabel('MAE_ipos')
plt.xlabel('tree depth')
plt.legend(['iops'])
plt.show()

plt.plot([2,3,4,5,6,7,8,9,10],MRE_all[0])
plt.plot([2,3,4,5,6,7,8,9,10],MRE_all[1])
plt.plot([2,3,4,5,6,7,8,9,10],MRE_all[2])
plt.ylabel('MRE')
plt.xlabel('tree depth')
plt.legend(['iops','bandwidth','latency'])
plt.show()