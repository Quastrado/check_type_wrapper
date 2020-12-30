from setuptools import find_packages, setup


with open('README.md', 'r') as fh:
    long_description = fh.read()


setup(
    name='Quastrado_check_type_wrapper',
    version='0.1.6',
    author='Quastrado',
    author_email='quastrado@gmail.com',
    description='''
    A simple decorator to control the type matching of the arguments passed
    ''',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Quastrado/check_type_wrapper',
    packages=find_packages()
)
