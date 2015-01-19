import subprocess

class Process(object):

    def __init__(self, cmd):
        self.cmd = cmd
        print cmd
        
    def run(self):
        subprocess.call(self.cmd, shell=True)