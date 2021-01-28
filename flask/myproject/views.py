from myproject import app, redd
from flask import jsonify, request, make_response
from myproject.reddit import RedditThread, RedditUser
import praw

CLIENT_ID = '2XmDNj0gkoQZZw'
CLIENT_SECRET = 'Qcs6RiZOpcWWjGK6-2yeZt5Fa5LPgQ'
REDIRECT_URI = 'http://localhost:5000/authorize_callback'

@app.route('/')
def home():
    return jsonify({
        'status' : 'success'
    })

@app.route('/init', methods=['POST'])
def initThread():
    data = request.get_json()
    threadid = data['threadid']
    subreddit = data['subreddit']
    if RedditThread.is_in(threadid):
        return jsonify({
            'status' : 'RedditThread already exists',
            'title' : RedditThread.activethreads[threadid].title
        })
    else:
        title = redd.submission(id=threadid).title
        new_reddit_thread = RedditThread(threadid,subreddit,title)
        return jsonify({
            'status' : 'New RedditThread created',
            'title' : title
        })


@app.route('/activethreads')
def activeThreads():
    return jsonify(RedditThread.all_threads())


@app.route('/getcomments', methods=['POST'])
def getComments():
    data = request.get_json()
    threadid = data['threadid']
    counter = data['counter']
    my_thread = RedditThread.findThread(threadid)

    if my_thread is not None:
        my_commentbox = my_thread.CommentBox
        comments = my_commentbox.returnComments(counter)
        if len(comments) > 0:
            counter = comments[-1]['counter']
            comments.reverse()
            return jsonify({
                'status' : 'success',
                'counter' : counter,
                'comments' : comments
            })
        else:
            return {
                'status' : 'fail',
                'counter' : counter,
                'comments' : []
            }            
    else:
        return {
            'status' : 'fail',
            'counter' : counter,
            'comments' : []
        }



#LOGINS

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        url = redd.auth.url(['identity submit read'],'...','permanent')
        return jsonify({
            'url' : url
        })


@app.route('/authorize_callback')
def authorized():

    state = request.args.get('state', '')
    code = request.args.get('code', '')


    my_instance = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     redirect_uri=REDIRECT_URI,
                     user_agent="livethreaddit by /u/iamjohnmiller")


    authorized_code = my_instance.auth.authorize(code)
    

    me = RedditUser(my_instance.user.me().name,code,my_instance,authorized_code)

    #create cookie and redirect#
    returnurl = request.cookies.get('red')
    res = make_response("")
    res.set_cookie("user", me.userhash.hexdigest(), 60*60*12)
    res.headers['location'] = returnurl
    return res, 302


@app.route('/getuser', methods=['GET','POST'])
def getUser():
    if request.method == 'POST':
        data = request.get_json()
        users = RedditUser.all_users()
        print(data)
        for user in users:
            if user.userhash.hexdigest().lower() == data['data']['hash'].lower():
                return {'username' : user.username}
        
        return {'username' : None}


@app.route('/activeusers')
def activeusers():
    users = RedditUser.all_users()
    users = [x.as_dict() for x in users]
    return {
        'data' : users
    }

@app.route('/post', methods=['POST'])
def postComment():
    if request.method=='POST':
        data = request.get_json()
        user_hash = data['hash']
        body = data['body']
        threadid = data['threadid']
        instance = RedditUser.findActiveUser(user_hash)
        mysub = instance.submission(id=threadid).reply(body)
        return mysub.id
