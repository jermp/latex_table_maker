#!/bin/python

import sys, json
from collections import OrderedDict
from sets import Set
import argparse

parser = argparse.ArgumentParser(description = "Latex table maker")
parser.add_argument('input_filename', type = str, help = "Input json filename")
parser.add_argument('table_output_filename', type = str, help = "Output table filename (should have '.tex' as extension)")

args = parser.parse_args()

types = Set({"string", "int", "float"})

def remove_underscore(str):
    return str.replace("_", "")

def fail(type):
    print "Error: type '" + type + "' is invalid"
    print "Valid types are:",
    for t in types:
        print "'" + t + "'",
    print "\nMaybe header is missing?"
    sys.exit(1)

with open(args.input_filename) as f:

    order = {}
    parsed = json.loads(f.readline(), object_pairs_hook=OrderedDict)
    id = 0
    for p in parsed:
        type = parsed[p]
        if type not in types:
            fail(type)
        order[p] = (id, parsed[p])
        id += 1
    columns = len(order)

    # table header
    table = ""
    table += "\\begin{tabular}{" + ('r' * columns) + "}\n"
    table += "\\toprule\n"
    l = sorted(order.iteritems(), key = lambda kv: kv[1])
    for i in range(0, len(l)):
        table += remove_underscore(l[i][0])
        if i != len(l) - 1:
            table += " & "
    table += " \\\ \n"
    table += "\\midrule\n"

    # table body
    while (True):
        line = f.readline()
        if line.strip() == "":
            break
        parsed = json.loads(line)
        data = [[] for i in range(0, columns)]
        for p in parsed:
            pos = order[p][0]
            type = order[p][1]
            data[pos] = parsed[p]

            if type == "int":
                data[pos] = int(data[pos])
            elif type == "float":
                data[pos] = "{0:0.2f}".format(float(data[pos]))

        for i in range(0, len(data)):
            table += str(data[i])
            if i != len(data) - 1:
                table += " & "
        table += " \\\ \n"

# table footer
table += "\\bottomrule\n\end{tabular}"

# save the table
output = open(args.table_output_filename, "w")
output.write(table)
output.close()

# print a minimal latex document with the created table
print """\\documentclass{article}

\\usepackage{booktabs}
\\usepackage{tabularx}
\\usepackage{graphicx}

\\begin{document}

\\begin{table}[t]
\\centering
\\caption{Caption text.}
\\scalebox{0.8}{\\input{""" + args.table_output_filename + """}}
\\label{tab:label}
\\end{table}

\\end{document}"""
