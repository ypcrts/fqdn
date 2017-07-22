from setuptools import setup
setup(
    name='fqdn',
    packages=['fqdn'],
    version='1.1.0',
    description=('Validate fully-qualified domain names compliant '
                 'to RFC 1035 and the preferred form in RFC 3686 s. 2.'),
    author='Guy Hughes',
    author_email='0x6768@gmail.com',
    url='https://github.com/guyhughes/fqdn',
    keywords=['fqdn', 'domain', 'hostname', 'RFC3686', 'dns'],
    license='MPL 2.0',
    zip_safe=True,
    install_requires=['cached-property>=1.3.0'],
    test_suite='tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ]
)
