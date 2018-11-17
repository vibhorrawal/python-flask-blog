#Python dependencies
import datetime as dt
from subprocess import check_output as run_out

def get_next_page_or(default='main.index'):
    """
    Method to get next page to a terminating event like user login
    """    
    #Flask and it's dependencies
    from flask import request, url_for
    from werkzeug.urls import url_parse
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for(default)
    return next_page

def setup_project():
    """
    Method to setup project.
    """
    try:
        #Creating .env file
        env_data = '''FLASK_APP=project.py
SECRET_KEY=some-secret-key'''
        env_file = open('.env', 'w')
        env_file.write(env_data)
        env_data.close()
        
        #Initializing database
        run_out(["flask", "db", "migrate"], shell=True)
        run_out(["flask", "db", "migrate"], shell=True)
        run_out(["flask", "db", "upgrade"], shell=True)

        #App dependencies
        from app import db
        from app.models import User, Post, Message
        
        #Creating Test Data
        for i in range(1, 6):
            u = User(username='U{}'.format(i), email='u{}@example.com'.format(i), about_me='User U{}'.format(i))
            u.set_password('password')
            db.session.add(u)

        for i in range(1, 6):
            u = User.get_user('U{}'.format(i))
            for j in range(1, 6):
                p = Post(author=u, body='U{} post {}.'.format(i, j))
                db.session.add(p)
                time.sleep(5)
                if i != j:
                    u.follow(User.get_user('U{}'.format(j)))
                    m = Message(sender=u,
                                recipient=User.get_user('U{}'.format(j)),
                                body='U{} {} message to U{}'.format(i, j, j))
                    db.session.add(m)
                            
        db.session.commit()
    except Exception as e:
        print(e)

def format_datetime(original_time, format=''):
    time_delta = dt.datetime.utcnow() - original_time
    seconds = time_delta.seconds
    if seconds<60:
        return "few seconds ago."
    days = time_delta.days
    if format == 'from-now':
        # > 2 Year
        if days >= 730: return "{} years ago.".format(days//365)
        # 2 Year >  > 1 Year
        elif days >= 365: return "a year ago."
        # > 2 Month
        elif days >= 60: return "{} months ago.".format(days//30)
        # 2 Month >  > 1 month
        elif days >= 30: return "a month ago."
        # > 2 Weeks
        elif days >= 14: return "{} weeks ago.".format(days//7)
        # 2 Month >  > 1 month
        elif days >= 7: return "a week ago."
        # > 2 Days
        elif days >= 2: return "{} days ago.".format(days)
        # 2 Days >  > 1 Day
        elif days == 1: return "a day ago."
        # > 2 Hours
        elif seconds >= 7200: return "{} hours ago.".format(seconds//3600)
        # 2 Hour >  > 1 Hour
        elif seconds >= 3600: return "a hour ago."
        # > 2 Minutes
        elif seconds >= 120: return "{} minutes ago.".format(seconds//60)
        # 2 Minute >  > 1 Minute
        elif seconds >= 60: return "a minute ago."
        #Rest
        else: return "few seconds ago."
    else:
        pass