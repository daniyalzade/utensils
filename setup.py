from distutils.core import setup
import utensils

requires = []

packages = [
    'utensils',
]

setup(
    name='utensils',
    author='Eytan Daniyalzade',
    author_email='eytan85@gmail.com',
    url='http://daniyalzade.com',
    packages=packages,
    description='Library of utilities for python',
    license='BSD',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    version='0.0.43',
    package_dir={
        'utensils': 'utensils'
        },
    classifiers=[
        "License :: OSI Approved :: BSD License",
    ]
)
