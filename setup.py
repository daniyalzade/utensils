from setuptools import setup
import utensils

requires = []

packages = [
    'utensils',
]

setup(
    name='utensils',
    version='0.0.43',
    packages=packages,
    description='Library of utilities for python',
    license='BSD',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    package_dir={
        'utensils': 'utensils'
        },
    classifiers=[
        "License :: OSI Approved :: BSD License",
    ]
)
