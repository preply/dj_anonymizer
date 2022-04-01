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
    include_package_data=True,
    version='0.5.1',
    description='This project helps anonymize production database '
                + 'with fake data of any kind.',
    long_description=(read('README.md')),
    long_description_content_type='text/markdown',
    license='MIT',
    author='Tim Pagurets',
    url='https://github.com/preply/dj_anonymizer',
    keywords=['django', 'data', 'database', 'anonymization', 'dj-anonymizer'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Topic :: Database'
    ],
    install_requires=[
        'Django>=2.2',
    ]
)
