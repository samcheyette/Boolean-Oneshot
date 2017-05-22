from LOTlib.Inference.Samplers.MetropolisHastings import MHSampler
from LOTlib.DataAndObjects import FunctionData
from LOTlib.Miscellaneous import logsumexp
from model import *
from clean_data import *
import time
from LOTlib.TopN import TopN
import random
from get_clean_response import *





def get_likely_hyps_enumerate(data, out_rule):

	enum = grammar.enumerate(log(samp, 2) + 1)

	lst = []
	tn=TopN(N=top)

	o_time = time.time()
	min_hd = len(out_rule)
	r_min_hd = None
	min_out = None
	st=set()

	ind=0
	while (ind < samp):

		if ind % 5000 == 0 and ind != 0:
			t_s = time.time() - o_time
			print ind, t_s, float(ind)/t_s
			print r_min_hd, min_hd
			print out_rule
			print min_out
			print len(st)
			print len(st)/(float(2**len(out_rule)))
			print len(st)/t_s
			print h0.value.count_subnodes()

			print

		fn = enum.next() 
		#print fn
		h0 = MyHypothesis(**{"sp":sp})
		fdata = copy.deepcopy([FunctionData(input=data, output=out_rule, 
						alpha=alpha) ])
		h0.set_value(fn)
		post = h0.compute_posterior(fdata)
		lik = h0.likelihood
		out= h0(data)
		hd = hamming_distance(out, out_rule)

		#lst.append((copy.deepcopy(h0), post))
		tn.add(h0)



		if hd < min_hd:
			min_hd = hd
			r_min_hd = copy.deepcopy(h0)
			min_out = copy.deepcopy(out)
		int_v = int(eval("0b" + "".join([str(i) for i in out])))
		st.add(int_v)
		ind=ind+1

	lst = [(h, h.posterior_score) for h in tn.get_all(sorted=True)]

	z = logsumexp([x[1] for x in lst])
	pp = ([(tup[0], exp(tup[1] - z), tup[0].value.count_subnodes()) for 
	    tup in lst])
	sorted_scores = sorted(pp, key=lambda tup: 1 - tup[1])

	return copy.deepcopy(sorted_scores)



def run_model(data, rule):


	print data
	print "******"
	print

	best_hyps = get_likely_hyps_enumerate(data, rule)

	all_best = []

	for hs in best_hyps[:5]:
		gen = hs[0](get_all_stimuli(nfeat))
		print hs, hamming_distance(hs[0](data), rule)
		print hs[0](data)
		print rule
		print gen
		print sum(gen)
		print

	return best_hyps
	#print

	#value_hyps = get_value(best_hyps, rewardP, rewardN)




def main_bda(out_file):
	#for alpha in [0.9999999, 0.9999, 0.99, 0.95, 0.9, 0.75, 0.6]:
	#alpha= 0.95

	c = clean("data.csv", nfeat)
	bf = bin_form(c, nfeat)
	data = get_all_stimuli(maxLen)
	grs = []


	vals = assign_vals(c, nfeat)
	resps = get_resps("data_answers.csv", nfeat)
	to_func = resps_to_func(resps, vals)
	Cont = get_all_stimuli(nfeat)


	for s in bf:

		if s['ID'] in to_func:
			tmp = []
			stim = s['stimulus']
			for d in data:
				if d in stim:
					tmp.append(1)
				else:
					tmp.append(0)


			idN = s['ID']
			f = to_func[idN]
			verbal_ans = []
			for C in Cont:
				verbal_ans.append(eval(f))

			grs.append((copy.deepcopy(s['blicket']), copy.deepcopy(tmp), 
						copy.deepcopy(verbal_ans), s['ID'],
						 s["RT_mean"], s["RT_median"]))


	random.shuffle(grs)


	print resps
	l = []
	for g in grs:
		print resps[g[3]]
		l.append((resps[g[3]].replace("not_striped", "solid"), 
					resps[g[3]].count("and") + resps[g[3]].count("or") + 1))
		print g[2]
		print g[1]
		print hamming_distance(g[2], g[1])
		print 



	true_resps = []
	model_res = []
	for gr in grs:
		best = run_model(data, gr[1])
		model_res.append((copy.deepcopy(gr[0]), 
							copy.deepcopy(gr[1]), 
							copy.deepcopy(best), 
							resps[gr[3]],
							gr[2], alpha, gr[4], gr[5]))
		#print

	#print data
	#print bf
	#run_model(data, gr)
	out = output(out_file, model_res, data, app=True)


def main_learning(out_file):
	#for alpha in [0.9999999, 0.9999, 0.99, 0.95, 0.9, 0.75, 0.6]:
	#alpha= 0.95

	c = clean("data.csv", nfeat)
	bf = bin_form(c, nfeat)
	data = get_all_stimuli(maxLen)
	grs = []


	vals = assign_vals(c, nfeat)
	resps = get_resps("data_answers.csv", nfeat)
	to_func = resps_to_func(resps, vals)
	Cont = get_all_stimuli(nfeat)


	print resps
	print bf

	grs=[]
	for b in bf:

		if b["ID"] in resps:
			#r = run_model([b["blicket"]], [1])
			r = run_model([b["blicket"]], [1])
			resp = resps[b["ID"]]
			grs.append((b["blicket"], copy.deepcopy(r),
				 alpha, b["ID"], resp))

		else:
			print 'ID NOT FOUND IN SURVEY'


	#print data
	#print bf
	#run_model(data, gr)
	out = output_learning(out_file, grs, app=True)







if __name__ == "__main__":

		#globals

	out_file = "model_output2.csv"

	alphas = [0.999999, 0.9]
	#alphas = [0.9999999999]
	samp = 50000
	top = 10
	sp = False
	nfeat = 4
	for alpha in alphas:
		main_bda(out_file)
		#main_learning(out_file)