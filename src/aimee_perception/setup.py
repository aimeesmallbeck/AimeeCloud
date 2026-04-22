from setuptools import setup

package_name = 'aimee_perception'

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
    description='3D pose estimation and grasp planning for Aimee robot',
    license='MPL-2.0',
    extras_require={'test': ['pytest']},
    entry_points={
        'console_scripts': [
            'pose_estimator_node = aimee_perception.pose_estimator_node:main',
            'grasp_planner_node = aimee_perception.grasp_planner_node:main',
        ],
    },
)
