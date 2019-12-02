from __future__ import unicode_literals

from mopidy_transistor import Extension


def test_get_default_config():
    ext = Extension()

    config = ext.get_default_config()

    assert "[transistor]" in config
    assert "enabled = true" in config

    assert "serial_port = /dev/ttyUSB0" in config
    assert "serial_baudrate = 115200" in config
    assert "podcasts_timeout = 5" in config
    assert "noise_folder = " in config
    assert "config_file = " in config
    assert "user = " in config
    assert "passwd =" in config


def test_get_config_schema():
    ext = Extension()

    schema = ext.get_config_schema()

    assert "serial_port" in schema
    assert "serial_baudrate" in schema
    assert "podcasts_timeout" in schema
    assert "noise_folder" in schema
    assert "config_file" in schema
    assert "user" in schema
    assert "passwd" in schema


# TODO Write more tests
