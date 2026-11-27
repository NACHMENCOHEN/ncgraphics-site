import json,sys
T=float(sys.argv[1]) if len(sys.argv)>1 else 12
d=open('week.json').read()
s=open('template.html').read().replace('__DATA__',d).replace('__TOTAL__',str(T))
open('frame.html','w').write(s)
