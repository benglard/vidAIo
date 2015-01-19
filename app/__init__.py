from flask import Flask, render_template
app = Flask(__name__)
app.config.from_object('config')
app.secret_key = '\xfc}\xadg\xcc\xd2\x80\x1eB2\xf8\x0bu\xea!\x8dm%\xd2\xe3\xbf~*Y'

from app.lib.db.mongo import MongoDB
db = MongoDB()

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from app.api.home   import mod_home   as home_module
from app.api.upload import mod_upload as upload_module
from app.api.search import mod_search as search_module

app.register_blueprint(home_module)
app.register_blueprint(upload_module)
app.register_blueprint(search_module)