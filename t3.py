import sys
import datetime

class Logger(object):
    def __init__(self, filename='./logs/t3.log', stream1=sys.stdout,stream2=sys.stderr):
        self.terminal = stream1
        self.termina2 = stream2
        self.log = open(filename, 'a', encoding="utf-8")
        
    def write(self, message):
        self.terminal.write(message)
        self.termina2.write(message)
        self.log.write(message)

    def flush(self):
        pass


sys.stdout = Logger(stream1=sys.stdout)
sys.stderr = Logger(stream2=sys.stderr)

# now it works
print(str(datetime.datetime.now()))
