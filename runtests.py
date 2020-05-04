import sys

import nose
import nose.config
from nose.plugins.manager import DefaultPluginManager

c = nose.config.Config()
c.plugins = DefaultPluginManager()
c.srcDirs = ["package"]
if not nose.run(config=c):
    sys.exit(1)
