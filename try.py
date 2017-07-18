from Xmlmc import MethodCall
from Xmlmc import EspSession

m = MethodCall()
m.param('userId', 'admin').param('password', '')

session = EspSession('192.168.1.120')
session.request(m)

m = MethodCall('data', 'sqlQuery')
m.database('swdata').query('select callref from opencall limit 5')

response = session.request(m)

print response

'''
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
'''

m = MethodCall('session', 'analystLogoff')
response = session.request(m)
