import string
import copy

def clean(file,  nfeat):
	f = open(file, "r")
	l = f.readline()
	p_dct = {}
	while l != "":
		r =  l.split(",")
		part = r[0]
		if part not in p_dct:
			p_dct[part] = {}


		lets = string.ascii_lowercase + string.ascii_uppercase
		i = 0

		for z in r[4:4+nfeat]:
			done = False
			j = 0
			while j < len(lets) and done == False:

				if lets[j] in z:
					i += 1
					done = True
				j += 1

		#yn_index = i + 1
		#RT_index = i + 2
		#yn = r[4+i+yn_index]
		#RT  = r[4+i+RT_index]

		if ((r[3].strip(" ") == "stimulus" or r[3].strip(" ") == "blicket")):
			
			yn_index = i + 1
			#print 4+yn_index
			yn = False
			if (r[3].strip(" ") == "blicket"):
				yn = True
			elif "Y" in r[4+yn_index]:
				yn = True


			if r[3].strip(" ") not in p_dct[part]:
				p_dct[part][r[3].strip(" ")] = []


			if yn:
				p_dct[part][r[3].strip(" ")].append(copy.copy([k.strip(" ") for k in r[4:4+i]]))


		l = f.readline()

	return p_dct


def get_category(resps):
	z = 0
	#for r in resps:
	#print len(resps)

def consistent_with_n(data, n=1):
	z = 0
	p = 0
	med = []
	for k in data:
		if "blicket" in data[k] and "stimulus" in data[k]:
			print "*", data[k]["blicket"][0], "*"
			blicket = data[k]["blicket"]
			in_category = get_category(data[k]["stimulus"])
			z += len(data[k]["stimulus"]) 
			p += 1
			med.append(len(data[k]["stimulus"]))
	print z/float(len(data[k]))
	print sorted(med)
	print sorted(med)[len(med)/2]
			#print k1, data[k][k1]


def assign_vals(clean_data, nfeat):
	dcts = [{} for _ in xrange(nfeat)]
	for k in clean_data:
		if 'stimulus' in clean_data[k]:
			stim = clean_data[k]['stimulus']
			bl = clean_data[k]['blicket']

			for s in stim:
				for i in xrange(len(s)):
					if s[i] not in dcts[i]:
						if len(dcts[i].keys()) == 0:
							dcts[i][s[i]] = "0"
						else:
							dcts[i][s[i]] = "1"

	return dcts


def to_bin(stims, vals):
	new_lst = []
	for stim in stims:
		tmp = ""
		for v in xrange(len(stim)):
			tmp += vals[v][stim[v]]
		new_lst.append(tmp)
	return new_lst



def bin_form(clean_data, nfeat):
	vals = assign_vals(clean_data, nfeat)

	clean_data_new = []

	for k in clean_data:
		if 'stimulus' in clean_data[k]:
			stim = clean_data[k]['stimulus']
			bl = clean_data[k]['blicket']

			bin_bl = to_bin(bl, vals)
			bin_stim = to_bin(stim, vals)

			new_dct = {}

			new_dct['stimulus'] = copy.deepcopy(bin_stim)
			new_dct['blicket'] = copy.deepcopy(bin_bl[0])
			new_dct['ID'] = k

			clean_data_new.append(copy.deepcopy(new_dct))

	return clean_data_new
			#print stim, bl
#

if __name__ == "__main__":
	nfeat = 4
	c = clean("data.csv", nfeat)
	bf = bin_form(c, nfeat)

	print c


	#print bf
	#cons = consistent_with_n(c, n=1)

