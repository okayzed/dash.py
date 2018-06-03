# dashdoc webserver
# i want to be able to browse all my dash websets from the web browser?

import difflib
import sqlite3
import os

from .lib import dash2

import SimpleHTTPServer

DATA_DIR=os.path.expanduser("~/.local/share/Zeal/Zeal/docsets")
DOCSET_FILE = "Contents/Resources/docSet.dsidx"

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

def take_selection(options):
    for i, o in enumerate(options):
        docset = os.path.basename(o)
        print "%i) %s" %(i, docset)

    while True:
        opt = raw_input()
        try:
            iopt = int(opt)
            break
        except:
            print "Invalid Option", opt

    print "SELECTED", options[iopt]

    return iopt



def main():
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

    fname = dash.path_document(doc)

    browser = os.environ.get("BROWSER", "firefox")
    import subprocess
    print "OPENING", fname
    subprocess.call([browser, '%s' % fname])



    

if __name__ == "__main__":
    main()
