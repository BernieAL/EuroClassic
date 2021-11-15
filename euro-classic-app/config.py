import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('mongodb+srv://admin:kirklandexpo@cluster0.7sxfp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False