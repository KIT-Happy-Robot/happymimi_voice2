from setuptools import setup

package_name = 'happymimi_voice2_common'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kawara',
    maintainer_email='c1139136@planet.kanazawa-it.ac.jp',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "stt = happymimi_voice2_common.stt_server:main",
            "tts = happymimi_voice2_common.tts_srvserver:main",
            "cli_stt = happymimi_voice2_common.client_stt:main",
            "cli_tts = happymimi_voice2_common.client_tts:main"
        ],
    },
)
