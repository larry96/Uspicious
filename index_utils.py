#!/usr/bin/python

###
#
# Utilities for procedure and comment indexing
#
###

# {proc : list_of_snippets}
# index[procedure] = { filename : [snippet] }
def index_procedures_from_file(index, filename, proc_snippet_dict):
    for proc in proc_snippet_dict:
        if (not proc in index):
            index[proc] = { }
        if (not filename in index[proc]):
            index[proc][filename] = []
        for snip in proc_snippet_dict[proc]:
            if not snip in index[proc][filename]:
                index[proc][filename].append(snip)
    return

def index_file_procedures(index, filename, proc_snippet_dict):
    index[filename] = proc_snippet_dict
    return

# ["# comment", "##if x", ... ]
# index[word] = { filename : [line] }
def index_comments_from_file(index, filename, comments):
    for commentline in comments:
        cl = commentline[1:]
        while (len(cl) > 0 and cl[0] == "#"):
            cl = cl[1:]
        words = cl.split()
        for word in words:
            if not word in index:
                index[word] = { }
            if not filename in index[word]:
                index[word][filename] = []
            index[word][filename].append(commentline)
    return

def index_file_comments(index, filename, comments):
    index[filename] = comments
    return

def all_from_file(index, filename):
    if not filename in index:
        return None
    return index[filename]

def lookup(index, key):
    if not key in index:
        return None
    return [(filename, index[key][filename]) for filename in index[key]]

def lookup_contains(index, key_fragment):
    out = [ ]
    FRAG = key_fragment.upper()
    for key in index:
        KEY = key.upper()
        if (KEY.find(FRAG) == -1):
            continue
        out.append((key, [(filename, index[key][filename]) for filename in index[key]]))
    return out

