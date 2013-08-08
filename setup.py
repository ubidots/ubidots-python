from setuptools import setup, find_packages


def read_file(name):
    with open(name, "r") as f:
        return f.read()

setup(
    name='ubidots',
    version='0.1.0-alpha',
    author='Ubidots Team',
    author_email='devel@ubidots.com',
    url='https://github.com/ubidots/ubidots-python/',
    license='MIT',
    description='Api Client to connect to ubidots.com',
    long_description=read_file("README.rst"),
    platforms='any',
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
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
        "requests >= 1.2.3",
    ],
)
