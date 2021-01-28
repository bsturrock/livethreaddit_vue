from myproject import redd
import threading
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import hashlib

class RedditUser(object):

    users=[]

    def __init__(self, username, code, instance, refresh):
        self.username = username
        self.userhash = hashlib.md5(username.encode('utf-8'))
        self.code = code
        self.instance = instance
        self.refresh = refresh
        self.__class__.users.append(self)

    @classmethod
    def all_users(cls):
        return cls.users

    def as_dict(self):
        return {
            'username' : self.username,
            'code' : self.code,
            'refresh' : self.refresh,
        }

    @classmethod
    def findActiveUser(cls, userhash):
        users = cls.all_users()
        for user in users:
            if user.userhash.hexdigest().lower() == userhash.lower():
                return user.instance



class ThreadManager():

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(func=self.checkLiveThreads, trigger='interval', seconds=30)
        self.scheduler.start()

    def checkLiveThreads(self):
        print('checking all live threads')
        threads = RedditThread.activethreads
        threads_to_end = []
        for key in threads.keys():
            if threads[key].CommentBox.ping == 0:
                threads[key].CommentStream.running = False
                threads_to_end.append(key)
            else:
                threads[key].CommentBox.ping = 0

        for key in threads_to_end:
            RedditThread.activethreads.pop(key)
            RedditThread.activethread_ids.remove(key)

class RedditThread(object):

    activethread_ids = []
    activethreads = {}

    def __init__(self, threadid, subreddit, title):
        self.threadid = threadid
        self.subreddit = subreddit
        self.title = title
        self.__class__.activethread_ids.append(self.threadid)
        self.__class__.activethreads[self.threadid] = self
        self.CommentBox = CommentBox(self)
        self.CommentStream = CommentStream(self.threadid, self.subreddit, self)
    
    @classmethod
    def all_threads(cls):
        threads = {}
        for key in cls.activethreads.keys():
            threads[key] = cls.activethreads[key].as_dict()
        return threads

    @classmethod
    def is_in(cls, id):
        if id in cls.activethread_ids:
            return True
        else:
            return False

    @classmethod
    def findThread(cls, id):
        try:
            return cls.activethreads[id]
        except:
            return None


    def as_dict(self):
        return {
            'threadid' : self.threadid,
            'subreddit' : self.subreddit,
            'title' : self.title,
        }

    


class CommentStream(object):

    def __init__(self, threadid, subreddit, RedditThread):
        self.threadid = threadid
        self.subreddit = subreddit
        self.RedditThread = RedditThread
        self.CommentBox = self.RedditThread.CommentBox
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
        self.counter = 0
        self.running = True
        

    def run(self):
        
        for comment in redd.subreddit(self.subreddit).stream.comments(skip_existing=True):
            if self.running:
                if comment.is_root and comment.submission.id == self.threadid:
                    new_comment = {
                        'author' : comment.author.name,
                        'body' : comment.body,
                        'root' : comment.is_root,
                        'parent' : comment.parent_id,
                        'timestamp' : datetime.utcfromtimestamp(comment.created_utc).strftime('%H:%M:%S'),
                        'id' : comment.id,
                        'counter' : self.counter
                    }
                    self.counter+=1
                    self.CommentBox.queue.append(new_comment)
            else:
                print('shutting down')
                return



class CommentBox(object):

    def __init__(self, RedditThread):
        self.queue = []
        self.RedditThread = RedditThread
        self.ping = 0

    def returnComments(self, counter):
        self.ping += 1
        self.clearQueue()
        if len(self.queue) == 0:
            return []
        elif len(self.queue) > 29:
            if counter == 0:
                return self.queue[len(self.queue)-11:len(self.queue)-1]
            return self.queue[counter:counter+30]               
        elif len(self.queue) > 19:
            if counter == 0:
                return self.queue[len(self.queue)-11:len(self.queue)-1]
            return self.queue[counter:counter+20]            
        elif len(self.queue) > 9:
            if counter == 0:
                return self.queue[len(self.queue)-11:len(self.queue)-1]
            return self.queue[counter:counter+10]
        else:
            return self.queue[counter:counter+1]

    def clearQueue(self):
        if len(self.queue) > 200:
            self.queue = self.queue[99:199]

    

