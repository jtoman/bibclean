import yaml, os.path, sys, re
from bibparse import parse_items
from bibwrite import write_item

data_dir = os.path.join(os.path.realpath(os.path.dirname(sys.argv[0])), "data")

def load_data_blob(f_name):
    with open(os.path.join(data_dir, f_name), 'r') as f:
        return yaml.load(f)

stopwords = [ re.compile(patt, re.I) for patt in load_data_blob("stopwords.yml") ]
whitelist = dict([ (k,set(v)) for (k,v) in load_data_blob("whitelist.yml").iteritems() ])
conf_abbrv = load_data_blob("pl-conf.yml")

if sys.argv[1] == '-':
    blob = sys.stdin.read()
else:
    with open(sys.argv[1], 'r') as f:
        blob = f.read()

bib_items = parse_items(blob)

def filter_kv(item):
    allowed_keys = whitelist[item.type]
    item.filter_mapping(lambda k: k in allowed_keys)

def matches_stopwords(item):
    if "booktitle" not in item.kv:
        return False
    val = item.kv["booktitle"]
    for stopword in stopwords:
        if stopword.search(val):
            return True
    return False

def replace_acronym(item):
    if "booktitle" not in item.kv:
        return
    booktitle = item.kv["booktitle"]
    for (k,v) in conf_abbrv.iteritems():
        if re.search(k, booktitle, re.I):
            booktitle = "{" + v + "}"
            break
    item.kv["booktitle"] = booktitle

for item in bib_items:
    if item.type in whitelist:
        filter_kv(item)
    if ("booktitle" in item.kv and item.kv["booktitle"] == "{ACM SIGPLAN Notices}") or \
       ("journal" in item.kv and item.kv["journal"] == "{ACM SIGPLAN Notices}"):
        print >> sys.stderr, "Need conference version of",item.ident
    if not matches_stopwords(item):
        replace_acronym(item)

out = sys.stdout
if len(sys.argv) > 2:
    out = open(sys.argv[2],'w')

for item in bib_items:
    write_item(item, out)
