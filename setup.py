from setuptools import setup, find_packages

setup(
    name="ravenchain",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "ecdsa>=0.18.0",
        "base58>=2.1.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ]
    },
)
