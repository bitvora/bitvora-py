from setuptools import setup, find_packages

setup(
    name='bitvora',
    version='0.1.0',
    description='A Python SDK for the Bitvora API and Webhooks.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/bitvora/bitvora-py',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License', 
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
