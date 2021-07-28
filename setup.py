from setuptools import setup, find_packages

setup(
    name='SHOOT',
    version='0.3.5',
    long_description=__doc__,
    packages=['shootbio'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask', 'ete3', 'six', 'numpy', 'biopython']
)
