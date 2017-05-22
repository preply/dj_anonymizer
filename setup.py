try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='dj_anonymizer',
    packages=['dj_anonymizer'],
    version='0.1.2',
    description='This project helps anonymize production database with fake data of any kind.',
    license='MIT',
    author='Tim Pagurets',
    author_email='tim@preply.com',
    url='https://github.com/knowledge-point/dj_anonymizer',
    download_url='https://github.com/knowledge-point/dj_anonymizer/archive/0.1.2.tar.gz',
    keywords=['django', 'data', 'database', 'anonymization', 'dj-anonymizer'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
        'Topic :: Database'
    ],
    install_requires=['django-bulk-update==1.1.10']
)
