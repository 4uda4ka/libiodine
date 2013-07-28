from distutils.core import setup, Extension

setup(
    name='libiodine',
    description='A module used as iodine judger backend',
    long_description=open('README').read(),
    author='Jason Lau',
    author_email='i@dotkrnl.com',
    url='https://github.com/dotkrnl/libiodine',
    download_url='https://pypi.python.org/pypi/libiodine/',
    packages=['libiodine',],
    version='0.1dev',
    platforms=['Unix', 'Linux', ], 
    license='GPL',
)
