from setuptools import setup, find_packages


def read_file(name):
    with open(name, "r") as f:
        return f.read()


setup(
    name="ubidots",
    version="2.0.0",
    author="Ubidots Team",
    author_email="devel@ubidots.com",
    url="https://github.com/ubidots/ubidots-python/",
    license="MIT",
    description="Python client for the Ubidots API v2.0",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    platforms="any",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Hardware",
    ],
    install_requires=[
        "requests>=2.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
        ],
    },
)
