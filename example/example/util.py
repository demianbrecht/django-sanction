# vim: ts=4 sw=4 et:

from urlparse import parse_qsl

def parse_url(data):
	return dict(parse_qsl(data))

