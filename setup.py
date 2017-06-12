from setuptools import setup
setup(
    name='fqdn',
    packages=['fqdn'],
    version='1.0.2',
    description=('Validate fully-qualified domain names compliant '
                 'to RFC 1035 and the preferred form in RFC 3686 s. 2.'),
    install_requires=[],
    author='0x6768',
    author_email='0x6768@gmail.com',
    url='https://github.com/0x6768/fqdn',
    keywords=['fqdn', 'domain', 'hostname'],
    license='MPL 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
        'Environment :: Web Environment',
    ]
)
