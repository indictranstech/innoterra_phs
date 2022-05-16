from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in innoterra_phs/__init__.py
from innoterra_phs import __version__ as version

setup(
	name="innoterra_phs",
	version=version,
	description="phs customization",
	author="Indictranstech",
	author_email="nilima.d@indictranstech.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
