'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
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
from bottle import request,response,redirect
import uuid


# Initialise our views, all arguments are defaults for the template

SESSION_EXPIRATION_TIME = datetime.timedelta(minutes=30)



page_view = view.View()
if os.path.exists("./temp.db")==False:
    database = sql.SQLDatabase("./temp.db")
    database.database_setup()
else:
    database = sql.SQLDatabase("./temp.db")








def home(username="",recommend_type_for_user=""):

    username=username
    
    
    # Modify here to generate string in html format can be then be upload
    #  
    recommend_type_for_user=recommend_type_for_user
    print("A")
    return page_view("home",username=username,recommend_game_of_certain_type=recommend_type_for_user)



def recommend_game_of_certain_type(username,gametype):

    # Based on username, generate recommend game type and game in each type


    # Define a Python dictionary
    dat=[]

    if username=="harry" and gametype=="ACT":
        dat = [
            {
                "rank": "1",
                "name": "Dark Soul 3",
                "description": "Hard game",
                "pop":"90",
                "url":"https://google.com"
            },
            {
                "rank": "2",
                "name": "Dark soul 2",
                "description": "Another Hard game",
                "pop":"60",
                "url":"https://google.com"
            },
            {
                "rank": "3",
                "name": "Dark soul 1",
                "description": "Very Hard game",
                "pop":"30",
                "url":"https://google.com"
            }

        ]


    # Convert the Python dictionary to a JSON object
    dat2 = json.dumps(dat)


    return dat2




def registerpage():
    return page_view("register")




def register(username,password):
    database.add_u(username,password)


    return page_view("home")




def update_session_expiry_time(session_id):
    current_time = datetime.datetime.now()

    # Calculate the new expiry time based on the session expiration time
    expiry_time = current_time + SESSION_EXPIRATION_TIME

    # Update the session data in the session data store with the new expiry time
    session_data = database.retrieve_session_data(session_id)
    session_data['expiry_time'] = expiry_time.strftime('%Y-%m-%d %H:%M:%S')
    database.update_session_data(session_id, session_data)



def is_valid_session():
    # Check if the session ID is present in the session cookie
    session_id = request.get_cookie('session_id')
    print(session_id)
    if session_id==None:
        print("sessionid not exist")
        return False

    # Retrieve the session data from the session data store
    session_data = database.retrieve_session_data(session_id)

    # Check if the session data exists
    
    print(session_data)
    
    if not session_data:

        return False

    # Check if the session has expired
    session_expiry_time = session_data.get('expiry_time')
    session_expiry_time= datetime.datetime.strptime(session_expiry_time, '%Y-%m-%d %H:%M:%S')



    if session_expiry_time and session_expiry_time < datetime.datetime.now():
        # Remove the expired session from the session data store
        database.remove_session_data(session_id)
        return False

    # If the session is valid, update the expiry time
    update_session_expiry_time(session_id)

    # Return True to indicate that the session is valid
    return True



def loginpage():

    if is_valid_session():
        print("already sign in")
        redirect("/home")

    return page_view("login")



def login(username,password):

    # check login
    result=database.get_u(username,password)

    if result!=False:
        # print("Result")
        print("Find user:{} , hash value:{} ".format(result[0],result[1]))

        session_id = str(uuid.uuid4())
        
        username=result[0]

        expiry_time= datetime.datetime.now()+SESSION_EXPIRATION_TIME
        expiry_time= expiry_time.strftime('%Y-%m-%d %H:%M:%S')


        print(expiry_time)

        # Store the session ID in a session cookie
        response.set_cookie('session_id', session_id, path='/')

        database.remove_session_data_by_username(username)
        database.add_session(session_id,username,expiry_time)
        print(database.retrieve_session_data(session_id))
        print("here")
        # redirect("/home?param1=value1&param2=value2")
        redirect("/home")
    else:
        print("Not found")
        redirect("/login")

    # return page_view("home")














# def geteveryday(begin,end):
#     datels=[]
#     begin=datetime.datetime.strptime(begin,"%Y-%m-%d")
#     end=datetime.datetime.strptime(end,"%Y-%m-%d")
#     while begin<=end:
#         datestr=begin.strftime("%Y-%m-%d")
#         datels.append(datestr)
#         begin+=datetime.timedelta(days=1)
#     return datels



# def all_file_name(file_dir):   
#     for roots,dir,files in os.walk(file_dir):  
#         # print(roots,dir,files) #当前目录路径
#         return files 


# def find_id(id,user_dir):
#     for roots,dir,files in os.walk(user_dir):
#         for f in files:
#             if f==id:
#                 return True
#     return False 


# def change_time_format(tweettime):
#     tweettime=tweettime.split(' ')
#     datetime_object = datetime.datetime.strptime(tweettime[1], "%b")
#     month = int(datetime_object.month)
#     day=int(tweettime[2])
#     year=int(tweettime[5])
#     hour,minute,second=tweettime[3].split(":")
#     hour=int(hour)
#     minute=int(minute)
#     second=int(second)
#     return datetime.datetime(year,month,day,hour,minute,second)





# #This function create the file if not existed. Return the file for research. The file is a dictionary containing all the hashtag and the count
# def get_trend_past(keyword,tr):
#     # print(tr)



#     # print(datetime.datetime(2021,8,19,0,0,0)<datetime.datetime(2021,8,24,0,0,0))
#     # timelimit=datetime.datetime(2021,8,19,0,0,0)
#     if str(tr)=="168":
#         # timelimit=datetime.datetime(2021,8,19,0,0,1)
#         tr="168"
#     if str(tr)=="24":
#         # timelimit=datetime.datetime(2021,8,24,0,0,1)
#         tr="24"
#     if str(tr)=="12":
#         # timelimit=datetime.datetime(2021,8,24,12,0,1)
#         tr="12"

#     filename="tweet/TweetScraper/Data/hashtag_rank/"+keyword+"_"+str(tr)+"_"+"tagrank.pkl"
#     # print(filename)
#     # print(os.path.exists(filename))

#     if os.path.exists(filename)==True:
#         F = open(filename,'rb')
#         E = pickle.load(F)
#         # print(E)
#         F.close()
#         return E


#     # tweet_dir="tweet"+keyword+"819-825/"
#     # ls=all_file_name(tweet_dir)
#     # lastlen=len(ls)
#     # # print(ls[0])
#     # count=0


#     # arr={}

#     # for tweetname in ls:
#     #     file_name=tweet_dir+tweetname
#     #     f = open(file_name)
#     #     # #将json格式的数据映射成list的形式
#     #     t = json.load(f)

#     #     time=t['raw_data'].get('created_at')
#     #     time=change_time_format(time)
#     #     # print(time<datetime.datetime(2021,8,24,12,0,1))
#     #     if time>timelimit:
#     #         print(time)
#     #         print(timelimit)
#     #         hashtags=[]
#     #         for element in t['raw_data']['entities']['hashtags']:
#     #             # print(element['text'])
#     #             hashtags.append(element['text'])
#     #             try:
#     #                 arr[element['text']]+=1
#     #             except:
#     #                 arr[element['text']]=1
#     #         # print(t['id_'])
#     #         # print(t['raw_data'].get('created_at'))
#     #         # print(t['raw_data'].get('full_text'))
#     #         # print(hashtags)
#     #         # print(t['raw_data'].get('retweet_count'))
#     #         # print(t['raw_data'].get('favorite_count'))
#     #         # print(t['raw_data'].get('reply_count'))
#     #         # print(t['raw_data'].get('quote_count'))
#     #         # print(t['raw_data'])




#     #         # time=t['raw_data'].get('created_at')
#     #         # print(change_time_format(time))
#     #         # time=change_time_format(time)
#     #         # print(time)
#     #         # if time>=timelimit:
#     #             # print(time)
#     #             # print(count)
#     #             # print(hashtags)
#     #             # print(database.add_tweet(t['id_'],time,t['raw_data'].get('full_text'),hashtags,t['raw_data'].get('retweet_count'),t['raw_data'].get('favorite_count'),t['raw_data'].get('reply_count'),t['raw_data'].get('quote_count'),t['raw_data'].get('user_id'),t['raw_data']))
#     #         count+=1
#     #         print(count)
#     #     f.close()

#     # # print(arr['Bitcoin'])
#     # # print(arr['BTC'])
#     # result= sorted(arr.items(), key = lambda kv:(kv[1], kv[0])) 
#     # print(result)


#     # filename=keyword+str(tr)+"trend.pkl"
#     # F = open(filename,'wb')
#     # pickle.dump(result,F)
#     # F.close()
#     # return result





# # def find_name_follower(id,worldtrend):
# #     user_dir="tweet/TweetScraper/Data/Data/user/"
# #     ls=all_file_name(user_dir)
# #     lastlen=len(ls)
# #     dictname={}
# #     dictfollower={}
# #     dictscreenname={}
# #     for userid in id.values():
# #         # if userid=="617853906":
# #         #     print("fffffffffffffffffffffffff")
# #         # print(userid)
# #         file_name=user_dir+str(userid[0])
# #         f = open(file_name)
# #         # #将json格式的数据映射成list的形式
# #         t = json.load(f)
# #         # print(t['raw_data']['name'],t['raw_data']['followers_count'])
# #         dictname[userid[1]]=t['raw_data']['name']
# #         dictfollower[userid[1]]=t['raw_data']['followers_count']
# #         dictscreenname[userid[1]]=t['raw_data']['screen_name']
# #         f.close()
# #         # print(t['raw_data']['screen_name'])
# #     # print(len(dictfollower.keys()))
# #     # print(len(dictname.keys()))
# #     # print("inside!!!:"+str(len(id.keys()))) 
# #     return (dictname,dictfollower,dictscreenname)




# # def find_important_twitter_past(worldtrend,tag,tr):
# #     #world trend is cryptocurrency

# #     print(tr)
# #     # return
# #     timelimit=datetime.datetime(2021,8,19,0,0,0)
# #     if tr=="7":
# #         timelimit=datetime.datetime(2021,8,19,0,0,1)
# #     if tr=="24":
# #         timelimit=datetime.datetime(2021,8,24,0,0,1)
# #     if tr=="12":
# #         timelimit=datetime.datetime(2021,8,24,12,0,1)
# #     # print(worldtrend)

# #     tweet_dir="tweet/TweetScraper/Data/Data/partition/"+worldtrend.lower()+"/"
# #     last7day=[]
# #     today = datetime.date.today()
# #     for d in geteveryday((today-datetime.timedelta(days=7)).strftime("%Y-%m-%d"),(today-datetime.timedelta(days=1)).strftime("%Y-%m-%d")):
# #         last7day.append(d)

# #     ls=[]
# #     temp=[]
# #     if str(tr)=="7":
# #         for d in last7day:
# #             temp=temp+all_file_name(tweet_dir+d+"/")
# #             for l in range(len(temp)):
# #                 temp[l]=tweet_dir+d+"/"+temp[l]
# #             ls=ls+temp
# #             temp=[]
# #     else:
# #         ls=all_file_name(tweet_dir+last7day[-1]+"/")
# #         for l in range(len(ls)):
# #             ls[l]=tweet_dir+last7day[-1]+"/"+ls[l]
# #     # print(ls)
# #     lastlen=len(ls)
# #     # print(ls[0])
# #     count=0

# #     dictretweet={}
# #     dictfav={}
# #     dictreply={}
# #     dicttext={}
# #     dictuserid={}
# #     dictuserid2={}
# #     dictscreenname={}
# #     dicttime={}
# #     # ret=[]
# #     count=0

# #     for tweetname in ls:
# #         file_name=tweetname
# #         print(tweetname)
# #         f = open(file_name)
# #         # #将json格式的数据映射成list的形式
# #         t = json.load(f)

# #         ti=t['raw_data'].get('created_at')
# #         ti=change_time_format(ti)
# #         # print(time<datetime.datetime(2021,8,24,12,0,1))
# #         count+=1
# #         # if count==10000:
# #         #     break
# #         if ti>timelimit:
# #             # print(count)
# #             for j in t['raw_data']['entities']['hashtags']:
# #                 if tag==j['text']:
# #                     # print(t['id_'])
# #                     dictretweet[t['id_']]=t['raw_data'].get('retweet_count')
# #                     dictfav[t['id_']]=t['raw_data'].get('favorite_count')
# #                     dictreply[t['id_']]=t['raw_data'].get('reply_count')
# #                     dicttext[t['id_']]=t['raw_data'].get('full_text')
# #                     dictuserid[t['id_']]=(t['raw_data'].get('user_id'),t['id_'])
# #                     dicttime[t['id_']]=change_time_format(t['raw_data'].get('created_at'))
# #                     # dictuserid[t['raw_data'].get('user_id')]=t['id_']
# #                     # time.sleep(1)
# #                     if(len(dictuserid.keys())!=len(dictretweet.keys())):
# #                         print(len(dictuserid.keys()))
# #                         print(len(dictretweet.keys()))
# #                         print(t['id_'])
# #                         return
# #         f.close()

# #     result1= sorted(dictretweet.items(), key = lambda kv:(kv[1], kv[0])) 
# #     result2= sorted(dictfav.items(), key = lambda kv:(kv[1], kv[0])) 
# #     result3= sorted(dictreply.items(), key = lambda kv:(kv[1], kv[0])) 
# #     result4= sorted(dictuserid.items(), key = lambda kv:(kv[1], kv[0])) 

# #     result56=find_name_follower(dictuserid,worldtrend.lower())
# #     # print(len(result1),len(result2),len(result3),len(result4),len(result56))
# #     result5= sorted(result56[0].items(), key = lambda kv:(kv[1], kv[0])) 
# #     result6= sorted(result56[1].items(), key = lambda kv:(kv[1], kv[0]))
# #     # print(len(result1),len(result2),len(result3),len(result4),len(result5),len(result6))
# #     # print(result56[1])
# #     # return None
# #     finalresult=[]
# #     finalresult.append(dictretweet)
# #     finalresult.append(dictfav)
# #     finalresult.append(dictreply)
# #     finalresult.append(dicttext)
# #     finalresult.append(dictuserid)
# #     finalresult.append(result56[0])
# #     #format twitter id/ username
# #     finalresult.append(result56[1])
# #     #format twitter id/ follower
    



# #     dicteffect={}


# #     for id in list(finalresult[0].keys()):
# #         dicteffect[id]=math.log(float(finalresult[0][id])+0.0001)*1.2+math.log((finalresult[1][id])+0.0001)*0.8+math.log(float(finalresult[2][id])+0.0001)*1.5+math.log(float(finalresult[6][id])+0.0001)
# #     finalresult.append(dicteffect)



# #     finalresult.append(result56[2])
# #     #format twitter id/ screenname

# #     finalresult.append(dicttime)
# #     #format twitter id/ twitter created time

# #     if os.path.exists("tweet/TweetScraper/Data/populartweet/")==False:
# #         os.makedirs("tweet/TweetScraper/Data/populartweet/")
# #     preprocessname="tweet/TweetScraper/Data/populartweet/"+worldtrend+"_"+tag+"_"+tr
    
# #     if os.path.exists(preprocessname)==False:
# #         F = open(preprocessname,'wb')
# #         pickle.dump(finalresult,F)
# #         F.close()
# #     print("here")
# #     return finalresult

# #     # dictretweet
# #     # dictfav
# #     # dictreply
# #     # dicttext
# #     # dictuserid
# #     # dictusername
# #     # dictuserfollower
# #     # dicteffect
# #     # dictscreenname
# #     # dicttime

















# # def old_populartweet(worldtrend,tag,tr):
# #     '''
# #         index
# #         Returns the view for the index
# #     '''
# #     # result contains below 8 elements
# #     # dictretweet 0
# #     # dictfav 1
# #     # dictreply 2
# #     # dicttext 3 
# #     # dictuserid 4
# #     # dictusername 5 
# #     # dictuserfollower 6
# #     # dicteffect 7
# #     # dictscreenname 8
# #     # dicttime 9
# #     # print(tag)

# #     if str(tr)=="24h":
# #         tr="24"
# #     if str(tr)=="12h":
# #         tr="12"
# #     if str(tr)=="7day":
# #         tr="7"
# #     preprocessname="tweet/TweetScraper/Data/populartweet/"+worldtrend.lower()+"_"+str(tag)+"_"+str(tr)
# #     print(preprocessname)
# #     print(os.path.exists(preprocessname))
# #     # time.sleep(2)
# #     if os.path.exists(preprocessname):
# #         # print(preprocessname)
# #         F = open(preprocessname,'rb')
# #         result = pickle.load(F)
# #         F.close()
# #         # time.sleep(10)
# #     else:
# #         # print("not find!")
# #         exit()
# #         result=find_important_twitter_past(worldtrend,tag,tr)
# #     #above take too long time
# #     print("stop")
# #     # time.sleep(10)
# #     rankscorels=result[7]
# #     rankscorels=sorted(rankscorels.items(), key = lambda kv:(kv[1], kv[0]),reverse = True) 
# #     # print(rankscorels[:10])

# #     #Filter repeat author
# #     appearauthor=[]
# #     dat=""
# #     max=100
# #     i=0


# #     while i <max and i<len(rankscorels)-1:
# #         i+=1

# #         # try:
# #         #     a=(result[5])
# #         # except:
# #         #     print("1")
# #         # try:
# #         #     b=(result[5][rankscorels[i]])
# #         # except:
            
# #         #     print(len(rankscorels))
# #         #     print(i,max)
# #         #     print(rankscorels[i])
# #         #     # print(result[5])
# #         #     print("2")
        
        

# #         if (result[5][rankscorels[i][0]]) in appearauthor:
# #             max+=1
# #             continue
# #         else:
# #             appearauthor.append(result[5][rankscorels[i][0]])
# #             print(result[3][rankscorels[i][0]])
# #             print(result[1][rankscorels[i][0]])
# #             print(result[2][rankscorels[i][0]])
# #             print(result[0][rankscorels[i][0]])
# #             print(rankscorels[i][1])
# #             print(result[5][rankscorels[i][0]])
# #             print(result[4][rankscorels[i][0]])
# #             print(result[8][rankscorels[i][0]])
# #             print(result[9][rankscorels[i][0]])
# #             text=str(result[3][rankscorels[i][0]])
# #             text=text.replace("\n","<br>")
# #             #Lost time
# #             # text="aaaaaaaaaaaaaaaa"
# #             dat=dat+"<tr>"
# #             dat=dat+"<td><a href='"+"https://twitter.com/"+str(result[8][rankscorels[i][0]])+"/status/"+str(rankscorels[i][0])+"'>"+text+"</a></td>"
# #             dat=dat+"<td>"+str(result[1][rankscorels[i][0]])+"</td>"
# #             dat=dat+"<td>"+str(result[2][rankscorels[i][0]])+"</td>"
# #             dat=dat+"<td>"+str(result[0][rankscorels[i][0]])+"</td>"
# #             dat=dat+"<td>"+str(rankscorels[i][1])+"</td>"
# #             dat=dat+"<td><a href='"+"https://twitter.com/"+str(result[8][rankscorels[i][0]])+"'>"+str(result[5][rankscorels[i][0]])+"</td>"
# #             dat=dat+"<td>"+str(result[9][rankscorels[i][0]])+"</td>"
# #             dat=dat+"</tr>"
# #             print("----------------------------------------------------------")
    
# #     return page_view("populartweet",tag=tag,time=tr,dat=dat)





# def populartweet(worldtrend,tag,tr):
#     '''
#         index
#         Returns the view for the index
#     '''
#     # result contains below 8 elements
#     # dictretweet 0
#     # dictfav 1
#     # dictreply 2
#     # dicttext 3 
#     # dictuserid 4
#     # dictusername 5 
#     # dictuserfollower 6
#     # dicteffect 7
#     # dictscreenname 8
#     # dicttime 9
#     # print(tag)

#     if str(tr)=="24":
#         tr="24"
#     if str(tr)=="12":
#         tr="12"
#     if str(tr)=="168":
#         tr="168"


#     preprocessname="tweet/TweetScraper/Data/populartweet/"+worldtrend.lower()+"_"+str(tag)+"_"+str(tr)
#     print(preprocessname)
#     print(os.path.exists(preprocessname))
#     # time.sleep(2)
#     if os.path.exists(preprocessname):
#         # print(preprocessname)
#         F = open(preprocessname,'rb')
#         result = pickle.load(F)
#         F.close()
#         # time.sleep(10)
#     else:
#         # print("not find!")
#         exit()
#         # result=find_important_twitter_past(worldtrend,tag,tr)


#     rankscorels=result[7]
#     rankscorels=sorted(rankscorels.items(), key = lambda kv:(kv[1], kv[0]),reverse = True) 
#     # print(rankscorels[:10])

#     #Filter repeat author
#     appearauthor=[]
#     dat=""
#     max=100
#     i=0


#     #dict item

#     tweetjson=[]

#     while i <max and i<len(rankscorels)-1:
#         i+=1


        
        

#         if (result[5][rankscorels[i][0]]) in appearauthor:
#             max+=1
#             continue
#         else:
#             appearauthor.append(result[5][rankscorels[i][0]])
#             # print(result[3][rankscorels[i][0]])
#             # print(result[1][rankscorels[i][0]])
#             # print(result[2][rankscorels[i][0]])
#             # print(result[0][rankscorels[i][0]])
#             # print(rankscorels[i][1])
#             # print(result[5][rankscorels[i][0]])
#             # print(result[4][rankscorels[i][0]])
#             # print(result[8][rankscorels[i][0]])
#             # print(result[9][rankscorels[i][0]])
#             # print(result[7])

#             # [rankscorels[i][0]] is the id of tweet

#             j={}
#             j['content']=str(result[3][rankscorels[i][0]])
#             j['contLink']="https://twitter.com/"+str(result[8][rankscorels[i][0]])+"/status/"+str(rankscorels[i][0])
#             j['authorlink']="https://twitter.com/"+str(result[8][rankscorels[i][0]])
#             j['like']=str(result[1][rankscorels[i][0]])
#             j['comment']=str(result[2][rankscorels[i][0]])
#             j['retweet']=str(result[0][rankscorels[i][0]])
#             j['pop']=str(result[7][rankscorels[i][0]])
#             j['author']=str(result[5][rankscorels[i][0]])
#             j['time']=str(result[9][rankscorels[i][0]])
#             tweetjson.append(j)


#     tweetjson=json.dumps(tweetjson)

#     return page_view("populartweet v2",trendtable=tweetjson)
#     # return tweetjson






# # def old_hashtagtrend(l,tag,tr):
# #     '''
# #         Returns the hashtag rank related to a cryptocurrency
# #     '''

# #     if tr=="7":
# #         # timelimit=datetime.datetime(2021,8,19,0,0,1)
# #         tr="7d"
# #     if tr=="24":
# #         # timelimit=datetime.datetime(2021,8,24,0,0,1)
# #         tr="24h"
# #     if tr=="12":
# #         # timelimit=datetime.datetime(2021,8,24,12,0,1)
# #         tr="12h"


# #     # print(l)
# #     l=int(l)
    

# #     #below is a cryptocurrency name
# #     keyword=tag.lower()
# #     # print(keyword)
    
    



# #     result=get_trend_past(keyword,tr)
# #     total_amount=result[2]

# #     # print(result[-l:])
# #     trendhtml=""
# #     for i in range(0,l):
# #         # print(i)
# #         print(result)
# #         amount=result[1][i][1]
# #         popularity=amount/total_amount
# #         popularity = "%.2f%%" % (popularity * 100)
# #         hashtag=result[1][i][0]
# #         trendhtml=trendhtml+"<tr>"
# #         trendhtml=trendhtml+"<td>"+str(i+1)+"</td>"
# #         trendhtml=trendhtml+"<td><a href='/populartweet?worldtrend="+str(tag)+"&tag="+str(hashtag)+"&time="+str(tr)+"'>"+hashtag+"</a></td>"
# #         trendhtml=trendhtml+"<td>"+str(amount)+"</td>"
# #         trendhtml=trendhtml+"<td>"+str(popularity)+"</td>"
# #     # getCookie("https://0.0.0.0")
# #     return page_view("hashtagtrend",trendtable=trendhtml)







# def hashtagtrend(l,tag,tr):
#     '''
#         Returns the hashtag rank related to a cryptocurrency
#     '''

#     if tr=="168":
#         # timelimit=datetime.datetime(2021,8,19,0,0,1)
#         tr="168"
#     if tr=="24":
#         # timelimit=datetime.datetime(2021,8,24,0,0,1)
#         tr="24"
#     if tr=="12":
#         # timelimit=datetime.datetime(2021,8,24,12,0,1)
#         tr="12"


#     print(l)
#     l=int(l)
    

#     #below is a cryptocurrency name
#     keyword=tag.lower()
#     # print(keyword)
    
    



#     result=get_trend_past(keyword,tr)
#     total_amount=result[2]


#     trendjson=[]
#     for i in range(0,l):
#         # print(i)
#         j={}

#         # print(result)
#         amount=result[1][i][1]
#         popularity=amount/total_amount
#         popularity = "%.2f%%" % (popularity * 100)
#         hashtag=result[1][i][0]


#         j['rank']=str(i+1)
#         j['name']=str(hashtag)
#         j['amount']=str(amount)
#         j['pop']=str(popularity)
#         j['link']="./populartweet?worldtrend="+str(tag)+"&tag="+str(hashtag)+"&time="+str(tr)
#         # jj=json.dumps(j)
#         # print(jj)
#         trendjson.append(j)
#         # trendhtml=trendhtml+"<tr>"
#         # trendhtml=trendhtml+"<td>"+str(i+1)+"</td>"
#         # trendhtml=trendhtml+"<td><a href='/populartweet?worldtrend="+str(tag)+"&tag="+str(hashtag)+"&time="+str(tr)+"'>"+hashtag+"</a></td>"
#         # trendhtml=trendhtml+"<td>"+str(amount)+"</td>"
#         # trendhtml=trendhtml+"<td>"+str(popularity)+"</td>"
#     # getCookie("https://0.0.0.0")
#     print(trendjson)
#     trendjson=json.dumps(trendjson)
#     print(trendjson)
#     # return page_view("newhashtagtrend",trendtable=trendjson)
#     return trendjson














# def result(currency,tr,searchword):
#     print(tr)
#     keyword=currency.lower()
#     print(searchword)
#     # tweet_dir="tweet/TweetScraper/Data/hashtag_rank/"+keyword+"_"+str(tr)+"_"+"tagrank.pkl"
#     # ls=all_file_name(tweet_dir)

#     # total_amount=len(ls)
    

#     result=get_trend_past(keyword,tr)
#     print(result)
#     total_amount=result[2]
#     displays="Not find this tag"
#     for i in range(0,len(result[1])):
#         if result[1][i][0]==searchword:
#             amount=result[1][i][1]
#             popularity=amount/total_amount
#             popularity = "%.2f%%" % (popularity * 100)
#             displays="Rank:"+str(i+1)+"<br>Amount:"+str(amount)+"<br>Popularity:"+str(popularity)
#             break
#     return page_view("result",result=displays)




# def pricegraph(t):


#     if t=="60":
#         filename="bitcoin_2_month_prediction"
#         if os.path.exists(filename)==True:
#             F = open(filename,'rb')
#             E = pickle.load(F)
#             F.close()
#             result=E
#         else:
#             result=[[]*4]

#         # result.append(timeseries[:60])
#         # result.append(ty)
#         # result.append(py)
#         # result.append(previousdayprice)
#         print(result)
#         labels=result[0]
#         # print(labels)
#         x=result[1]
#         print(x)
#         x2=result[2]
#         x3=result[3]


#         script="<script>"+\
#             "const labels = "+str(labels)+";"+\
#             "var x="+str(x)+";"+\
#             "var x2="+str(x2)+";"+\
#             "var x3="+str(x3)+";"+\
#             "const data2 = { labels: labels, datasets: ["+\
#             "{ label: 'Today Bitcoin price', backgroundColor: 'rgb(255, 99, 132)', borderColor: 'rgb(255, 99, 132)', data: x, },"+\
#             "{ label: 'Today Bitcoin price prediction', backgroundColor: 'rgb(54, 162, 235)', borderColor: 'rgb(54, 162, 235)', data: x2, },"+\
#             "{ label: 'Previous day price', backgroundColor: 'rgb(154, 255, 0)', borderColor: 'rgb(154, 255, 0)', data: x3, },"+\
#             "] };"+\
#             "const config = { type: 'line', data: data2, options: {} };"+\
#             "var myChart = new Chart(document.getElementById('myChart'), config);"+"</script>"
#     elif t=="24":
#         filename="bitcoin_2_month_hourly_prediction"
#         if os.path.exists(filename)==True:
#             F = open(filename,'rb')
#             E = pickle.load(F)
#             F.close()
#             result=E
#         else:
#             result=[[]*4]

#         # result.append(timeseries[:60])
#         # result.append(ty)
#         # result.append(py)
#         # result.append(previousdayprice)
        
#         labels=result[0][-24:]
#         # print(len(result[0]))
#         # print(labels)
#         x=result[1][-24:]
#         print(len(x),len(labels))
#         x2=result[2][-24:]
#         x3=result[3][-24:]
#         print(x,x2,x3,labels)

#         script="<script>"+\
#             "const labels = "+str(labels)+";"+\
#             "var x="+str(x)+";"+\
#             "var x2="+str(x2)+";"+\
#             "var x3="+str(x3)+";"+\
#             "const data2 = { labels: labels, datasets: ["+\
#             "{ label: 'Today Bitcoin price', backgroundColor: 'rgb(255, 99, 132)', borderColor: 'rgb(255, 99, 132)', data: x, },"+\
#             "{ label: 'Today Bitcoin price prediction', backgroundColor: 'rgb(54, 162, 235)', borderColor: 'rgb(54, 162, 235)', data: x2, },"+\
#             "{ label: 'Previous day price', backgroundColor: 'rgb(154, 255, 0)', borderColor: 'rgb(154, 255, 0)', data: x3, },"+\
#             "] };"+\
#             "const config = { type: 'line', data: data2, options: {} };"+\
#             "var myChart = new Chart(document.getElementById('myChart'), config);"+"</script>"
#     return page_view("pricegraph",myscript=script)




# def showtrend(keyword):
#     return page_view("hashtagtrend",trendtable="ff")
























































