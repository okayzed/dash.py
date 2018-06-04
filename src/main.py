# dashdoc webserver
# i want to be able to browse all my dash websets from the web browser?

import difflib
import sqlite3
import os

from .lib import dash2

import SimpleHTTPServer
import subprocess
import urllib

DATA_DIR=os.path.expanduser("~/.local/share/Zeal/Zeal/docsets")
DOCSET_FILE = "Contents/Resources/docSet.dsidx"
DEFAULT_BROWSER="google-chrome"
USE_DMENU=True
DMENU="/usr/bin/dmenu"

def read_docsets():
    results = os.listdir(DATA_DIR)
    paths = []
    for r in results:
        if not r.endswith(".docset"):
            continue

        path = os.path.join(DATA_DIR, r, DOCSET_FILE)
        if not os.path.exists(path):
            continue

        paths.append(os.path.join(DATA_DIR, r))

    return paths



def list_docsets(s=None):
    docsets = read_docsets()
    if s:
        return filter(lambda d: d.lower().find(s) != -1, docsets)

    return docsets

def list_remote_docsets():
    pass

def list_unofficial_docsets():
    pass

def download_docset():
    pass

def load_docset(name):
    dash = dash2.DashDoc(name)
    return dash

def search_docsets(s, docset=None):
    docsets = read_docsets()
    for d in docsets:
        if docset and d.index(docset) == -1:
            continue

        dash = dash2.DashDoc(d)
        rows = dash.search(s)
        for row in rows:
            print d, row

if not os.path.exists(DMENU):
    print "NOT USING DMENU"
    USE_DMENU=False

def take_selection(options):
    if USE_DMENU:
        return dmenu_selection(options)

    for i, o in enumerate(options):
        docset = os.path.basename(o)
        print "%i) %s" %(i, docset)

    while True:
        opt = raw_input()
        try:
            iopt = int(opt)
            break
        except:
            return opt

    return iopt

def dmenu_selection(options):
    p = subprocess.Popen(DMENU, shell=True,
          stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)

    (child_stdin, child_stdout) = (p.stdin, p.stdout)

    stdout, stderr = p.communicate("\n".join(map(str, options)))

    if not stdout.strip():
        return -1

    try:
        return options.index(stdout.strip("\n"))
    except Exception:
        return stdout.strip()



def run_query(query, lang=None):

    if query.find("/") != -1:
        tokens = query.split("/")
        if len(tokens) > 1:
            lang = tokens[0]
            query = "/".join(tokens[1:])

    print "LANG", lang
    print "QUERY", query

    if lang:
        sets = list_docsets(lang)
    else:
        sets = read_docsets()

    if not query:
        query = "  "

    if query:
        results = []
        for docset in sets:
            ds = load_docset(docset)
            for row in ds.search(query):
                results.append((ds, row))

        query_funcs = [ a[1][0] for a in results ]
        matches = difflib.get_close_matches(query, query_funcs, n=100)

        idx = {}
        for i, q in enumerate(query_funcs):
            idx[q] = i

        sorted_rows = []
        for m in matches:
            i = idx[m]
            sorted_rows.append(results[i])

        s = take_selection(matches)
        if s == -1:
            print "NO SELECTION, EXITING"
            return

        if type(s) == int:
            doc = sorted_rows[s][1][2]
            ds = sorted_rows[s][0]


            open_doc(ds, doc)
        elif type(s) == str:
            run_query(s, lang)



def open_doc(dash, doc):
    fname = "file://%s" % dash.path_document(doc)

    browser = os.environ.get("BROWSER", DEFAULT_BROWSER)
    print "OPENING", fname
    subprocess.call([browser, fname])


def interactive_query():
    docsets = list_docsets()


    selected = take_selection(docsets)
    dash = load_docset(docsets[selected])

    query = raw_input()

    rows = dash.search(query)
    query_funcs = [ a[0] for a in rows ]

    idx = {}
    for i, q in enumerate(query_funcs):
        idx[q] = i

    matches = difflib.get_close_matches(query, query_funcs, n=100)
    print "MATCHES", matches

    sorted_rows = []
    for m in matches:
        i = idx[m]
        sorted_rows.append(rows[i])

    selected = take_selection(matches)
    name, type, doc = sorted_rows[selected]


if __name__ == "__main__":
    interactive_query()
