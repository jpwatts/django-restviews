"""RESTful Views for Django"""

from django import http


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

    When called, dispatch based on the value of ``request.method``.  If
    there isn't a handler for the method, return an HTTP 405.

    >>> class View(Resource):
    ...     def DELETE(self, request):
    ...         return http.HttpResponse('', status=204)
    ...
    ...     def GET(self, request):
    ...         return http.HttpResponse('Resource')

    >>> request = http.HttpRequest()
    >>> view = View()

    >>> request.method = 'DELETE'
    >>> response = view(request)
    >>> response.content
    ''
    >>> response.status_code
    204

    >>> request.method = 'GET'
    >>> response = view(request)
    >>> response.content
    'Resource'
    >>> response.status_code
    200

    >>> request.method = 'PUT'
    >>> response = view(request)
    >>> response.content
    ''
    >>> response.status_code
    405
    >>> response['Allow']
    'DELETE, GET'

    """
    __metaclass__ = ResourceBase

    def __call__(self, request, *args, **kwargs):
        if request.method not in self.allow:
            return http.HttpResponseNotAllowed(self.allow)
        return getattr(self, request.method)(request, *args, **kwargs)
