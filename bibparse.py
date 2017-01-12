from pyparsing import *

class BibKV(object):
    def __init__(self, kv_list):
        self._ind = {}
        self._backing_list = kv_list
        for i in range(0, len(kv_list)):
            self._ind[kv_list[i][0].lower()] = i
    def __getitem__(self, key):
        key = key.lower()
        if key not in self._ind:
            raise KeyError()
        return self._kv_ref(key)[1]
    def __setitem__(self, key, value):
        key = key.lower()
        if key not in self._ind:
            raise KeyError()
        self._kv_ref(key)[1] = value
    def _kv_ref(self, key):
        return self._backing_list[self._ind[key]]
    def __contains__(self, key):
        return key.lower() in self._ind
    def __iter__(self):
        return iter([ kv[0] for kv in self._backing_list ])

class BibWrapper(object):
    def __init__(self, type, ident, kv):
        self.type = type
        self.ident = ident
        self.kv = kv
    def filter_mapping(self, l):
        new_kv = []
        for k in self.kv:
            if not l(k):
                continue
            new_kv.append([k, self.kv[k]])
        self.kv = BibKV(new_kv)

lit_open = Suppress('{')
lit_close = Suppress('}')
lit_comma = Suppress(',')
equals = Suppress('=')

no_comma = Regex(r"[^,]+")
key = Word(alphas + "_")
non_brace = Regex(r"[^{}]+")
brace_value = Forward().addParseAction(lambda s: "".join(s.asList()))
brace_delim = (Literal("{") + ZeroOrMore(brace_value) + Literal("}"))
brace_value <<= (brace_delim | non_brace)
value = brace_delim.addParseAction(lambda s: "".join(s.asList())) | no_comma

key_item = Group(key + equals + Group(value).addParseAction(lambda s: s.asList()[0]))

key_item_list = Group(delimitedList(key_item, delim=',') + Optional(Suppress(",")))

type_start = Suppress("@") + non_brace

bib_item = Group(type_start + lit_open + no_comma + lit_comma + key_item_list + lit_close)

items = OneOrMore(bib_item) + StringEnd()

def parse_items(blob):
    return [ BibWrapper(item[0], item[1], BibKV(item[2])) for item in  \
             items.parseString(blob).asList() ]
