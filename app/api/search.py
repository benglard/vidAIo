from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, abort

from app.lib.search.vid_search import search as vid_search

mod_search = Blueprint('search',  __name__, url_prefix='/search')

@mod_search.route('/', methods=['POST'])
def search():
    query = request.form.get('search-field', None)

    if not query:
        return redirect(url_for('home.home'))

    videos = vid_search(query)
    return render_template('videos.html', title='Search Results', videos=videos)