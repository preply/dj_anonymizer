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
    version='0.6.1-dev',
    description='dj_anonymizer is a utility designed to anonymize '
                + 'production databases with various types of mock data, '
                + 'specifically designed for use within Django projects.'
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
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Framework :: Django',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Topic :: Database'
    ],
    install_requires=[
        'Django>=4.2',
    ]
)
