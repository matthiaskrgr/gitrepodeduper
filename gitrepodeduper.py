#!/usr/bin/env python3

#    gitrepodeduper - finds identical files in git repositorys which then can be passed to duperemove
#    Copyright (C) 2016  Matthias Krüger

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 1, or (at your option)
#    any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA  02110-1301 USA


# USAGE:  gitrepodeduper  | duperemove -rh -

import sys
if (sys.version_info.major != 3): # no python 3
	print("Python 3 or higher is required.")
	sys.exit(1)

import subprocess


# shell:
# git ls-files  -s  | cut -d' ' -f2 | sort -n | uniq -c | sort -n 
rawhashlist = subprocess.Popen(["git", "ls-files", "-s"], stdout=subprocess.PIPE).communicate()[0].decode("utf-8").replace('\t',' ').split("\n")

hashlist= []
for index, line in enumerate(rawhashlist): # list into sublist with words

	if line == "":
		continue

	splitline = line.split()
	hashlist.append([splitline[1], splitline[3]]) #new list [hash, filename]

hashlist.sort() #sort by hash

# walk through list, add dupes to todedupe list
todedupe = []
prev = 0
cur = 1
while (cur < len(hashlist)):
	if (hashlist[cur][0] == hashlist[prev][0]): # current and previous hashes are identical, assume identical file
		todedupe.append(hashlist[cur][1]) # add both entrys to the list
		todedupe.append(hashlist[prev][1])
	prev = cur
	cur += 1

todedupe = set(todedupe) # remove duplicate entrys (filenames)

for i in todedupe: # print the files
	print(i)

# TODO: call duperemove with this

