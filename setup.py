from distutils.core import setup
import py2exe

setup(
    console=["hook.py"],
    name='hook',
    version='1.0.0',
    packages=['bin', 'bin.logger'],
    url='https://www.facebook.com/adnane.deev',
    license='',
    author='Adnane Boulben',
    author_email='adnane.deev@gmail.com',
    description='Hook for programming workflow',
    requires=['colorama']
)
