from setuptools import setup

package_name = 'aimee_vision_pipeline'

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
    description='Color-based object detection and tracking for Aimee robot',
    license='MPL-2.0',
    extras_require={'test': ['pytest']},
    entry_points={
        'console_scripts': [
            'color_detector_node = aimee_vision_pipeline.color_detector_node:main',
            'object_tracker_node = aimee_vision_pipeline.object_tracker_node:main',
        ],
    },
)
