#!/usr/bin/python

def PostCardGen(rule):
    global vn
    rid = rule["id"]
    sid = rule["sid"]
    if vn[sid]:
        if rid< len(vn[sid]):
            vn[sid][rid]= vn[sid][rid] + 1
        else:
            vn[sid].append(0)
    else:
        vn[sid].append(0)

    print vn
    global portarray
    tag = (rid << 4) + (sid << 2 ) + vn[sid][rid]
    rule["actions"].append("push_mpls:0x8847")
    rule["actions"].append("set_mpls_label:" + str(tag))
    rule["actions"].append("output:" + str(portarray[sid]))
    return rule

vn = [[],[],[]]
portarray = [3,4,3]
row = 3
'''for i in range(0,row):
    vn.append([])'''
rule = {"id" : 0, "sid":1,"priority" : 65, "dstport": 2, "actions" : ["srcport:1,fwd:4"]}
print rule
print PostCardGen(rule)



    
    
