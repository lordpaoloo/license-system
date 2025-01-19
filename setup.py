from setuptools import setup, find_packages

setup(
    name='license-system',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'bottle',
    ],
    entry_points={
        'console_scripts': [
            'license-system=app:main',
        ],
    },
    author='Yousef Mohammad',
    author_email='your.email@example.com',
    description='A simple license management system using Bottle framework',
    url='https://github.com/lordpaoloo/license-system',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Bottle',
        'License :: OSI Approved :: MIT License',
    ],
)