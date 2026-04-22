from setuptools import setup

package_name = 'aimee_manipulation'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Aimee Team',
    maintainer_email='aimee@example.com',
    description='Arm control and manipulation skills for Aimee robot',
    license='MPL-2.0',
    extras_require={'test': ['pytest']},
    entry_points={
        'console_scripts': [
            'arm_controller_node = aimee_manipulation.arm_controller_node:main',
            'pick_place_server = aimee_manipulation.pick_place_server:main',
            'test_pick_place_client = aimee_manipulation.test_pick_place_client:main',
        ],
    },
)
