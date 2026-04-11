from setuptools import setup

package_name = 'aimee_lerobot_bridge'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/config', [
            'config/roarm_m3_config.yaml',
            'config/lerobot_config.toml',
        ]),
        ('share/' + package_name + '/launch', [
            'launch/teleop.launch.py',
            'launch/data_collection.launch.py',
            'launch/policy_inference.launch.py',
        ]),
    ],
    install_requires=['setuptools', 'pyyaml', 'toml', 'numpy', 'opencv-python'],
    zip_safe=True,
    maintainer='Aimee Team',
    maintainer_email='aimee@example.com',
    description='LeRobot integration bridge for Aimee robot',
    license='MPL-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'dataset_recorder = aimee_lerobot_bridge.dataset_recorder:main',
            'policy_controller = aimee_lerobot_bridge.policy_controller:main',
            'teleop_keyboard = aimee_lerobot_bridge.teleop_keyboard:main',
            'teleop_gamepad = aimee_lerobot_bridge.teleop_gamepad:main',
            'bag_to_dataset = aimee_lerobot_bridge.bag_converter:main',
            'replay_episode = aimee_lerobot_bridge.replay_node:main',
        ],
    },
)
