import os
import unittest
from os import path

base_path = path.dirname(path.realpath(__file__))
cfg_path = path.join(base_path, 'config', 'testing.py')
os.environ['TODO_SETTINGS'] = cfg_path

import server


class TodoTestCase(unittest.TestCase):

    def test_config_settings(self):
        config = server.app.config
        assert config['DATABASE'] == 'sqlite:///test.db'
        assert config['TESTING']
        assert config['DEBUG']


if __name__ == '__main__':
    unittest.main()
