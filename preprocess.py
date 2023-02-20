import model
import view
import random
import sql
import os
import random
import json 
import datetime
import pickle
import time
import math
from bottle import request

timelimit=datetime.datetime(2021,8,19,0,0,0)

trls=[7,24,12]

keyword=["bitcoin","ethereum","dogecoin"]



def getpkl(keyword,tr):
    if tr=="7":
        timelimit=datetime.datetime(2021,8,19,0,0,1)
    if tr=="24":
        timelimit=datetime.datetime(2021,8,24,0,0,1)
    if tr=="12":
        timelimit=datetime.datetime(2021,8,24,12,0,1)


    filename=keyword+str(tr)+"trend.pkl"

    if os.path.exists(filename)==True:
        F = open(filename,'rb')
        E = pickle.load(F)
        F.close()
        return E
    else:
        print("File of currency trend is not exist")
        exit()


k=keyword[2]


for tr in trls:
    # print(getpkl("bitcoin",7)[-1][0])
    pkl=getpkl(k,tr)
    # print(pkl)
    time.sleep(4)
    count=0
    for i in range(len(pkl)-1,len(pkl)-101,-1):
        tag=getpkl(k,tr)[i][0]
        model.find_important_twitter_past(k,tag,str(tr))
        count+=1
        if count>=100:
            break