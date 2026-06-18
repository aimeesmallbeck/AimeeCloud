from setuptools import find_packages, setup

package_name = 'aimee_vision_k210'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'pyserial'],
    zip_safe=True,
    maintainer='Aimee Team',
    maintainer_email='aimee@example.com',
    description='Hiwonder K210 (WonderMV) vision module integration for Aimee Robot',
    license='MPL-2.0',
    extras_require={'test': ['pytest']},
    entry_points={
        'console_scripts': [
            'k210_node = aimee_vision_k210.k210_node:main',
        ],
    },
)
