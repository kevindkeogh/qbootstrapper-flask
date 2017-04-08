from setuptools import setup

setup(
        name='qbflask',
        packages=['qbflask'],
        include_package_data=True,
        install_requires=[
            'flask',
            'qbootstrapper',
        ],
     )

