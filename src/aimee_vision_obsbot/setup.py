from setuptools import find_packages, setup

package_name = 'aimee_vision_obsbot'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Aimee Team',
    maintainer_email='aimee@example.com',
    description='OBSBOT Tiny 2 camera control via OSC/SDK for Aimee Robot',
    license='MPL-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'obsbot_node = aimee_vision_obsbot.obsbot_node:main',
            'obsbot_keepalive_node = aimee_vision_obsbot.obsbot_keepalive_node:main',
        ],
    },
)
