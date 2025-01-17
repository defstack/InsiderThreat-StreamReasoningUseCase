# background.py
import os,sys,datetime
from globals import *
path = '../data-r6.2/'

def decoyFileToRDF():
    f = open(path+'decoy_file.csv')
    outfile = open('background/decoy.nt','w')
    f.readline()
    for record in f:
        record = record.strip().split(',')
        filename = record[0].replace('\\','_')
        print >>outfile, '<%s%s> <%s> <%sDecoyFile>.' %(ex,filename,a,ex)
        print >>outfile, '<%s%s> <%sisIn> <%s%s>.' %(ex,filename,ex,ex,record[1])
    f.close()
    outfile.close()

# employee_name,user_id,email,role,projects,business_unit,functional_unit,department,team,supervisor
#      0,          1,     2,   3,    4,         5,              6,            7,      8,    9
def ldapToRDF():
    fileList = os.listdir(path+'LDAP/')
    for filename in fileList:
        infile = open(path+'LDAP/'+filename)
        infile.readline()
        date = filename[:filename.find('.')]
        outfile = open('background/'+date+'.nq','w')
        for record in infile:
            record = record.strip().split(',')
            print >>outfile, '<%s%s> <%shasName> <%s%s> <%s%s>.' %(ex,record[1],ex,ex,record[0].replace(' ','_'),ex,date)
            print >>outfile, '<%s%s> <%shasEmailAddress> <%s%s> <%s%s>.' %(ex,record[1],ex,ex,record[2],ex,date)
            if record[3]:
                print >>outfile, '<%s%s> <%shasRole> <%s%s> <%s%s>.' %(ex,record[1],ex,ex,record[3],ex,date)
            if record[4]:
                print >>outfile, '<%s%s> <%shasProjects> <%s%s> <%s%s>.' %(ex,record[1],ex,ex,record[4].replace(' ',''),ex,date)
            if record[5]:
                print >>outfile, '<%s%s> <%shasBussinessUnit> "%s"^^<%sstring> <%s%s>.' %(ex,record[1],ex,record[5].replace(' ',''),xsd,ex,date)
            if record[6]:
                print >>outfile, '<%s%s> <%shasFunctionalUnit> "%s"^^<%sstring> <%s%s>.' %(ex,record[1],ex,record[6].replace(' ',''),xsd,ex,date)
            if record[7]:
                print >>outfile, '<%s%s> <%shasDepartment> "%s"^^<%sstring> <%s%s>.' %(ex,record[1],ex,record[7].replace(' ',''),xsd,ex,date)
            if record[8]:
                print >>outfile, '<%s%s> <%shasTeam> "%s"^^<%sstring> <%s%s>.' %(ex,record[1],ex,record[8].replace(' ',''),xsd,ex,date)
            if record[9]:
                print >>outfile, '<%s%s> <%shasSupervisor> <%s%s> <%s%s>.' %(ex,record[1],ex,ex,record[9].replace(' ','_'),ex,date)
        infile.close()
        outfile.close()

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
    infile = open(path+'logon.csv')
    outfile = open('intermediate/PCusertimes.csv','w')
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
    infile = open(path+'logon.csv')
    outfile = open('intermediate/userPCtimes.csv','w')
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

# Annotates each pc, whether it is assigned to a user or it its a share pc.
# Output is stored in pc.nt
def PCannotation():
    # PCusertimes(10)   # comment out this line if PCusertimes.csv is already created
    infile = open('intermediate/PCusertimes.csv')
    outfile = open('background/pc.nt','w')
    for line in infile:
        line = line.strip().split(',')
        pc = line[0]
        if len(line)>1:
            userid = line[1][:line[1].find('(')]
            print >>outfile, '<%s%s> <%s> <%sAssignedPC>.' %(ex,pc,a,ex)
            print >>outfile, '<%s%s> <%shasAccessToPC> <%s%s>.' %(ex,userid,ex,ex,pc)
        else:
            print >>outfile, '<%s%s> <%s> <%sSharedPC>.' %(ex,pc,a,ex)
    infile.close()
    outfile.close()


# if __name__ == '__main__':
    # decoyFileToRDF()
    # ldapToRDF()
    # PCannotation()

    # userList = ['ACM2278','MBG3183','CDE1846','CMP2946']
    # To user getRoutineHours:
    # logonHoursDic, logoffHoursDic = getRoutineHours(userList)
    # for userID in userList:
        # print userID, 'has routine logon time:', logonHoursDic[userID]
        # print '        has routine logoff time:', logoffHoursDic[userID]

    # To user getAverageUSBUsage:
    # print getAverageUSBUsage(userList)
