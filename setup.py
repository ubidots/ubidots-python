from setuptools import setup, find_packages
import multiprocessing # http://bugs.python.org/issue15881#msg170215

def read_file(name):
    with open(name, "r") as f:
        return f.read()

setup(
    name='ubidots',
    version='1.6.4',
    author='Ubidots Team',
    author_email='devel@ubidots.com',
    url='https://github.com/ubidots/ubidots-python/',
    license='MIT',
    description='Api Client to connect to ubidots.com api version 1.6',
    long_description=read_file("README.rst"),
    platforms='any',
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Hardware"
    ],
    install_requires=[
        "requests >= 2.5.1",
    ],
    test_suite='nose.collector',
    tests_require=[
        'mock >= 1.0.1',
        'nose >= 1.3.0',
        'requests >= 2.5.1'
    ]
)
