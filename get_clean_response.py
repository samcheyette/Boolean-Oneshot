import string
import copy
from helpers import get_all_stimuli

from clean_data import *
from model import *

def get_resps(file,  nfeat):
	f = open(file, "r")
	l = f.readline()
	p_dct = {}
	while l != "":
		r =  l.split(",")
		l =f.readline()

		if ("Resp" in r[3]) and ('deb' not in r[0]):
			#print r
			p_dct[r[0]] = r[5]

	return p_dct



def resps_to_func(resps, vals):
	all_resps = {}
	for r in resps:
		resp = resps[r]
		strped = resp.split(" ")
		new_strped = []
		for k in xrange(len(strped)):
			if k % 2 == 0:
				tmp = ""
				for v in xrange(len(vals)):
					if strped[k] in vals[v]:
						tmp += "x_(C[%s])" % v
						if vals[v][strped[k]] == '0':
							tmp = "not__(%s)" % tmp
			else:
				tmp = strped[k]

			new_strped.append(tmp)

		strped_str = ""
		if len(new_strped) > 1:
			assert(len(new_strped) != 2)
			strped_str += "%s__(%s, %s)" % (new_strped[1], new_strped[0], new_strped[2])
			for s in xrange(3, len(new_strped), 2):
				strped_str = "%s__(%s, %s)" % (new_strped[s], new_strped[s+1], strped_str)

		else:
			strped_str += new_strped[0]


		all_resps[r] = strped_str

	return all_resps






if __name__ == "__main__":
	nfeat = 4
	c = clean("data.csv", nfeat)
	#bf = bin_form(c, nfeat)

	vals = assign_vals(c, nfeat)
	resps = get_resps("data_answers.csv", nfeat)
	to_func = resps_to_func(resps, vals)
	Cont = get_all_stimuli(nfeat)



	for idN in to_func:
		f = to_func[idN]
		print f
		for C in Cont:
			print eval(f)



	#bf = bin_form(c, nfeat)




	#print c

