#!/usr/bin/python

###
#
# The goal here is to learn what procedures are defined in a python file
#
###

from sys import argv
from sys import exit

def help_not_in_string_literal(s, char, 
                               pos):
    occ = s.find(char,pos)
    if (occ == -1):
        return -1
    single = s.find("'",pos)
    double = s.find('"',pos)
    if (single == -1 and double == -1):
        return occ
    if (single == -1):  # must be double quoted
        quotechar = '"'
        start = double
    elif (double == -1): # must be single quoted
        quotechar = "'"
        start = single
    elif (single < double): # double quote is in the single-quoted string
        quotechar = "'"
        start = single
    else: # single quote is in the double-quoted string
        quotechar = '"'
        start = double
    if (occ < start):
        return occ
    stop = s.find(quotechar,start+1)
    return help_not_in_string_literal(s,char,stop+1)

def find_not_in_string_literal(s, char):
    if (not char in s):
        return -1
    return help_not_in_string_literal(s,char,0)

def parse_line_for_procedure(line):
    sl = line.split()
    if (len(sl) == 0 or sl[0] != "def"):
        return None
    return sl[1].split("(")[0]

def parse_line_for_comment(line):
    start = find_not_in_string_literal(line, "#")
    if (start == -1):
        return None
    return line[start:-1]

def procedures_in_file(filename):
    proc_snip_dict = { }
    extracting_parameters = False
    curr_snippet = ""
    curr_proc = ""
    for line in open(filename):
        p = parse_line_for_procedure(line)
        if (p):
            if not p in proc_snip_dict:
                proc_snip_dict[p] = [ ]
            if (extracting_parameters):
                print "Error: Found new procedure %s while extracting parameters of"\
                    %p
                print "%s.  Perhaps a missing :?"%curr_proc
                proc_snip_dict[curr_proc].append(curr_snippet)
                curr_snippet = ""
                extracting_parameters = False
            start = line.find("def")
            stop = find_not_in_string_literal(line,":")
            if (stop == -1):
                curr_snippet = line[start:]
                curr_proc = p
                extracting_parameters = True
            else:
                proc_snip_dict[p].append(line[start:stop])
        else:
            if extracting_parameters:
                stop = find_not_in_string_literal(line,":")
                if (stop != -1):
                    proc_snip_dict[curr_proc].append(curr_snippet+line[:stop])
                    extracting_parameters = False
                    curr_snippet = ""
                else:
                    curr_snippet = curr_snippet + line
    if (extracting_parameters):
        print "Error: File ended while extracting parameters for %s"%curr_proc

    return proc_snip_dict

def comments_in_file(filename):
    comments = []
    for line in open(filename):
        c = parse_line_for_comment(line)
        if (c):
            comments.append(c)
    return comments

if __name__ == '__main__':

    if (len(argv) == 1):
        files = [argv[0]]
    else:
        files = argv[1:]

    for file in files:
        print "\n\nAll of the procedures defined in the file", file

        proc_snip_dict = procedures_in_file(file)
        for proc in proc_snip_dict:
            print proc
            print "----"
            for snip in proc_snip_dict[proc]:
                print snip
                print "----"
            
        print "\n\nAnd now the comments"
        comments = comments_in_file(argv[0])
        for c in comments:
            print c

    exit()
