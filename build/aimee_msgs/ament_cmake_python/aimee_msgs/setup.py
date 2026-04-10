from setuptools import find_packages
from setuptools import setup

setup(
    name='aimee_msgs',
    version='0.1.0',
    packages=find_packages(
        include=('aimee_msgs', 'aimee_msgs.*')),
)
