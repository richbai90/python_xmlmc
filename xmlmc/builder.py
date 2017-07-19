from lxml import etree


class MethodCall(object):
    """
    Provide an interface for generating xml requests suitable for submitting to the Supportworks API
    Every method returns self and therefore supports method chaining.
    Request parameters can be added via the param method, or by calling the parameter name as a method directly
    """

    def __init__(self, service='session', method='analystLogon', _root=None, _params=None):
        """
        Initializes the MethodCall class with a service and a method
        :param service: The service the requested method resides on, default session
        :param method: The method to call, default analystLogon
        :param _root: For use with recursive calls when complex parameters are required do not set manually,
        default None
        :param _params: For use with recursive calls when complex parameters are required do not set manually,
        default None
        """
        if _root is None:
            self.root = etree.Element('methodCall', service=service, method=method)
            self._params = None
        else:
            self.root = _root
            self._params = _params

    def __getattr__(self, name):
        def wrapper(value=None):
            return self.param(name, value)

        return wrapper

    def _ensure_params(self):
        if self._params is None:
            self._params = etree.SubElement(self.root, 'params')

    def param(self, param, value=None):
        """
        Add a parameter to the API request. Equivalent to calling MethodCall.param_name(value) where
        param_name is the name of the param you wish to set.

        This method ensures that the xml object has the required <params> element and then adds children to it.
        If no value is provided it is assumed that you want to create a sub element and will return instead of self,
        It will return a Param class allowing you to create additional sub children. If you instead want to add the
        param with an empty value, pass a blank string.

        :param param: The name of the param you wish to set
        :param value: The value of the param
        :return: self or Param as explained
        """
        self._ensure_params()
        param = etree.SubElement(self._params, param)
        if value is not None:
            param.text = value
            return MethodCall(_root=self.root, _params=self._params)
        return Param(root=self.root, params=self._params, lastparam=param)

    def tostring(self):
        """
        Returns a string representation of the MethodCall object
        :return: Xml String
        """
        return etree.tostring(self.root)

    def __str__(self):
        return self.tostring()

    def length(self):
        return self.tostring().length


class Param(MethodCall):
    """
    Provide an interface for creating more complex parameter structures. IE instead of <param>value</param>,
    this class allows the creation of
    <param>
      <sub_param>
        <sub_sub_param>value</sub_sub_param>
      </sub_param>
    </param>
    which is occasionally necessary. This class should never be instantiated explicitly but is returned implicitly
    when no value is giving for MethodCall.param this class extends MethodCall
    """

    def __init__(self, root, params, lastparam):
        """
        Initializes the param class
        :param root:
        :param params:
        :param lastparam:
        """
        super(Param, self).__init__(_root=root, _params=params)
        self.lastparam = lastparam
        self._params = params

    def __getattr__(self, name):
        def wrapper(value=None):
            return self.child(name, value)

        return wrapper

    def child(self, param, value=None):
        if value is None:
            self.lastparam = etree.SubElement(self.lastparam, param)
        else:
            param = etree.SubElement(self.lastparam, param)
            param.text = value
        return Param(self.root, self._params, self.lastparam)

    def params(self):
        return Param(self.root, self._params, self._params)