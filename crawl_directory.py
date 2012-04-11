#!/usr/bin/python
from os import listdir
from os import path as os_path

###
#
# Procedure for crawling the directory and adding files
# We need to parse each .py file for comments and procedures
# and add them to the right index
#
# It produces a dictionary of file names with procedures and
# comments.
#
###

from parse_file import procedures_in_file
from parse_file import comments_in_file

def walkdirectory_help(top, collected):

    for name in listdir(top):
        pathname = os_path.join(top,name)

        if os_path.isdir(pathname): # found a directory
            walkdirectory_help(pathname, collected)
        elif os_path.isfile(pathname): # found a file
            if (name[-3:] != ".py"):
                continue
            proc_snip_dict = procedures_in_file(pathname)
            comments = comments_in_file(pathname)
            if (pathname in collected):
                for proc in proc_snip_dict:
                    if proc in collected[pathname]["proc_snip"]:
                        for snip in proc_snip_dict[proc]:
                            if not snip in collected[pathname]["proc_snip"][proc]:
                                collected[pathname]["proc_snip"][proc].append(snip)
                    else:
                        collected[pathname]["proc_snip"][proc] = proc_snip_dict[proc]
                collected[pathname]["comments"] += comments
            else:
                collected[pathname] = { }
                collected[pathname]["proc_snip"] = proc_snip_dict
                collected[pathname]["comments"] = comments
        else: # unknown file type
            print "Skipping", pathname
    return

def walkdirectory(top):
    collected = { }
    walkdirectory_help(top, collected)
    return collected

