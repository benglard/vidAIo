from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, abort

import os
from werkzeug.utils import secure_filename
from uuid import uuid4

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from app.lib.nlp.run_nlp import *
from app.lib.cv.run_cv import *
from app import db

mod_upload = Blueprint('upload',  __name__, url_prefix='/upload')

UPLOAD_FOLDER = './app/static/raw'
ALLOWED_EXTENSIONS = frozenset(['mp4', 'mov', 'm4v'])

AWS_ACCESS_KEY_ID = '###'
AWS_SECRET_ACCESS_KEY = '###'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@mod_upload.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # save to app/static/raw/
            filename = secure_filename(file.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)
            
            # analyze!
            nlp_data = nlp(path)
            cv_data = cv(path)

            # upload video to s3
            conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
            bucket = conn.get_bucket('project-vidaio')
            k = Key(bucket)
            name, ext = os.path.splitext(filename)
            k.key = str(uuid4()) + ext
            k.set_contents_from_filename(path)
            k.set_acl('public-read')
            url = k.generate_url(expires_in=0, query_auth=False)

            # upload thumbnail to s3
            thumb_path = 'app/static/raw/thumb.jpg'
            k2 = Key(bucket)
            k2.key = str(uuid4()) + '.jpg'
            k2.set_contents_from_filename(thumb_path)
            k2.set_acl('public-read')
            thumb_url = k2.generate_url(expires_in=0, query_auth=False)

            # put in mongodb
            insert = {}
            insert['url'] = url
            insert['thumb'] = thumb_url
            for k,v in nlp_data.iteritems():
                insert[k] = v
            for k,v in cv_data.iteritems():
                insert[k] = v
            db.new_video(insert)

            # remove from app/static/raw
            os.remove(path)
            os.remove(thumb_path)
                    
        return redirect(url_for('home.video', url=url))
    else:
        return render_template('file_upload.html', title='File Upload')