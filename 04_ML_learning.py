import os
import random
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR 
import math
import joblib 

random.seed(42)

# 최종 merge 데이터
mergedata = pd.read_csv('data/total_df.csv', encoding='cp949')
# mergedata = mergedata.sample(n=10000)
# month 열 추가
mergedata['기준_날짜시간']=pd.to_datetime(mergedata['기준_날짜시간'],format="%Y-%m-%d %H:%M:%S")
mergedata['month']=mergedata['기준_날짜시간'].dt.month
# 학습시킬 features로 df 재구성 
mergedata=mergedata[['month','time','요일', '전체_건수','버스 수', '버스_하차승객수', '지하철하차승객수', '강수', '기온', '풍속', 'dem']]
# one-hot encoding
mergedata=pd.get_dummies(mergedata, columns=['month','time','요일']) # 요일, month, time

X_train, X_test, y_train, y_test = train_test_split(mergedata.drop('전체_건수',axis=1), mergedata['전체_건수'], test_size=0.2, random_state=42)

### 데이터 학습 및 최적 파라미터로 최종모형 생성 / 테스트셋 성능평가 
# XGBoosting
'''
pipeline = Pipeline([('Scaler', StandardScaler()), ('XGB', XGBRegressor())]) # scalar 적용 

lambda_list = [1, 2, 3, 4, 5]
gamma_list = [10, 50, 100, 150, 200]
parameters = {'XGB__reg_lambda':lambda_list, 'XGB__gamma':gamma_list}

xgb_grid = GridSearchCV(pipeline, parameters, cv=5, scoring = 'neg_root_mean_squared_error') # 5-fold cross validation 
xgb_grid.fit(X_train, y_train)

reg = XGBRegressor(reg_lambda = xgb_grid.best_params_['XGB__reg_lambda'], 
                   gamma = xgb_grid.best_params_['XGB__gamma'])
reg.fit(X_train, y_train)

y_pred=reg.predict(X_test)
RMSE = math.sqrt(mean_squared_error(y_test, y_pred))
print("XGB RMSE':{}".format(RMSE))
print("XGB best reg_lambda':{},best gamma':{}".format(xgb_grid.best_params_['XGB__reg_lambda'],xgb_grid.best_params_['XGB__gamma']))
'''

# Random Foreast
'''
pipeline = Pipeline([('Scaler', StandardScaler()), ('RF', RandomForestRegressor())]) # scalar 적용 

max_depth_list = [5,10,15]
min_samples_leaf_list = [5,15]
n_estimators_list= [50,100,200]

parameters = {'RF__max_depth':max_depth_list, 
              'RF__min_samples_leaf':min_samples_leaf_list, 
              'RF__n_estimators':n_estimators_list}

rf_grid = GridSearchCV(pipeline, parameters, cv=5, scoring = 'neg_root_mean_squared_error') # 5-fold cross validation 
rf_grid.fit(X_train, y_train)

reg = RandomForestRegressor(max_depth = rf_grid.best_params_['RF__max_depth'], 
                            min_samples_leaf = rf_grid.best_params_['RF__min_samples_leaf'],
                            n_estimators = rf_grid.best_params_['RF__n_estimators'])
reg.fit(X_train, y_train)

y_pred=reg.predict(X_test)
RMSE = math.sqrt(mean_squared_error(y_test, y_pred))
print("RF RMSE':{}".format(RMSE))
print("RF best max_depth:{}, best min_samples_leaf:{}, best n_estimators:{}".format(rf_grid.best_params_['RF__max_depth'], rf_grid.best_params_['RF__min_samples_leaf'], rf_grid.best_params_['RF__n_estimators']))
'''

# SVR 
pipeline = Pipeline([('Scaler', StandardScaler()), ('SVR', SVR())])

kernel_list = ['linear','rbf']
C_list = [1, 10,20]
parameters = {'SVR__kernel':kernel_list, 'SVR__C':C_list}

svm_grid = GridSearchCV(pipeline, parameters, cv=5, scoring = 'neg_root_mean_squared_error', n_jobs=4) # 5-fold cross validation # 메모리 병렬처리 
svm_grid.fit(X_train, y_train)

svr_best_C = svm_grid.best_params_['SVR__C']
svr_best_kernel = svm_grid.best_params_['SVR__kernel']

reg = SVR(C = svr_best_C, 
          kernel = svr_best_kernel)
reg.fit(X_train, y_train)

y_pred=reg.predict(X_test)
RMSE = math.sqrt(mean_squared_error(y_test, y_pred))

print("SVR RMSE':{}".format(RMSE))
print("SVR best kernel:{}, best C:{}".format(svr_best_kernel, svr_best_C))

# 모델 저장
joblib.dump(reg,f'SVR_{round(RMSE,2)}_k{svr_best_kernel}_C{svr_best_C}.pkl')