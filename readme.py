"""
This is a demo of the Xmlmc SDK for python
To get started import EspSession and MethodCall
From the Xmlmc Module
"""

from Xmlmc import MethodCall
from Xmlmc import EspSession

"""
MethodCall is the interface to create requests
Behind the scenes it will generate the necessary XML
For a request. Upon initialization, MethodCall may take
Two optional named parameters: service and method.
These parameters default to session and analystLogon
To know which service and method you should use, visit <servername>:5015 for documentation.
"""

m = MethodCall()

"""
The first request you will always need to make is a logon request.
This could be a customer logon request, or an analyst logon request.
Most of the time requests will require parameters. What those parameters are
Can be found in the documentation @ http://<servername>:5015
To create those params in the request, you can use the param method of the MethodCall class
Param takes two parameters: the parameter name, and the parameter value
Any passwords sent to the API must be base64 encoded and the SDK does not do this automatically
"""

m.param('userId', 'admin').param('password', '')

"""
To submit a request you will need to create a session using the EspSession class
The EspSession class takes one required parameter: endpoint, which is the ip or fqdn of the Supportworks server
And an optional named parameter: port, which defaults to 5015
Unless you know otherwise we suggest leaving it at the default
The session will maintain your connection to the server and propagate the session cookie between requests
"""

session = EspSession('192.168.1.120')

"""
To submit the request to the server use the request method.
The request method takes as a single required parameter an instance of MethodCall
Representing the request you wish to make
"""
session.request(m)

"""
MethodCall is chainable meaning that you can chain the methods together for quicker coding
It also intercepts a call to an unknown method, shortcutting the param method.
In this case you would call MethodCall.<param_name>(<param_value>).
This is equivalent to calling MethodCall.param(<param_name>,<param_value>)
"""

m = MethodCall('data', 'sqlQuery').database('swdata').query('select callref from opencall limit 5')

"""
The request method returns a Response object which is a dictionary
Representation of the XML response. The response from the query above
Would return:

{
    'status': 'ok',
    'data': {
        'rowData': {
            'rows': [{
                'callref': '23'
            }, {
                'callref': '33'
            }, {
                'callref': '34'
            }, {
                'callref': '35'
            }, {
                'callref': '36'
            }]
        }
    },
    'params': {
        'rowsEffected': '5'
    }
}


"""

response = session.request(m)
print response

"""
Another important note is that it is imperative that you call the appropriate logoff method
After your session is done so as not to consume a license
"""

m = MethodCall('session', 'analystLogoff')
response = session.request(m)

"""
A few other notes:

In rare occasions it may be necessary to create a request with some nested xml as
Is the case with the helpdesk::addFilesToCallDiary method, the xml request for which 
Looks like this:

...
<params>
  ...
  <fileAttachment>
    <fileName>...</fileName>
    <fileData>...</fileData>
  </fileAttachment>
</params>
...

To facilitate this requirement, when MethodCall.param is called with a name parameter but no value
The SDK assumes we mean to move to the next level. This behavior is maintained until a value is provided.
Once a value is provided any param entered will be entered at that level.
To go back to the params level, you need only call the MethodCall::params method.
The same is true when calling the param method implicity by calling the param name as a method.

So for instance to achieve the above request:
"""

print MethodCall('helpdesk', 'addFilesToCallDiary') \
    .fileAttachment() \
    .fileName('FileName') \
    .fileData('base64_stuff') \
    .params() \
    .another_param('value')

# OR

print MethodCall('helpdesk', 'addFilesToCallDiaray') \
    .param('fileAttachment') \
    .param('fileName', 'FileName') \
    .param('fileData', 'base64_stuff') \
    .params() \
    .param('another_param', 'value')

