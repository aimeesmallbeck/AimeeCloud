from setuptools import setup, find_packages

package_name = 'arduino'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Aimee Team',
    maintainer_email='aimee@example.com',
    description='Arduino brick framework utilities for AIMEE',
    license='MPL-2.0',
    extras_require={'test': ['pytest']},
    entry_points={},
)
