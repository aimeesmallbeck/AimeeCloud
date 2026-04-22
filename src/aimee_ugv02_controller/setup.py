from setuptools import setup

package_name = 'aimee_ugv02_controller'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'pyserial'],
    zip_safe=True,
    maintainer='Aimee Team',
    maintainer_email='aimee@example.com',
    description='UGV02 rover platform controller using JSON serial protocol',
    license='MPL-2.0',
    extras_require={'test': ['pytest']},
    entry_points={
        'console_scripts': [
            'ugv02_controller_node = aimee_ugv02_controller.ugv02_controller_node:main',
            'ugv02_teleop_node = aimee_ugv02_controller.ugv02_teleop_node:main',
        ],
    },
)
