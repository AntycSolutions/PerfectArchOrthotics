from setuptools import setup

import os

# Put here required packages
packages = ['Django<=1.6',
            'South<=1.0']

if 'REDISCLOUD_URL' in os.environ and 'REDISCLOUD_PORT' in os.environ and 'REDISCLOUD_PASSWORD' in os.environ:
     packages.append('django-redis-cache')
     packages.append('hiredis')

setup(name='PerfectArchOrthotics',
      version='1.0',
      description='Client tracking application for Danny Mu',
      author='Eric and Chris Klinger',
      author_email='eklinger@ualberta.ca',
      url='https://pypi.python.org/pypi',
      install_requires=packages,
)

