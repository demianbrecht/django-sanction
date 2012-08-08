# vim: ts=4 sw=4 et:

from gzip import GzipFile
from StringIO import StringIO
from urlparse import parse_qsl


def parse_url(data):
	return dict(parse_qsl(data))


def gunzip(data):
    s = StringIO(data)
    gz = GzipFile(fileobj=s, mode="rb")
    return gz.read()

