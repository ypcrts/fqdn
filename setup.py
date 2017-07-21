from setuptools import setup
setup(
    name='fqdn',
    packages=['fqdn'],
    version='1.1.0',
    description=('Validate fully-qualified domain names compliant '
                 'to RFC 1035 and the preferred form in RFC 3686 s. 2.'),
    install_requires=[],
    author='Guy Hughes',
    author_email='ypcrts',
    url='https://github.com/ypcrts/fqdn',
    keywords=['fqdn', 'domain', 'hostname'],
    license='MPL 2.0',
    zip_safe=True,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
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
