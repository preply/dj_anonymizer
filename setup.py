from distutils.core import setup


setup(
    name='dj_anonymizer',
    packages=['dj_anonymizer'],
    version='0.1.1',
    description='A random test lib',
    author='Tim Pagurets',
    author_email='tim@preply.com',
    url='https://github.com/knowledge-point/dj_anonymizer',
    download_url='https://github.com/knowledge-point/dj_anonymizer/archive/0.1.1.tar.gz',
    keywords=['django', 'database', 'anonymization'],
    classifiers=[],
    install_requires=['django-bulk-update==1.1.10']
)
