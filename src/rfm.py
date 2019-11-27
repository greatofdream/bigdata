#! /usr/bin/python3
import re

def extractHeader(sqlFile):
   fsql = open(sqlFile)
   regexString = r"'(.*)'"
   name = []
   store = []
   for line in fsql:
      if re.search(r'\(', line):
         beginFlag = 1
      elif re.search(r'\)', line):
         beginFlag = 0
      if beginFlag ==1:
         matchObj =re.search(regexString, line)
         if matchObj:
            name.append(matchObj.group(1))
      else:
         matchObj =re.search(regexString, line)
         if matchObj:
            store.append({matchObj.group(1): name})
            name =[]
   return store
