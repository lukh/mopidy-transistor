# describe what settings are allowed in the settings interface
from collections import OrderedDict

settings_conf = OrderedDict()

# settings convert passwd to new, old, repeat passwd
settings_conf["transistor"] = [("user", "string"), ("passwd", "password")]
settings_conf["proxy"] = [
    ("scheme", "string"),
    ("hostname", "string"),
    ("port", "int"),
    ("username", "string"),
    ("password", "password"),
]
settings_conf["local"] = [("media_dir", "string")]
settings_conf["file"] = [("media_dirs", "tuple")]
