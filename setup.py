"""
Setup script for ``radarly-py``
"""

from os.path import dirname, join
from setuptools import setup, find_packages


def readme():
    """Generate the README file of the package"""
    filepath = join(dirname(__file__), 'README.rst')
    with open(filepath) as file_readme:
        return file_readme.read()


setup(
    name='radarly-py',
    version='1.0.11',
    description="Python client for Radarly API",
    long_description=readme(),
    author='Linkfluence',
    author_email='help@linkfluence.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'lxml',
        'pytz',
        'python-dateutil',
        'pycountry',
    ],
    include_package_data=True,
    keywords='radarly linkfluence api',
    license='Apache-2.0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    project_urls={
        'Documentation': 'https://api.linkfluence.com',
    },
    python_requires='>=3.4',
)
