from setuptools import setup, find_packages

setup(
    name='depth-estimation',
    version='0.1.0',
    description='A library for depth estimation',
    author='Artem Trybushenko',
    author_email='artem.trybushenko@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)