import requests
import logging
import json

class Auth(object):

    def __init__(self, username, password, instance, timeout=60, debug=False):
        self.username = username
        self.password = password
        if 'https://' in instance:
            self.instance = instance
        else:
            self.instance = 'https://%s.service-now.com/' % instance
        self.timeout = timeout
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)

    def _list(self, table, meta, metaon=None):
        query = '^'.join(['%s=%s' % (field, value) for field, value in meta.iteritems()])
        if metaon:
            query += '^' + '^'.join(['%sON%s' % (field, value) for field, value in metaon.iteritems()])
        params = {
            'JSON':             '',
            'sysparm_action':   'getKeys',
            'sysparm_query': query
        }
        return self.session.get('%s/%s' % (self.instance, table), params=params, timeout=self.timeout)

    def _list_by_query(self, table, query):
        params = {
            'JSON':             '',
            'sysparm_action':   'getKeys',
            'sysparm_query':    query
        }
        return self.session.get('%s/%s' % (self.instance, table), params=params, timeout=self.timeout)

    def _get(self, table, meta, metaon=None, displayvalue=False, displayvariables=False):
        query = '^'.join(['%s=%s' % (field, value) for field, value in meta.iteritems()])
        if metaon:
            query += '^' + '^'.join(['%sON%s' % (field, value) for field, value in metaon.iteritems()])
        params = {
            'JSON':             '',
            'sysparm_action':   'getRecords',
            'sysparm_query': query
        }
        if displayvalue:
            params['displayvalue'] = 'true'
        if displayvariables:
            params['displayvariables'] = 'true'
        return self.session.get('%s/%s' % (self.instance, table), params=params, timeout=self.timeout)

    def _get_by_query(self, table, query, displayvalue=False, displayvariables=False):
        params = {
            'JSON':             '',
            'sysparm_action':   'getRecords',
            'sysparm_query': query
        }
        if displayvalue:
            params['displayvalue'] = 'true'
        if displayvariables:
            params['displayvariables'] = 'true'
        return self.session.get('%s/%s' % (self.instance, table), params=params, timeout=self.timeout)

    def _post(self, table, data, displayvalue=False, displayvariables=False):
        params = {
            'JSON':             '',
            'sysparm_action':   'insert'
        }
        if displayvalue:
            params['displayvalue'] = 'true'
        if displayvariables:
            params['displayvariables'] = 'true'
        return self.session.post('%s/%s' % (self.instance, table), params=params, data=json.dumps(data), timeout=self.timeout)

    def _update(self, table, where, data, displayvalue=False, displayvariables=False):
        query = '^'.join(['%s=%s' % (field, value) for field, value in where.iteritems()])
        params = {
            'JSON':             '',
            'sysparm_action':   'update',
            'sysparm_query':    query
        }
        if displayvalue:
            params['displayvalue'] = 'true'
        if displayvariables:
            params['displayvariables'] = 'true'
        return self.session.post('%s/%s' % (self.instance, table), params=params, data=json.dumps(data), timeout=self.timeout)

    def _update_by_query(self, table, query, data, displayvalue=False, displayvariables=False):
        params = {
            'JSON':             '',
            'sysparm_action':   'update',
            'sysparm_query':    query
        }
        if displayvalue:
            params['displayvalue'] = 'true'
        if displayvariables:
            params['displayvariables'] = 'true'
        return self.session.post('%s/%s' % (self.instance, table), params=params, data=json.dumps(data), timeout=self.timeout)

    def _delete(self, table, id, displayvalue=False, displayvariables=False):
        params = {
            'JSON':             '',
            'sysparm_action':   'deleteRecord',
            'sysparm_sys_id':    id
        }
        if displayvalue:
            params['displayvalue'] = 'true'
        if displayvariables:
            params['displayvariables'] = 'true'
        return self.session.post('%s/%s' % (self.instance, table), params=params, timeout=self.timeout)

    def _get_session(self):
        return self.session
