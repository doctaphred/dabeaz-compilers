from setuptools import find_packages, setup


# Requirements for using this library in another project.
requirements = [
    'sly>=0.3',
]


# Requirements for developing this project.
requirements_dev = [
    'flake8==3.7.7',
    'pytest==4.6.2',
]


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
    extras_require={
        'dev': requirements_dev,
    },
)
