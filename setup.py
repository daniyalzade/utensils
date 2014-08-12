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
    long_description=open('README.rst').read(),
    version=utensils.__version__,
    #data_files=[
    #    ('', ['README.rst', 'LICENSE']),
    #    ('utensils', [
    #        'utensils/base.html',
    #        'utensils/style.css',
    #        ]),
    #    ],
    package_dir={
        'utensils': 'utensils'
        },
    #package_data={
    #    'utensils': [
    #        '*.html',
    #        '*.css',
    #        ],
    #    },
    install_requires=requires,
    include_package_data=True,
)
