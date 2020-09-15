import numpy as np
import pandas as pd
import pickle
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import export_graphviz
import graphviz

# loading dataset
df = pd.read_csv('./SP_DETAIL3.CSV',index_col='SPNAME')

# selecting feature and target column
feature_names = ['SUSPEND', 'LOCK_LATCH',
       'SYNCIO', 'SQL_STMT_AVG' ,'CP_CPU_SU' ,'SQL_STMT_TOTAL', 'OCCUR']
X = df[feature_names]
y = df['SP_OK']

# splitting data
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=22)

# fitting and predection
model = DecisionTreeClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(accuracy_score(y_test,y_pred))

#saving model
filename = 'finalized_model.sav'
pickle.dump(model, open(filename, 'wb'))

#print predection value
df_pridict = pd.read_csv('./SP_DETAIL4.csv',index_col='SPNAME')
X_pridict = df_pridict[feature_names]
y_pred_pridict = model.predict(X_pridict)

i = 0
while(i < y_pred_pridict.size):
       if (y_pred_pridict[i] == 0):
              print(X_pridict.index[i], X_pridict['OCCUR'].values[i], y_pred_pridict[i])
              print("-------")
       #if (y_test.values[i] != y_pred[i]):
              #print(y_test.index[i],y_test.values[i],y_pred[i])
       i+=1
print('TOTAL COUNT:'+str(i))

#decision tree graph
#dot_file = export_graphviz(model, feature_names= feature_names, out_file=None)
#graph = graphviz.Source(dot_file)
#graph.render('tree', format = 'png', view=True)