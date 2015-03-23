#def parser(file):



def FindOutport(postcard):  #for every postcard
    #rule = findRule(SwitchID(postcard),RuleID(postcard)) #interface from probe engine
    rule = {"id" : 0, "sid":1,"priority" : 65, "dstport": 2, "actions" : ["srcport:1","fwd:4"]}
    outstr = rule["actions"][1]
    outport = int(outstr[4:])
    return outport

def getpid(postcard):
    return postcard["pid"]

def SwitchID(postcard):
    tag = postcard["mpls"]
    tag = tag >> 12
    sid = (tag >> 2) & 3
    return sid

def RuleID(postcard):
    tag = postcard["mpls"]
    tag = tag >> 12
    rid = tag >> 4
    return rid
    
def GetMatrix(postcard):# iterate for every postcard
    global matrix
    pid = getpid(postcard)  #interface from injector
    portid = FindOutport(postcard)
    sid = SwitchID(postcard)
    matrix.setdefault(pid, [-1, -1, -1])
    matrix[pid][sid] = portid
    return None

def FindRange(postcard):  ## for every postcard
    global pktrange
    sid = SwitchID(postcard)
    rid = RuleID(postcard)
    pid = getpid(postcard)
    pktrange[sid].setdefault(rid,[])
    pktrange[sid][rid].append(pid)
    return None

def sendToPostcardProcessor(rid, sid):
    global path
    global pktrange
    pktarray = pktrange[rid][sid]
    p = []
    for i in pktarray:
        p.append(path[i])
    return p


def FindPath(topo, matrix):
    path = {}
    pid = 0
    l = len(matrix)
    while pid < l:
        ports = matrix[pid]
        path_nodes = []
        single_path = []
        for i in range(0,3):
            if ports[i] != -1:
                path_nodes.append(i)
        for i in path_nodes:
            outport = ports[i]
            for j in path_nodes:
                if j != i:
                    if topo[i][j] == outport:
                        if not i in single_path:
                            if not j in single_path:
                                single_path.append(i)
                                single_path.append(j)
                            else:
                                single_path.insert(0,i)
                        elif not j in single_path:
                            single_path.append(j)
        path[pid] = single_path
        pid = pid + 1
    return path

#post_array = [{"mpls":0,"pid":0},{"mpls":4,"pid":1},{"mpls":8,"pid":2}]


pktrange = {}
for i in range(0,3):
    pktrange[i] = {}
matrix = {0:[2,3,2],1:[-1,1,1],2:[1,1,1]}
#for i in post_array:
#GetMatrix(postcard)
#FindRange(postcard)
topo = [[-1,2,-1],[1,-1,3],[-1,1,-1]] # need to be modified
print "topo:"
for i in topo:
    print i
print "matrix:"
for m in matrix:
    print m,matrix[m]
path = FindPath(topo,matrix)
print "path:"
for p in path:
    print p,path[p]
#print "pktrange:"
#print pktrange

