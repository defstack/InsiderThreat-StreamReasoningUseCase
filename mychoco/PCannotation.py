# PCannotation.py
from globals import *

# Reads logon.csv and outputs a list of PC and users in the following format:
# PC1,userid1(#uses),userid2(#uses),...
# PC2,userid3(#uses),userid4(#uses),...
# ...
# Output is stored in PCusertimes.csv
# If minUses is specified, only the users who uses the pc more than that number are output
# Otherwise minUses = 0
# PCs are output regardless if they are used by anyone more times than minUses
def PCusertimes(minUses=0):
    dic = {}
    infile = open('logon.csv')
    outfile = open('PCusertimes.csv','w')
    infile.readline()
    for line in infile:
        line = line.strip().split(',')
        userid = line[2]
        pc = line[3]
        if line[4] == 'Logon':
            if pc in dic.keys():
                if userid in dic[pc]:
                    dic[pc][userid] += 1
                else:
                    dic[pc][userid] = 1
            else:
                dic[pc] = {}
                dic[pc][userid] = 1

    for pc in dic.keys():
        outfile.write(pc)
        for userid in dic[pc].keys():
            if dic[pc][userid] > minUses:
                outfile.write(',%s(%s)'%(userid,dic[pc][userid])) # userid(times)
        outfile.write('\n')
    infile.close()
    outfile.close()

# Reads logon.csv and outputs a list of users and PCs in the following format:
# userid1,pc1(#uses),pc2(#uses),...
# userid2,pc3(#uses),pc4(#uses),...
# ...
# Output is stored in userPCtimes.csv
# If minUses is specified, only the PCs that are logged on by the user more times than minUses is output
# Otherwise minUses = 0
# userids are output regardless if they use any PC more times than minUses
def userPCtimes(minUses=0):
    dic = {}
    infile = open('logon.csv')
    outfile = open('userPCtimes.csv','w')
    infile.readline()
    for line in infile:
        line = line.strip().split(',')
        userid = line[2]
        pc = line[3]
        if line[4] == 'Logon':
            if userid in dic.keys():
                if pc in dic[userid]:
                    dic[userid][pc] += 1
                else:
                    dic[userid][pc] = 1
            else:
                dic[userid] = {}
                dic[userid][pc] = 1

    for userid in dic.keys():
        outfile.write(userid)
        for pc in dic[userid].keys():
            if dic[userid][pc] > minUses:
                outfile.write(',%s(%s)'%(pc,dic[userid][pc])) # pc(times)
        outfile.write('\n')
    infile.close()
    outfile.close()

def PCannotation():
    # PCusertimes(10)   # comment out this line if PCusertimes.csv is already created
    infile = open('PCusertimes.csv')
    for line in infile:
        line = line.strip().split(',')
        pc = line[0]
        if len(line)>1:
            userid = line[1][:line[1].find('(')]
            print '<%s%s> <%shasAccessToPC> <%s%s>.' %(ex,userid,ex,ex,pc)
        else:
            print '<%s%s> <%s> <%sSharedPC>.' %(ex,pc,a,ex)


if __name__ == '__main__':
    PCannotation()