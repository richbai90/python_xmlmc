from distutils.core import setup

setup(
    name='Xmlmc',
    version='0.1dev',
    install_requires=['requests', 'lxml'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    packages=['xmlmc']
)