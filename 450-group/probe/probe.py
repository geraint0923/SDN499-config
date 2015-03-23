#!/usr/bin/python
import json
import re
import copy

# global variable initialization
rule_list = []
edge_list = []
edge_dict = {}
types = []

output_file = open("temp.txt", 'w')

def type_parse(filename):
    fileHandle = open(filename)
    types = []
    lines = fileHandle.readlines()
    for line in lines:
        reg = re.compile(r'"(.+?)"')
        types.append(reg.findall(line)[0])
    fileHandle.close()
    return types

def rule_parse(types, rule_data):
    rule_list = []
    for i in range(len(rule_data)):
        #print rule_data[i]
        rule = [] 
        for feature in types:
            if feature in rule_data[i]:
                rule.append(rule_data[i][feature])
            else:
                rule.append(-1)
        #print rule
        rule_list.append([[rule]])
    
    return rule_list
        
def createPacket(subtraction, types):
    if subtraction == None:
        return {}

    rule = subtraction[0][0]
    packet = {}
    for i in range(len(rule)):
        if rule[i] != -1:
            value = rule[i]
            packet[types[i]] = value
    return packet


def packetGeneratorHelper(rule1, header_space, pairs):
    adj_list = edge_dict[rule1]
    if not adj_list:
        return 

    for rule2 in adj_list:
        h = header_space[:]
        print "header_space = ", h
        print "rule1 = ", rule1
        print "rule2 = ", rule2
        print
        intersection = intersect_molecule(rule_list[rule1], rule_list[rule2])
        subtraction = subtraction_wrapper(intersection, h)
        
        packet = createPacket(subtraction, types)
        sendToInjector(packet)
        
        h.append(rule_list[rule1])
    
        tu = (rule1, packet)
        if tu not in pairs and packet != {}:
            pairs.append(tu)

        packetGeneratorHelper(rule2, h, pairs)

                
# if rule id goes from 0 to N, and rules are sorted according to their id, works
def packetGenerator(start_nodes):
    pairs = []
    # containg all pkt, rule paris
    for rule in start_nodes:
        header_space = []  
        adj_list = edge_dict[rule]

        # if rule has another rule to depend on
        if adj_list:
            packetGeneratorHelper(rule, header_space, pairs)
                    
        # no depend on
        else:
            subtraction = subtraction_wrapper(rule_list[rule], header_space)

            packet = createPacket(subtraction, types)
            sendToInjector(packet)
            
            tu = (rule, packet)
            if tu not in pairs and packet != {}:
                pairs.append(tu)
    
    return pairs




def edgeDictParse(edge_dict):
    start_nodes = []
    for rule in edge_dict:
        start_nodes.append(rule)
            
    for rule in edge_dict:
        adj_list = edge_dict[rule]

        for node in adj_list:
            if node in start_nodes:
                start_nodes.remove(node)

    return start_nodes

        
            
def sendToPostcardProcessor(rid,sid, num = 1000):
    pass

def sendToInjector(packet, switch_id = 1, num = 1000):
    if packet:
        output_file.write(str(packet))
        output_file.write('\n')


def include_singu(a,b):
	for i in range(0,len(a)):
		if (a[i] != b[i] and a[i] != -1):
			return False
	return True

#intersection of singu1 and singu2 
# -1 means a wildcard
def intersect_singu(a,b):
	ans = []
	for i in range(0,len(a)):
		if (a[i] == b[i]):
			ans.append(a[i])
		elif (a[i] == -1):
			ans.append(b[i])
		elif (b[i] == -1):   
			ans.append(a[i])
		else:             # a and b differing on any value domain indicates that they don't intersect
			return None
	return ans


# intersection of atom1 and atom2 : a new atom whose main area is the intersection of the two main areas 
#                                   and whose holes are old holes of atom1 and atom2 that remain in the new main area
# Potential optimization: check repetition
def intersect_atom(a,b):
	ans=[]
	domain = intersect_singu(a[0],b[0])
	if (domain == None):
		return None
	ans.append(domain)
	for i in range(1,len(a)):
		temp = intersect_singu(domain, a[i])
		if (temp != None):
			ans.append(temp)
	for i in range(1,len(b)):
		temp = intersect_singu(domain, b[i])
		if (temp != None):
			ans.append(temp)
	for i in range(1,len(ans)):
		if (ans[i] == ans[0]):
			return None
	return ans
# using '^' to represent intersect 	
# atomA ([mainA, singuA1, singuA2....])  - atomB ([mainB, singuB1, singuB2, ...] =
#  [mainA, mainA ^ mainB, singuA1, singuA2.., singuAn] +
#  [singuBi ^ mainA ^ main B, singuA1, singuA2...., singuAn]
# Reason: any hole in A will still be a hole 
#         intersection of mainA and mainB will be a new hole
#         the part of a hole in B that falls into (mainA^mainB) and doesn't intersect with any hole in A results in a concrete piece after A-B
#  always return a molecule
def subtract_atom(a,b):
	newAtom1 = []
	newDomain = intersect_singu(a[0],b[0])
	if (newDomain == None):
		return None
	for i in range(1,len(a)):
		if include_singu(a[i],newDomain):
			return None
	ans = []
	if (include_singu(newDomain,a[0]) == False):
		newAtom1.append(a[0])
		newAtom1.append(newDomain)
		for i in range(1,len(a)):
			if (include_singu(newDomain,a[i]) == False):
			#only subtract holes of A that don't fall into the new hole mainA^mainB
				newAtom1.append(a[i])      
		ans.append(newAtom1)
	for i in range(1,len(b)):
		atomMain = intersect_singu(b[i],a[0]) #b[i] is already in mainB 
		if (atomMain == None):
			continue
		newAtom = [];
		newAtom.append(atomMain)
		valid = True
		for j in range(1,len(a)):
			singu = intersect_singu(atomMain,a[j])
			if (singu != None):
				if (singu == atomMain):  
					valid = False
					break
				else:
					newAtom.append(singu)
		if (valid):
			ans.append(newAtom)
	return ans
#moleculeA @ moleculeB = atoms in A @ atoms in B
# atoms in the same molecule don't intersect

# called by new_dag_generator
def intersect_molecule(a,b):
        #print "moleculeA: "
        #print a
        #print "moleculeB: "
        #print b

	ans = []
	for atomA in a:
		for atomB in b:
			newAtom = intersect_atom(atomA, atomB)
			if (newAtom != None):
				ans.append(newAtom)
        
        #print "ans:"
        #print ans
	if (len(ans) == 0):
		return None
	else:
		return ans

	
# this is not the most efficient but the correctness can be guarenteed. 
# after A - B: all atoms in A don't intersect with any atom in B
# called by new_dag_generator.
def subtract_molecule(a,b):
        if a == None:
            return None

	ans = [copy.deepcopy(atom) for atom in a]
	cursor =0
	while (cursor < len(ans)):
		deleted = False
		for atom in b:
			temp = subtract_atom(ans[cursor],atom)
			if (temp != None):
				del ans[cursor]
				if (len(temp) == 0):  # A[cursor] is subtracted to empty
					deleted= True
					break
				ans.insert(cursor,temp[0]) # replace A[cursor] with a subtracted atom
				for i in range(1,len(temp)):
					ans.append(temp[i]) #append the rest subtracted atoms
		if (not deleted):
			cursor+=1
	if (len(ans) == 0):
		return None
	else:
		return ans

def subtraction_wrapper(intersection, header_space):
    subtraction = intersection
    if header_space == []:
        return subtraction

    for i in header_space:
        #print "i:"
        #print i
        subtraction = subtract_molecule(subtraction, i)
    return subtraction
				
#new dag generator
def new_dag_generator(rules):
	dag = []
	for i in range(len(rules)):
		match_range=copy.deepcopy(rules[i])
		if match_range == None:
			continue
		#print "loop on",i
		#print "---------------------------------"
		for j in range(i+1,len(rules)):
			#print "     and rule",j,":",rules[j]
		  if (rules[j] != None):
                        #print "rules[j]:"
                        #print rules[j]
			if intersect_molecule(match_range, rules[j])!=None:
				dag.append((i,j))
				#match_range = subtract_molecule(match_range,rules[j])
				#print "match changes to   ",match_range
				#print rules[i]
				#print rules[j]
				rules[j] = subtract_molecule(rules[j],rules[i])
				#print "rule",j,"changes to   ",rules[j]
	return dag	

# without the trailing [] at the end of my rule
def new_rule_parse(types,filename):
	fileHandle = open(filename)
	rule_pattern = re.compile(r'pattern=([\s\S]*?)action=')
	content = fileHandle.read()
	#print content
	patterns = rule_pattern.findall(content)
	#print patterns
	rules=[]
	for line in patterns:
		rule=[]
		for type in types:
			pattern = type +'=(\d+?),'
			reg = re.compile(pattern)
			value = reg.findall(line)
			if len(value)==0:
				rule.append(-1)
			else: 
				rule.append(int(value[0]))
		#print rule
		rules.append([[rule]])
	return rules				

def reFormatting():
    temp = open("temp.txt", 'r')
    lines = temp.readlines()
    #print "lines: ", lines
    
    f = open("data_to_injector.txt", 'w')

    f.write("[\n")

    count = 0
    for line in lines:
        #print "inside write"
        if count != len(lines)-1:
            f.write('\t' + line[:-1] + ',' + '\n')
        else:
            f.write('\t' + line[:-1] + '\n')
        count += 1

    f.write("]\n")
    f.close()
    temp.close()




if __name__ == "__main__":
    f = open("input.txt")
    types = type_parse("typename.txt")
    print types

    #print "len of types =", len(types)

    line_count = 1

    rule_list = []
    edge_list = []
    edge_dict = {}

    # data preparation
    while True:
        line = f.readline()
        line = line[:-1]

        if line_count == 1:
            rule_list = line.split(' ')
            rule_list = [int(i) for i in rule_list]

            for i in rule_list:
                edge_dict[i] = []

        if line_count == 2:
            edge_list = line.split(' ')

            for i in edge_list:
                i = i[1:-1]
                i = i.split(',')
                edge_dict[int(i[0])].append(int(i[1]))
    
        if len(line) == 0:
            break

        line_count += 1

    data_file = open("data.json")
    rule_data = json.load(data_file)

    rule_list = rule_parse(types, rule_data)
    #print rule_list

    start_nodes = edgeDictParse(edge_dict) 

    pairs = packetGenerator(start_nodes)

    output_file.close()

    reFormatting()

    #print rule_list
    #print edge_list
    print "edge_dict:"
    print edge_dict
    print "start_nodes:", start_nodes
    print "pairs:"
    print pairs
    f.close()
    data_file.close()


