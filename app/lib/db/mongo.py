from flask.ext.pymongo import PyMongo
from app import app

class MongoDB(object):

    def __init__(self): 
        self.mongo = PyMongo(app)

    def new_video(self, obj):
        self.mongo.db.videos.save(obj)

    def get_videos(self):
        return [ elem for elem in self.mongo.db.videos.find().sort([('_id', -1)]) ]