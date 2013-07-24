import sys
syspath = sys.path
syspath.append('/'.join(syspath[0].split('/')[:-1]))

from base.retrospect import get_source_code
import SimpleHTTPServer

src = get_source_code(SimpleHTTPServer)
print '-' * 100
print src
f = open('SimpleHTTPServer_src.py', 'w')
f.write(src)
f.close()
print '-' * 100
