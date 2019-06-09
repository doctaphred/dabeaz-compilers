from setuptools import find_packages, setup


# Requirements for using this library in another project.
# TODO: Is it okay to open this file here?
with open('requirements/base.in') as f:
    requirements = [line.strip() for line in f]


setup(
    name='compilers',
    version='0.0.1',
    description="Code for David Beazley's compilers course, June 2019",
    author_email='doctaphred@gmail.com',
    author='doctaphred',
    url='https://github.com/doctaphred/compilers',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=requirements,
)
