def get_def(name):
	p = name.split(".")
	
	m = None
	for n in range(-1, -len(p), -1):
		mod = ".".join(p[:n])
		try:
			m = __import__(mod)
			if m is not None:
				break
		except: pass
	assert(m is not None)

	for c in p[1:]:
		m = getattr(m, c)
	return m

