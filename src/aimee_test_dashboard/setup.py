#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

from setuptools import setup, find_packages
import os
from glob import glob

package_name = 'aimee_test_dashboard'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
        # Include web templates
        (os.path.join('share', package_name, 'web/templates'), 
         glob('aimee_test_dashboard/web/templates/*')),
    ],
    install_requires=['setuptools', 'flask'],
    zip_safe=True,
    maintainer='Arduino SRL',
    maintainer_email='software@arduino.cc',
    description='Web-based testing dashboard for AIMEE Robot with simulation mode',
    license='MPL-2.0',
    extras_require={'test': ['pytest']},
    entry_points={
        'console_scripts': [
            'dashboard_node = aimee_test_dashboard.dashboard_node:main',
        ],
    },
)
