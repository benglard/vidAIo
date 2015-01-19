import subprocess, re

def get_duration(sound):
    print 'Finding duration of {}'.format(sound)

    find_duration = re.compile('.*Duration: ([0-9:]+)', re.MULTILINE)

    cmd = '/opt/local/bin/ffmpeg -i {}; exit 0'.format(sound)
    print cmd
    ffmpeg = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

    match = find_duration.search(ffmpeg)
    if match: 
        ffmpeg = match.group(1)
    else: 
        ffmpeg = '--'

    length = ffmpeg.lstrip('0:')
    time = length.split(':')

    if len(time) == 2:
        min, sec = time
    else:
        min, sec = 0, time[0]

    duration = 60 * int(min) + int(sec) + 1

    return duration