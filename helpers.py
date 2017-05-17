import copy

def hamming_distance(a, b):
	assert(len(a) == len(b))
	hd = 0
	for i in xrange(len(a)):
		if a[i] != b[i]:
			hd += 1

	return hd


def get_all_stimuli(length):
	if length == 0:
		return [""]

	else:
		new_lst = []
		for x in copy.deepcopy(get_all_stimuli(length - 1)):
			y1 = x + "0"
			y2 = x + "1"
			new_lst.append(y1)
			new_lst.append(y2)
		return new_lst


def complexity_penalty(constant, hyp):
	cplx = hyp.value.count_subnodes()
	return const / float(2**cplx)