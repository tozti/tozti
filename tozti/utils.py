class ResourceDef:
    def __init__(self, path, name=None):
        self._path = path
        self._name = name
        self._routes = {}
        self._prefix = ''

    def register(self, app):
        resource = app.add_resource(self._path, name=self._name)
        resource.add_prefix(self._prefix)
        for m, h in self._routes.items():
            resource.add_route(m, h)

    def get(self, handler):
        self._routes['GET'] = handler
        return handler

    def post(self, handler):
        self._routes['POST'] = handler
        return handler

    def put(self, handler):
        self._routes['PUT'] = handler
        return handler

    def patch(self, handler):
        self._routes['PATCH'] = handler
        return handler

    def delete(self, handler):
        self._routes['DELETE'] = handler
        return handler

    def head(self, handler):
        self._routes['HEAD'] = handler
        return handler

    def options(self, handler):
        self._routes['OPTIONS'] = handler
        return handler

    def any(self, handler):
        self._routes['*'] = handler
        return handler


class Router:
    def __init__(self):
        self._resources = []

    def add_resource(self, path, name=None):
        r = ResourceDef(path, name=name)
        self._resources.append(r)
        return r

    def add_prefix(self, prefix):
        for r in self._resources:
            r._prefix = prefix

    def __iter__(self):
        return iter(self._resources)
