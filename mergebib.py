from bibparse import *
from bibwrite import write_item
import sys

total_list = {}

for i in sys.argv[1:]:
    with open(i, 'r') as f:
        blob = f.read()
    print >> sys.stderr, "Parsing",i
    i_list = parse_items(blob)
    for it in i_list:
        total_list[it.ident] = it

for it in total_list.itervalues():
    write_item(it)
