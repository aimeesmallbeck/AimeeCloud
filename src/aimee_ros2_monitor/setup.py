from setuptools import setup

package_name = 'aimee_ros2_monitor'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', [f'resource/{package_name}']),
        (f'share/{package_name}', ['package.xml']),
        (f'share/{package_name}/templates', [
            'aimee_ros2_monitor/templates/index.html',
        ]),
    ],
    install_requires=['setuptools', 'flask'],
    zip_safe=True,
    maintainer='AIMEE Team',
    maintainer_email='aimee@arduino.cc',
    description='Lightweight ROS2 monitoring dashboard',
    license='MPL-2.0',
    extras_require={'test': ['pytest']},
    entry_points={
        'console_scripts': [
            'monitor_node = aimee_ros2_monitor.monitor_node:main',
        ],
    },
)
