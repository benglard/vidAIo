from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, abort

from app import db

mod_home = Blueprint('home',  __name__, url_prefix='')

@mod_home.route('/', methods=['GET'])
def home():
    return render_template('home.html', videos=db.get_videos())

@mod_home.route('/video/', methods=['GET'])
def video():
    return render_template('video.html', title='Your Video', 
        video=request.args.get('url', None))