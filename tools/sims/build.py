"""Builds static/sim/*.html from tools/sims/src/*.js.
Each .js file starts with two comment lines: //TITLE: ... and //NOTE: ...
Run: python3 tools/sims/build.py"""
import glob, os, re
root = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(root, '..', '..', 'static', 'sim')
T = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="common.css"><title>{t}</title></head><body>
<h1>{t}</h1><p class="note">{n}</p>
<canvas id="c"></canvas><div class="ctl" id="k"></div><div class="read" id="r"></div>
<script src="common.js"></script><script>
{js}
</script></body></html>
'''
for p in sorted(glob.glob(os.path.join(root, 'src', '*.js'))):
    s = open(p).read()
    t = re.search(r'//TITLE: (.*)', s).group(1)
    n = re.search(r'//NOTE: (.*)', s).group(1)
    name = os.path.basename(p)[:-3]
    open(os.path.join(out, name + '.html'), 'w').write(T.format(t=t, n=n, js=s))
    print(name)
