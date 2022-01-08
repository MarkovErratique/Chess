# -*-coding:utf8 -*
import requests, json
import os
import sys
import pickle
from datetime import datetime
#import numpy as np
import random
import re
from collections import defaultdict
from optparse import OptionParser
################################


## To download user names: https://lichess.org/api/team/candignols-elitistes/users, then a little bit of parsing is requirred
###


url = "https://www.lichess.org/api/games/user/MarkovErratique"
parser = OptionParser()
parser.add_option("--database",'-d',dest="chess_database",action="store",
		  help="file containing all games")

(options, args) = parser.parse_args()
chess_database=options.chess_database
all_users=[]
print("eval\tdate\tWhite\tBlack\tResult\tOpening\tplayer\topponent\tmove\ttime\tmoveTime\tCentipLost")

games = defaultdict(dict)

with open (chess_database,'r') as u: 
	for line in u.readlines():
		line=line.rstrip()
		if bool(re.match("\[",line)):
			line=line[1:len(line)-1]
			if bool(re.match("White ",line)):
				White=line[7:len(line)-1]
			elif bool(re.match("Black ",line)):
				Black=line[7:len(line)-1]
			elif bool(re.match("^Date",line)):
				Date=line[6:len(line)-1]
			elif bool(re.match("^Result",line)):
				Result=line[8:len(line)-1]
			elif bool(re.match("^Opening",line)):
				Opening=line[9:len(line)-1]
			elif bool(re.match("^TimeControl",line)):
				Cadence=line[13:len(line)-1]
				duration=re.sub("\+.*","",Cadence)
				inc=re.sub(".*\+","",Cadence)
#				print(duration,"\t",inc)
		elif bool(re.match("^1",line)):

			this_game=Date+"-"+"White"+"-"+Black
			if this_game in games:
				games[this_game]=games[this_game]+1
			else:
				games[this_game]=1
	#			m=re.match("\[\%eval\d+.\d+\]",line)	
				m=re.findall("\[\%eval [\-\#\d\.]+\]",line)	
				mc=re.findall("\[\%clk [\d+:]+\]",line)	
	#			m=re.findall("e",line)	
				u=1
				move=1
				timeleft_W=duration
				timeleft_B=duration
				if len(mc) == len(m)+1:
					if len(m)%2==0 :
						m.append("[%eval #1]")
					else:
						m.append("[%eval #-1]")
				elif len(mc) != len(m):
					print("#test")
				for i in range(0,len(m)):
					eva=str(m[i])
					eva=eva[6:len(eva)-1]
				
			
					timestring=mc[i]
					timestring=timestring[6:len(timestring)-1]
					pt = datetime.strptime(timestring,'%H:%M:%S')
					total_seconds = pt.second + pt.minute*60 + pt.hour*3600
					if bool(re.match(" #",eva)):
						if eva[1] == "-" or eva[2] == '-':
							eva=-60
						else:
							eva=60
					if float(eva)<(-60):
						eva=-60
					elif float(eva)>60:
						eva=60
					else:
						eva=float(eva)
					

					if i==0:
						centiPrev=eva
		
					
					if  u%2 ==1:
						move_time=int(timeleft_W)-int(total_seconds)+int(inc)
						timeleft_W=total_seconds
						centiLost=float(eva)-float(centiPrev)
						centiPrev=float(eva)
						print(str(eva),end='\t')
						print(Date+"\t"+White+"\t"+Black+"\t"+Result+"\t"+Opening,end='\t')
						print(White+"\t"+Black+"\t"+str(move)+"\t"+str(total_seconds)+"\t"+str(move_time)+"\t"+str(centiLost))
					else:
						move_time=int(timeleft_B)-int(total_seconds)+int(inc)
						timeleft_B=total_seconds
						eva=float(eva)
						centiLost=-float(eva)+float(centiPrev)
						centiPrev=float(eva)
						eva=-eva
						print(str(eva),end='\t')

						print(Date+"\t"+White+"\t"+Black+"\t"+Result+"\t"+Opening,end='\t')
						print(Black+"\t"+White+"\t"+str(move)+"\t"+str(total_seconds)+"\t"+str(move_time)+"\t"+str(centiLost))
						move=move+1

					u=u+1

			

	#

