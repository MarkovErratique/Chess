# -*-coding:utf8 -*
import requests, json
import os
import sys
import pickle
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
parser.add_option("--users",'-u',dest="user_file",action="store",
		  help="file containing user names")

(options, args) = parser.parse_args()
user_file=options.user_file
all_users=[]
with open (user_file,'r') as u: 
	for user in u.readlines():
		user=user.rstrip()
		all_users.append(user)	
		url="https://www.lichess.org/api/games/user/"+user
		r = requests.get(url, params={"pgnInJson":"false", "analysed":"true", "clocks":"true", "evals":"true", "opening":"true","perfType":"classical","since":"1584261235","literate":"true"})
		r_text = r.content.decode("utf-8")
		print(r_text)


