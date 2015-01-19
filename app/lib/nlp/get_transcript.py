from app.lib.process import *
from os.path import splitext
from app.lib.nlp.get_duration import *
import urllib2, json

def get_transcript(filename):
    URL = 'https://www.google.com/speech-api/v2/recognize?output=json&lang=en-us&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw&client=chromium'
    HEADERS = {'Content-type': 'audio/l16; rate=16000'}
    FFMPEG = '/opt/local/bin/ffmpeg -loglevel panic'
    VID = "\"{}\"".format(filename)
    name, ext = splitext(filename)
    WAV = "\"{}.wav\"".format(name)

    # extract audio; convert to wav
    Process('{} -i {} -ar 16000 -acodec pcm_s16le -ac 1 {}'.format(FFMPEG, VID, WAV)).run()
    duration = get_duration(WAV)
    transcript = ''

    # google speech api can't handle audio samples greater than 1 MB I believe,
    # so use ffmpeg to break into 5 second samples, get transcript of each,
    # concatenate results
    for n in xrange(0, duration, 5):
        name = 'out{}.wav'.format(n)
        Process('{} -i {} -ss {} -t 5 {}'.format(FFMPEG, WAV, n, name)).run()
        with open(name, 'rb') as f:
            data = f.read()

        try:
            req = urllib2.Request(URL, data=data, headers=HEADERS)
            response_url = urllib2.urlopen(req)
            response_read = response_url.read()
            response_read = response_read.decode('utf-8')
            decoded = json.loads(response_read.split("\n")[1])
            transcript += decoded['result'][0]['alternative'][0]['transcript'] + '. '
        except:
            pass

        Process('rm {}'.format(name)).run()

    Process('rm {}'.format(WAV)).run()

    print transcript
    return transcript