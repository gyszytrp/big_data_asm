'''
    This file will handle our typical Bottle requests and responses
    You should not have anything beyond basic page loads, handling forms and
    maybe some simple program logic
'''

from bottle import route, get,post, request, redirect ,static_file
import model
import time
from myapp import app


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
@app.route('/css/<css:path>')
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
@app.route('/js/<js:path>')
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



@app.get('/')
@app.get('/home')
@get('/')
@get('/home')
def home():

    # Handle right panel
    return model.home()
    # return static_file("hashtagtrend v2.html", root = "templates/")

@app.get('/register')
@get('/register')
def registerpage():

    return model.registerpage()


@app.post('/register')
@post('/register')
def register():
    dat=request.forms
    username=dat['name']
    password=dat['password']
    return model.register(username,password)


@app.get('/login')
@get('/login')
def loginpage():

    return model.loginpage()


@app.get('/logout')
@get('/logout')
def logoutpage():

    return model.logout()


@app.post('/login')
@post('/login')
def login():
    dat=request.forms
    username=dat['name']
    password=dat['password']


    model.login(username,password)

    


@app.get('/userprofile')
@get('/userprofile')
def userprofile():



    # cookie_value = request.get_cookie("user_name")
    # if cookie_value==None:
    #     return model.home("visitor","pass_data")
    # else:
    #     return model.home(cookie_value,"pass_data")


    return model.user_profile()


@app.post('/profile')
@post('/profile')
def get_preference_from_profile():

    # option = request.forms['option']
    # session = request.forms.get('session')


    # print(option,session)

    # print("!")

    data = request.json
    print(data) # {'name': 'John', 'age': 30}

    # then input data to model








@app.get('/recommend_game_of_certain_type')
@get('/recommend_game_of_certain_type')
def recommend_game_of_type():
    
    username=request.query.get("username")
    gametype=request.query.get("gametype")
    return model.recommend_game_of_certain_type(username,gametype)

