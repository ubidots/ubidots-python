from setuptools import setup, find_packages

setup(
    name='ubidots',
    version='0.1.0-alpha',
    author='Ubidots Team',
    author_email=' devel@ubidots.com',
    url='https://github.com/Ubidots/ubidots-python/',
    license='LICENSE.txt',
    description='Api Client to connect to ubidots.com',
    long_description="Api Client to connect to ubidots.com",
    packages= find_packages(),
    install_requires=[
        "requests >= 1.2.3",
    ],
)
