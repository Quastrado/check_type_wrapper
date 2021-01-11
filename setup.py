from setuptools import find_packages, setup
import versioneer


with open('README.md', 'r') as fh:
    long_description = fh.read()
with open('requirements.txt', 'r') as fh:
    requirements = [line.strip() for line in fh]


setup(
    name='Quastrado_check_type_wrapper',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
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
