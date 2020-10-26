#build model on train and use models to predict the test set data and see if we get similar results  
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from sklearn.model_selection import train_test_split,cross_val_score,GridSearchCV
from sklearn.linear_model import LinearRegression,Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error




data=pd.read_csv('glassdoor_jobs_eda.csv') 
data.columns
#choose relevant columns
data.columns
data_model=data[["avg_salary","Rating","Size","Type of ownership","Industry","Sector","Revenue","hourly","employer_provided",
             "job_state", "age", "python_yn","spark","aws","excel","job_simp","seniority", "desc_len"]]

#get dummy data
data_dum = pd.get_dummies(data_model) #create dummy variables 

#train test split
X = data_dum.drop('avg_salary',axis=1) #predictor 
y = data_dum.avg_salary.values   # response
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42) #80% train, 20% test

#multiple linear regression
X_sm = X = sm.add_constant(X) #add intercept
model = sm.OLS(y,X_sm)#regression linear model
model.fit().summary()

lm = LinearRegression()
lm.fit(X_train,y_train)
np.mean(cross_val_score(lm,X_train,y_train,scoring='neg_mean_absolute_error',cv=3)) #mini train test split
#-25.973036646994046
print(lm.coef_)  

#lasso linear regression (dataset is sparse with all these dummy variables, lasso helps to normilze that)
lm_l = Lasso()
lm_l.fit(X_train,y_train)
np.mean(cross_val_score(lm_l,X_train,y_train,scoring='neg_mean_absolute_error',cv=3))
#-21.927479011351128

alpha = []
error = []
for i in range(1,100):
    alpha.append(i/100)
    lml = Lasso(alpha=i/100)
    error.append(np.mean(cross_val_score(lml,X_train,y_train,scoring='neg_mean_absolute_error',cv=3)))

err = list(zip(alpha,error))
df_err= pd .DataFrame(err,columns=['alpha','error'])
df_err[df_err.error == max(df_err.error)] #max alpha=0.23 error=-20.639725
plt.plot(alpha,error) #alpha:0.2~0.3, error:-21~-20.5


#random forest  (we'll have a tree based model to compare our linear model, judging based on time.)
rf = RandomForestRegressor()
np.mean(cross_val_score(rf,X_train,y_train,scoring='neg_mean_absolute_error',cv=3))
#21.086743827160493
####also can use gradient boosted tree,suppoer vector regression both can spice this up a little bit.


#tune models GridsearchCV
parameters = {'n_estimators':range(10,300,10),'criterion':('mse','mae'),'max_features':('auto','sqrt','log2')}
gs = GridSearchCV(rf,parameters,scoring='neg_mean_absolute_error',cv=3)
gs.fit(X_train,y_train)

gs.best_score_ #-20.383429686370864 compare to random forest improved by a little
gs.best_estimator_#criterion='MAE', n_estimators=170


#test ensembles 
pred_lm = lm.predict(X_test)
#X_test['predlm'] = pred_lm

lm_l = Lasso(alpha=.23) #update alpha for prediction
lm_l.fit(X_train,y_train)
pred_lml = lm_l.predict(X_test)
#X_test['predlasso'] = pred_lml

pred_rf = gs.best_estimator_.predict(X_test)
#X_test['predrf'] = pred_rf 
print('MAE for Linear Regression:',mean_absolute_error(y_test,pred_lm))
print('MAE for Lasso Regression:',mean_absolute_error(y_test,pred_lml))
print('MAE for Random Forest Regressor:',mean_absolute_error(y_test,pred_rf))

#See if two models together perform better
print('MAE of Linear Regression combined with random Forest Regressor:',mean_absolute_error(y_test, (pred_lm+pred_rf)/2))

####FLASK API
###Building flask API endpoint
#take model bulit for predicting glassdoor salary, turn it into an API endpoint using flask
#this is known as porductionization and with an API endpoint we can have a website to reach out to it and get back reponse
#for our case is our website send information related to a job and our API endpoint return an expected salary 

import pickle
pickl = {'model': gs.best_estimator_}
pickle.dump( pickl, open( 'model_file' + ".p", "wb" ) )

file_name = "model_file.p"
with open(file_name, 'rb') as pickled:
   data = pickle.load(pickled)
   model = data['model']

model.predict(X_test.iloc[1,:].values.reshape(1,-1)) #salary prediction for the position is $74.2375 
#pickle does work

list(X_test.iloc[1,:])
