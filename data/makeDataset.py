import re

data = file('betty.txt').read()
data = re.sub(' +', ' ', data)
N = len(data)

print "letter"
print "string"
print ""

for i in xrange(0, N):
    c = data[i]
    if ord(c) > 31 and ord(c) < 127:
        print c
