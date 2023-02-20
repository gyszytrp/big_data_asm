'''
    This file will handle our typical Bottle requests and responses
    You should not have anything beyond basic page loads, handling forms and
    maybe some simple program logic
'''

from bottle import route, get,post, request, redirect ,static_file
import model
import time
#-----------------------------------------------------------------------------
# Static file paths
#-----------------------------------------------------------------------------

# Allow image loading
@route('/img/<picture:path>')
def serve_pictures(picture):
    '''
        serve_pictures

        Serves images from static/img/

        :: picture :: A path to the requested picture

        Returns a static file object containing the requested picture
    '''
    return static_file(picture, root='static/img/')

#-----------------------------------------------------------------------------

# Allow CSS
@route('/css/<css:path>')
def serve_css(css):
    '''
        serve_css

        Serves css from static/css/

        :: css :: A path to the requested css

        Returns a static file object containing the requested css
    '''
    return static_file(css, root='static/css/')

#-----------------------------------------------------------------------------

# Allow javascript
@route('/js/<js:path>')
def serve_js(js):
    '''
        serve_js

        Serves js from static/js/

        :: js :: A path to the requested javascript

        Returns a static file object containing the requested javascript
    '''
    return static_file(js, root='static/js/')




# @get('/populartweet')
# def get_populartweet():
#     worldtrend=request.query.worldtrend
#     tag=request.query.tag
#     tr=request.query.time
#     if not worldtrend and not tr and not tag:
#         return static_file("populartweet.html", root = "templates/")
#     if not worldtrend:
#         worldtrend="bitcoin"
#     if not tag:
#         tag="bitcoin"
#     if not tr:
#         tr=168
#     return model.populartweet(worldtrend,tag,tr)


@get('/')
@get('/home')
def home():

    # Handle right panel
    return model.home("harry","abc")
    # return static_file("hashtagtrend v2.html", root = "templates/")


@get('/register')
def registerpage():

    return model.registerpage()



@post('/register')
def register():
    dat=request.forms
    username=dat['name']
    password=dat['password']
    print(username,password)
    print("tuple")
    return model.register(username,password)



@get('/login')
def loginpage():

    return model.loginpage()



@post('/login')
def login():
    dat=request.forms
    username=dat['name']
    password=dat['password']
    # print(username,password)
    # print("tuple")

    model.login(username,password)

    



@get('/userprofile')
def userprofile():

    cookie_value = request.get_cookie("user_name")
    if cookie_value==None:
        return model.home("defaultname",".....")
    else:
        return model.home("harry","abc")




# @post('/')
# @post('/home')
# def home_login():
#     return model.home("harry","a")



# Handle left panel
@get('/recommend_game_of_certain_type')
def recommend_game_of_type():
    
    username=request.query.get("username")
    gametype=request.query.get("gametype")
    return model.recommend_game_of_certain_type(username,gametype)

# @get('/trend')
# def get_hashtagtrend():
#     value = request.query.value
#     value = 10 if not value else value
#     tag=request.query.tag
#     tag = "bitcoin" if not tag else tag
#     t=request.query.time
#     t = 168 if not t else t
#     keyword=request.query.keyword
#     #when the page search the rank of certain hastag
#     if keyword!="":
#         return model.result("bitcoin",t,keyword)
        
#     return model.hashtagtrend(value,tag,t)




# @get('/pricegraph')
# def get_pricegraph():
#     t=request.query.time
#     print("timerange:{}".format(t))
#     if t=="":
#         t="60"
#     return model.pricegraph(t)





# @get('/showtrend')
# def showtrend():

#     return model.showtrend("gg")
