###############################################################
#### SIMPLE GRAMMAR PARSING
###############################################################
def parse_cnf(file):
    #lines = [line.strip() for line in file]
    lines = []
    for line in file:
        lines.append(line.strip())
    G = {}
    valid = True

    R = [_f for _f in lines[0].split(" ") if _f]
    for line in lines[1:]:
        if line.strip() != "":
            l, r, valid = parse_rule(line)

            if valid == True:
                if not l in list(G.keys()):
                    G[l] = []
                G[l] = G[l] + r

    Gt = filter_dict(G, 1)
    GT = filter_dict(G, 2)

    #check if we have rules for the start symbols
    for r in R:
        if not r in list(GT.keys()):
            print(("Grammar invalid. Not found rule for the start symbol '%s'"%r))
            valid = False


    return (R, list(G.keys()), find_terminals(G), Gt, GT, valid)

def filter_dict(d, l):
    r = {}
    for k, values in d.items():
        r[k] = []
        for v in values:
            if len(v) == l: 
                r[k] = r[k] + [v]

        if len(r[k]) == 0: 
            del r[k]

    return r

def parse_rule(line):
    #rule = [x.strip() for x in line.split("->")]
    rule = []
    for x in line.split("->"):
        rule.append(x.strip())
    #print line
    if len(rule) != 2:
        print(("Rule no valid: " + line))
        l = None
        r = None
        valid = False
    else:
        l, r = rule
        r = [_f for _f in [x.strip().split(' ') for x in r.split(" | ")] if _f]
        valid = validate_rule(l, r, line)

    return l, r, valid

def validate_rule(l, r, rule):
    invalid = False
    if not l.isupper():
        cause = "left side must be a non terminal"
        invalid = True

    if len(r) == 0:
        cause = "right side can't be empty"
        invalid = True

    if invalid == True:
        print(("Rule no valid: %s (%s)"%(rule, cause)))

    return not invalid


def find_terminals(G):
    t = []
    for nt in list(G.keys()):
        for r in G[nt]:
            for s in r:
                if not s in list(G.keys()) and not s in t:
                    t = t + [s]

    return t
