#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

from setuptools import setup
import os
from glob import glob

package_name = 'aimee_tts'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
    ],
    install_requires=['setuptools', 'gtts', 'pygame'],
    zip_safe=True,
    maintainer='Arduino SRL',
    maintainer_email='software@arduino.cc',
    description='Text-to-Speech with Kokoro (primary) and gTTS (fallback) for AIMEE Robot',
    license='MPL-2.0',
    extras_require={'test': ['pytest']},
    entry_points={
        'console_scripts': [
            'tts_node = aimee_tts.tts_node:main',
        ],
    },
)
