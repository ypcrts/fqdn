from setuptools import setup

setup(
    name="fqdn",
    packages=["fqdn"],
    version="1.5.0",
    description=(
        "Validates fully-qualified domain names against RFC 1123, "
        "so that they are acceptable to modern bowsers"
    ),
    author="ypcrts",
    author_email="ypcrts@users.noreply.github.com",
    url="https://github.com/ypcrts/fqdn",
    keywords=["fqdn", "domain", "hostname", "RFC3686", "dns"],
    license="MPL 2.0",
    zip_safe=True,
    install_requires=["cached-property>=1.3.0;python_version<'3.8'"],
    python_requires=">=2.7, !=3.0, !=3.1, !=3.2, !=3.3, !=3.4, <4",
    test_suite="tests",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: Name Service (DNS)",
        "Topic :: Internet",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
)
