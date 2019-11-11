def len2(x):
	if x.__class__ is str:
		return len([x])
	else:
		return len(x)

def get_meta(x):
  if has_meta(x):
  	return { z: x[z] for z in ['offset','limit','endOfRecords'] }
  else:
  	return None

def has_meta(x):
	if x.__class__ != dict:
		return False
	else:
		tmp = [y in x.keys() for y in ['offset','limit','endOfRecords']]
		return True in tmp

