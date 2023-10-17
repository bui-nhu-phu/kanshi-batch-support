from setuptools import setup

setup(
    name='kanshi-lib',
    version='0.0.6',
    author='buinhuphu',
    author_email='bn.phu@afterfit.co.jp',
    package_dir = {'':'src'},
    install_requires=[
        'python-dotenv==1.0.0',
        'requests==2.31.0',
        'urllib3<2',
        'botocore==1.31.64'
    ],
)
