from django.http import HttpResponseNotAllowed


__all__ = ['Resource']


# http://www.ietf.org/rfc/rfc2616
METHODS = """OPTIONS
             GET
             HEAD
             POST
             PUT
             DELETE
             TRACE
             CONNECT""".split()


class ResourceBase(type):
    def __new__(cls, name, bases, attrs):
        attrs['allow'] = sorted(k for k in attrs if k in METHODS)
        return super(ResourceBase, cls).__new__(cls, name, bases, attrs)


class Resource(object):
    """A base class for creating RESTful Django views.

    When called, the view checks ``request.method`` to dispatch to the
    appropriate method handler or returns an HTTP 405 if the method is
    not allowed.

    """
    __metaclass__ = ResourceBase

    def __call__(self, request, *args, **kwargs):
        if request.method not in self.allow:
            return HttpResponseNotAllowed(self.allow)
        return getattr(self, request.method)(request, *args, **kwargs)
