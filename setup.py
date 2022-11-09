import re
from setuptools import setup

version = re.search(
	'^__version__\s*=\s*"(.*)"',
	open('maya/maya.py').read(),
	re.M
	).group(1)

#with open("README.rst", "rb") as f:
#	long_descr = f.read().decode("utf-8")
long_descr = "Zengine Plugin Build Automation Tool."

setup(
	name = "zn-maya",
	packages = ["maya"],
	entry_points = {
		"console_scripts": ['maya = maya.maya:main']
		},
	version = version,
	description = "Zengine Plugin Build Automation Tool.",
	long_description = long_descr,
	install_requires=['docopt==0.6.1',
			'requests==2.7.0']
	)