from app import db
from app.lib.nlp.tfidf import *

def search(query):
    videos = db.get_videos()
    transcripts = [ elem['transcript'] for elem in videos ]
    ranked_ts = TFIDF(transcripts).query(query, sort=True)
    ranked_vs = [ videos[i] for i, sim in ranked_ts ]
    return ranked_vs