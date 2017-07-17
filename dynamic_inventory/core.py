class _Config:
    def __init__(self):
        self._vars = {}

    def __getitem__(self, item):
        return self._vars[item]

    def __setitem__(self, key, value):
        if isinstance(value, (dict, list)):
            self._vars[key] = value
        else:
            self._vars[key] = str(value)


class Inventory(_Config):
    def __init__(self):
        super().__init__()
        self.groups = {}

    def _all(self):
        _all = _Group('all')
        _all._vars = self._vars
        for _group in self.groups.values():
            _all.hosts.update(_group.hosts)
        return _all

    def list(self):
        _all_group = self._all()
        _groups = {**self.groups, _all_group.name: _all_group}
        _groups_config = {
            _group_name: _group.raw() for _group_name, _group in _groups.items()
        }
        _meta_config = {'_meta': {'hostvars': {}}}

        for _group_name, _group in _groups.items():
            for _host_fqdn, _host in _group.hosts.items():
                hostvars = _meta_config['_meta']['hostvars'].setdefault(_host_fqdn, {})
                hostvars.update(_group.hosts[_host_fqdn].raw())

        return {**_groups_config, **_meta_config}

    def group(self, name):
        return self.groups.setdefault(name, _Group(name))


class _Group(_Config):
    def __init__(self, name):
        super().__init__()
        self.name  = name
        self.hosts = {}

    def raw(self):
        return {
            'hosts': list(self.hosts.keys()),
            'vars' : self._vars
        }

    def host(self, name, ansible_host, ansible_user, domain):
        fqdn = f'{name}.{domain}'
        _host = _Host(fqdn)
        _host['ansible_host'] = ansible_host
        _host['domain']       = domain
        _host['home']         = f'/home/{ansible_user}'
        _host['ansible_user'] = ansible_user
        return self.hosts.setdefault(fqdn, _host)


class _Host(_Config):
    def __init__(self, fqdn):
        super().__init__()
        self.fqdn = fqdn

    def raw(self):
        return self._vars
