from sklearn.svm import SVC
from sklearn.metrics import scorer
import pandas as pd
from matplotlib import style
import numpy as np
import matplotlib.pyplot as plt
from pandas_datareader import data as web
import quandl
style.use('fivethirtyeight')

df = web.DataReader('AAPL', 'quandl', input("Enter the starting date of the stock(format=YYYY-MM-DD): \n"), input("Enter the ending date of the stock(format=YYYY-MM-DD): \n"))
#data=quandl.get("FRED/GDP",returns="pandas")
df=df[['Open','High','Low','Close']]
print(df.head())
df['High']=df['High'].shift(1)
df['Low']=df['Low'].shift(1)
df['Close']=df['Close'].shift(1)
df['Signal']=1
df['Signal'][df['Open'].shift(-1)<df['Open']]=-1
df=df.dropna()
x=df[['Open','High','Low','Close']]
y=df['Signal']
t=0.8
split=int(t*len(df))
x_train,y_train=x[:split],y[:split]
print(x_train)
reg=SVC(C=1,cache_size=200,class_weight=None,coef0=0,decision_function_shape=None,degree=3,gamma='auto',kernel='rbf',max_iter=1000,probability=False,random_state=None,shrinking=True,tol=0.001,verbose=False).fit(x_train,y_train)
y_predict=reg.predict(x[split:])
df=df.assign(p_trend=pd.Series(np.zeros(len(x))).values)
df['p_trend'][split:]=y_predict
accuracy=scorer.accuracy_score(df['Signal'][split:],df['p_trend'][split:])
df=df.assign(ret=pd.Series(np.zeros(len(x))).values)
df['ret']=np.log(df['Open'].shift(-1)/df['Open'])
df=df.assign(ret1=pd.Series(np.zeros(len(x))).values)
df['ret1']=df['p_trend']*df['ret']
df=df.assign(cu_ret1=pd.Series(np.zeros(len(x))).values)
df['cu_ret1']=np.cumsum(df['ret1'][split:])
df=df.assign(cu_ret=pd.Series(np.zeros(len(x))).values)
df['cu_ret']=np.cumsum(df['ret'][split:])
std=pd.expanding_std(df['cu_ret1'])
sharpe=(df['cu_ret1']-df['cu_ret'])/std
sharpe=sharpe[split:].mean()
print("\n\n ACCURACY :",accuracy)
plt.plot(df['cu_ret1'],color='b',label='Strategy Returns')
plt.plot(df['cu_ret'],color='g',label='Market Returns')
plt.figtext(0.14,0.7,s='Sharpe ratio: %.2f'%sharpe)
plt.legend(loc='best')
plt.show()
