from setuptools import setup

VERSION = 0.01
LICENSE = 'MIT'


setup(
        name='qbflask',
        packages=['qbflask'],
        include_package_data=True,
        install_requires=[
            'flask',
            'qbootstrapper',
        ],
        version=VERSION,
        license=LICENSE,
     )
