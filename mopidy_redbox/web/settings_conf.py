# describe what settings are allowed in the settings interface
settings_conf = [
    # settings convert passwd to new, old, repeat passwd
    ('redbox', ['user', 'passwd']),
    ('proxy', ['scheme', 'hostname', 'port', 'username', 'password']),
    ('local', ['media_dir']),
    ('file', ['media_dirs'])
]
