try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name='dj_anonymizer',
    packages=['dj_anonymizer'],
    version='0.1.6',
    description='This project helps anonymize production database' +
                'with fake data of any kind.',
    long_description=(read('README.md')),
    license='MIT',
    author='Tim Pagurets',
    url='https://github.com/knowledge-point/dj_anonymizer',
    keywords=['django', 'data', 'database', 'anonymization', 'dj-anonymizer'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
        'Topic :: Database'
    ],
    install_requires=[
        'Django==1.11.13',
        'django-bulk-update==2.2.0'
    ]
)
