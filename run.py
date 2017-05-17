from LOTlib.Inference.Samplers.MetropolisHastings import MHSampler
from LOTlib.DataAndObjects import FunctionData
from LOTlib.Miscellaneous import logsumexp
from model import *
from clean_data import *
import time
from LOTlib.TopN import TopN
import random
from get_clean_response import *
import os.path



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
	while (ind < samp and (min_hd > 0 or ind < 20000)):

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
		h0 = MyHypothesis()
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
		print hs, hamming_distance(hs[0](data), rule)
		print hs[0](data)
		print rule
		print

	return best_hyps
	#print

	#value_hyps = get_value(best_hyps, rewardP, rewardN)


def output(file, model, data, app=False):

	if (not app) or (not os.path.isfile(file)):
		s = ("subj, blicket, resp, hyp, hyp_pred, prob, hamming,")
		s += "complexity, verbal, verbal_pred, alpha, time\n"
		app_use = "w+"
	else:
		s = ""
		app_use = "a+"

	subs = 0
	tm = str(time.time())
	for m in model:

		blicket = "".join(["ab"[int(i)] for i in m[0]])
		resp = "".join(["ab"[i] for i in m[1]])
		verbal_resp = m[3]
		verbal_resp_pred = "".join(["ab"[i] for i in m[4]])
		alph = str(m[5])
		for pred in m[2]:
			hyp = str(pred[0]).replace(",", "")
			hyp_pred = str("".join(["ab"[i] for i in pred[0](data)]))
			hd = str(hamming_distance(pred[0](data), m[1]))
			prob = str(round(pred[1],4))
			cplx = str(pred[2])

			print subs, blicket, resp, hyp, hyp_pred, prob, hd, cplx

			s += "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (subs, blicket, resp, hyp,
															 hyp_pred, prob, hd, cplx,verbal_resp,
															 	 verbal_resp_pred, alph, tm)

		subs += 1
		print

	f = open(file, app_use)
	f.write(s)
	f.close()




if __name__ == "__main__":

		#globals


	#for alpha in [0.9999999, 0.9999, 0.99, 0.95, 0.9, 0.75, 0.6]:
	for alpha in [0.999]:
	#alpha= 0.95
		samp = 40000
		top = 10
		nfeat = 4
		out_file = "model_output6.csv"
		c = clean("data.csv", nfeat)
		bf = bin_form(c, nfeat)
		#print data
		data = get_all_stimuli(maxLen)
		#gr = get_rule(grammar, which, data)
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
							copy.deepcopy(verbal_ans), s['ID']))


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
								gr[2], alpha))
			#print

		#print data
		#print bf
		#run_model(data, gr)
		out = output(out_file, model_res, data, app=True)



