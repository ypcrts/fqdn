from setuptools import setup

setup(
    name="fqdn",
    packages=["fqdn"],
    version="1.3.1",
    description=(
        "Validate fully-qualified domain names compliant "
        "to RFC 1035 and the preferred form in RFC 3686 s. 2."
    ),
    author="ypcrts",
    author_email="ypcrts@users.noreply.github.com",
    url="https://github.com/ypcrts/fqdn",
    keywords=["fqdn", "domain", "hostname", "RFC3686", "dns"],
    license="MPL 2.0",
    zip_safe=True,
    install_requires=["cached-property>=1.3.0"],
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
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
)
