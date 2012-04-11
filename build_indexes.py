#!/usr/bin/python

###
#
# This is the main code for building the indexes
# We use the code in:
#     parse_file.py
#     index_utils.py
#     crawl_directory.py
#
# after crawl_directory, have
# { file : {"proc_snip" : {proc : list_of_snippets}, "comments" : list} }
#
###

from crawl_directory import walkdirectory
from index_utils import *

def build_indexes (top):
    collected = walkdirectory(top)
    comments_by_file = { }
    indexed_comments = { }
    procedures_by_file = { }
    indexed_procedures = { }
    for file in collected:
        index_procedures_from_file(indexed_procedures, file,
                                   collected[file]["proc_snip"])
        index_file_procedures(procedures_by_file, file,
                              collected[file]["proc_snip"])
        index_comments_from_file(indexed_comments, file,
                                 collected[file]["comments"])
        index_file_comments(comments_by_file, file,
                            collected[file]["comments"])
    return comments_by_file, indexed_comments, procedures_by_file, indexed_procedures
# comments_by_file, indexed_comments, procedures_by_file, indexed_procedures =
#  build_indexes(".")
