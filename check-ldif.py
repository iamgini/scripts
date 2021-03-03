import os
from datetime import datetime
dateTimeObj = datetime.now()
#import pandas as pd

old_openldap_ldif = '20210225.ldif'
new_rhds_ldif = 'complete-directory-new.ldif'

group_dn_counter = 0
gid_count = 0
gid_name_count = 0
dict_group = { }
dict_user = {}

with open(new_rhds_ldif,mode='r') as varfile:
  found_group_dn = False
  group_dn_count = 0
  found_people_dn = False
  people_dn_count = 0
  gidNumber = ""
  group_name = ""
  user_name = ""
  uidNumber = ""
  uid_count = 0
  uname_count = 0

  for line in varfile:
    if ('dn: ' in line) and ('ou=People' not in line) and ('ou=Group' not in line):
      found_group_dn = False
      found_people_dn = False
      print ("something else")

    if ('dn: ' in line) and ('ou=People' in line):
       #reset all user values
      found_people_dn = True
      people_dn_count = people_dn_count + 1
      dict_user[people_dn_count] = { 'count': people_dn_count }   
      dict_user[people_dn_count]['type'] = "user"
      dict_user[people_dn_count] = { 'dn': line }  

      found_people_cn = False
      list_u_objectClass = []
      user_name = ""
      uidNumber = ""

      # reset group DN
      found_group_dn = False

    if ('dn: ' in line) and (('ou=Group' in line) or ('ou=group' in line)):
      #reset all group values
      found_group_dn = True
      group_dn_count = group_dn_count + 1
      dict_group[group_dn_count] = { 'count': group_dn_count }   
      dict_group[group_dn_count]['type'] = "group"   
      dict_group[group_dn_count] = { 'dn': line }  
      dict_group[group_dn_count]['memberUid'] = ""
      this_member_list = ""

      found_group_cn = False
      group_name = ""
      list_g_objectClass = []

      group_dn_counter = group_dn_counter + 1

      #reset dn people 
      found_people_dn = False
    
    # ====== extract user details ===========================
    if found_people_dn == True:
      
      if 'objectClass: ' in line:
        this_objectClass = line.split(": ")
        list_u_objectClass.append(this_objectClass)

      if 'cn: ' in line:
        #print (line)
        found_user_cn =  True
        found_cn_details = line.split(": ")
        user_name = found_cn_details[1].replace("\n", "")
        uname_count = uname_count + 1
        # print (dict_user[people_dn_count])
        dict_user[people_dn_count]["cn"] = user_name

      if 'uidNumber: ' in line:
        #print (line)
        #found_uid =  True
        found_uid_details = line.split(": ")
        uidNumber = int(found_uid_details[1].replace("\n", ""))
        dict_user[people_dn_count]["uidNumber"] = uidNumber

      if 'uid: ' in line:
        uid_data = line.split(": ")
        dict_user[people_dn_count]["uid"] = uid_data[1].replace("\n", "")

      if 'sn: ' in line:
        sn_data = line.split(": ")
        dict_user[people_dn_count]["sn"] = sn_data[1].replace("\n", "")

      if 'homeDirectory: ' in line:
        home_data = line.split(": ")
        dict_user[people_dn_count]["homeDirectory"] = home_data[1].replace("\n", "")
      
      if 'mail: ' in line:
        mail_data = line.split(": ")
        dict_user[people_dn_count]["mail"] = mail_data[1].replace("\n", "")

      if 'o: ' in line:
        o_data = line.split(": ")
        dict_user[people_dn_count]["o"] = o_data[1].replace("\n", "")

      if 'ou: ' in line:
        ou_data = line.split(": ")
        dict_user[people_dn_count]["ou"] = ou_data[1].replace("\n", "")

      if 'loginShell: ' in line:
        shell_data = line.split(": ")
        dict_user[people_dn_count]["loginShell"] = shell_data[1].replace("\n", "")
        
      if 'gidNumber: ' in line:
        gid_data = line.split(": ")
        dict_user[people_dn_count]["gidNumber"] = gid_data[1].replace("\n", "")

      if uidNumber != "" and user_name != "":
        #print (str(user_name) + "," + str(uidNumber))
        #print (this_objectClass)
        #list_g_objectClass
        aa = "b"

    # ====== extract goup details ===========================
    if found_group_dn == True:
      
      if 'memberUid: ' in line:
        get_members =  dict_group[group_dn_count]['memberUid']
        this_memberUid = line.split(": ")
        this_member_list = get_members + "," + str(this_memberUid[1].replace("\n", ""))
        dict_group[group_dn_count]['memberUid'] = this_member_list
      
      # for rhds only
      if 'uniqueMember: ' in line:
        get_members =  dict_group[group_dn_count]['memberUid']
        this_memberUid = line.split(": ")
        this_member_list = get_members + "," + str(this_memberUid[1].replace("\n", ""))
        dict_group[group_dn_count]['memberUid'] = this_member_list

      if 'cn: ' in line:
        found_cn_details = line.split(": ")
        group_name = found_cn_details[1].replace("\n", "")
        dict_group[group_dn_count]['cn'] = found_cn_details[1].replace("\n", "")

      if 'gidNumber: ' in line:
        #print (line)
        found_gid =  True
        found_gid_details = line.split(": ")
        dict_group[group_dn_count]['gidNumber'] = int(found_gid_details[1])

varfile.close() #close the file

#print ("\n\n" + str(group_dn_counter) + " / " + str(gid_count) + " / " + str(gid_name_count))

# f = open("a_ldif_user.csv", "w")
# 
# this_string = "dn,sn,cn,uid,uidNumber,gidNumber,homeDirectory,o,ou,loginShell,mail"
# f.write( "\n" + this_string )
# for key in dict_user:
#   this_string = ""
#   #print (dict_user[key]['dn'].replace("\n",""))
#   this_string = this_string + "\"" + dict_user[key]['dn'].replace("\n","") + "\""
#   if 'sn' in dict_user[key]:
#     this_string = this_string + ",\"" + dict_user[key]['sn'].replace("\n","") + "\""
#   else:
#     this_string = this_string + ",\" \""
#   if 'cn' in dict_user[key]:
#     this_string = this_string + ",\"" + dict_user[key]['cn'].replace("\n","") + "\""
#   else:
#     this_string = this_string + ",\" \""
#   if 'uid' in dict_user[key]:
#     this_string = this_string + ",\"" + dict_user[key]['uid'].replace("\n","") + "\""
#   else:
#     this_string = this_string + ",\" \""
#   if 'uidNumber' in dict_user[key]:
#     this_string = this_string + ",\"" + str(dict_user[key]['uidNumber']) + "\""
#   else:
#     this_string = this_string + ",\" \""
#   if 'gidNumber' in dict_user[key]:
#     this_string = this_string + ",\"" + str(dict_user[key]['gidNumber']) + "\""
#   else:
#     this_string = this_string + ",\" \""
#   if 'homeDirectory' in dict_user[key]:
#     this_string = this_string + ",\"" + dict_user[key]['homeDirectory'].replace("\n","") + "\""
#   else:
#     this_string = this_string + ",\" \""
#   if 'o' in dict_user[key]:
#     this_string = this_string + ",\"" + dict_user[key]['o'].replace("\n","") + "\""
#   else:
#     this_string = this_string + ",\" \""
#   if 'ou' in dict_user[key]:
#     this_string = this_string + ",\"" + dict_user[key]['ou'].replace("\n","") + "\""
#   else:
#     this_string = this_string + ",\" \""
#   if 'loginShell' in dict_user[key]:
#     this_string = this_string + ",\"" + dict_user[key]['loginShell'].replace("\n","") + "\""
#   else:
#     this_string = this_string + ",\" \""
#   if 'mail' in dict_user[key]:
#     this_string = this_string + ",\"" + dict_user[key]['mail'].replace("\n","") + "\""
#   else:
#     this_string = this_string + ",\" \""
#   
#   print (this_string)
#   f.write( "\n" + this_string )
# f.close()
# 

f = open("a_ldif_group.csv", "w")

this_string = "dn,cn,gidNumber,memberUid"
f.write( "\n" + this_string )
for key in dict_group:
  this_string = ""
  #print (dict_group[key]['dn'].replace("\n",""))
  this_string = this_string + "\"" + dict_group[key]['dn'].replace("\n","") + "\""
  if 'cn' in dict_group[key]:
    this_string = this_string + ",\"" + dict_group[key]['cn'].replace("\n","") + "\""
  else:
    this_string = this_string + ",\" \""
  if 'gidNumber' in dict_group[key]:
    this_string = this_string + ",\"" + str(dict_group[key]['gidNumber']) + "\""
  else:
    this_string = this_string + ",\" \""
  if 'memberUid' in dict_group[key]:
    this_string = this_string + ",\"" + dict_group[key]['memberUid'].replace("\n","") + "\""
  else:
    this_string = this_string + ",\" \""
  
  print (this_string)
  f.write( "\n" + this_string )
f.close()
