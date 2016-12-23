import sys

def write_item(item, out = sys.stdout):
    print >> out, "@%s{%s," % (item.type, item.ident)
    i = 0
    keys = list(item.kv)
    while i < len(keys) - 1:
        k = keys[i]
        print >> out,"  %s=%s," % (k, item.kv[k])
        i+=1
    print >> out,"  %s=%s" % (keys[-1], item.kv[keys[-1]])
    print >> out,"}"
