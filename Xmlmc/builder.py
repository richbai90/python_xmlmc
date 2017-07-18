from lxml import etree


class MethodCall(object):
    def __init__(self, service='session', method='analystLogon', root=None, params=None):
        if root is None:
            self.root = etree.Element('methodCall', service=service, method=method)
            self.params = None
        else:
            self.root = root
            self.params = params

    def __getattr__(self, name):
        def wrapper(value):
            return self.param(name, value)

        return wrapper

    def _ensure_params(self):
        if self.params is None:
            self.params = etree.SubElement(self.root, 'params')

    def param(self, param, value=None):
        self._ensure_params()
        param = etree.SubElement(self.params, param)
        if value is not None:
            param.text = value
            return MethodCall(root=self.root, params=self.params)
        return Param(root=self.root, params=self.params, lastparam=param)

    def tostring(self):
        return etree.tostring(self.root)

    def __str__(self):
        return self.tostring()

    def length(self):
        return self.tostring().length


class Param(MethodCall):
    def __init__(self, root, params, lastparam):
        super(Param, self).__init__(root=root, params=params)
        self.lastparam = lastparam

    def child(self, param, value=None):
        if value is None:
            self.lastparam = etree.SubElement(self.lastparam, param)
        else:
            param = etree.SubElement(self.lastparam, param)
            param.text = value

        return Param(self.root, self.params, self.lastparam)
