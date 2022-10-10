from os import path
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='python-namesilo',
    version='1.4.1',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=['requests', 'xmltodict'],
    python_requires='>=3.6,<=3.10',
    py_modules=['namesilo'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    url='https://github.com/goranvrbaski/python-namesilo',
    license='GPLv3+',
    author='Goran Vrbaski',
    author_email='vrbaski.goran@gmail.com',
    description='API wrapper for Namesilo service',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
