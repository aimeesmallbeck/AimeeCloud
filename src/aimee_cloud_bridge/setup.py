#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

from setuptools import setup
import os
from glob import glob

package_name = 'aimee_cloud_bridge'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name, f'{package_name}.brick'],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Arduino SRL',
    maintainer_email='software@arduino.cc',
    description='AimeeCloud MQTT bridge for AIMEE Robot',
    license='MPL-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'cloud_bridge_node = aimee_cloud_bridge.cloud_bridge_node:main',
        ],
    },
)
