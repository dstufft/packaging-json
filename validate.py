"""
Validates a distribution.json to verify it matches the requirement. It requires
that Distutils2 be installed.


Usage:
    python validate.py [/path/to/distribution.json ...]

Example:
    python validate.py examples/distribution.json

Output:
    examples/distribution.json              [OK]
"""
import json
import os
import string
import sys

from schema import Schema, And, Use, Optional, SchemaError
from distutils2 import version


VALDIATOR = Schema({
    "Metadata-Version": And(basestring, "2.0"),
    "Name": And(basestring, lambda x: "/" not in x),  # @@@ What exactly is "ok" for a name?
    "Version": Use(version.NormalizedVersion),
    "Summary": basestring,
    Optional("Description"): And(basestring),  # @@@ Verify ReST?
    Optional("Keywords"): [basestring],
    Optional("Author"): basestring,
    Optional("Author-Email"): And(basestring),  # @@@ Verify Proper Email
    Optional("Maintainer"): basestring,
    Optional("Maintainer-Email"): And(basestring),  # @@@ Verify Proper Email
    Optional("License"): basestring,
    Optional("Classifiers"): [basestring],
    Optional("URIs"): {And(basestring, lambda x: len(x) <= 32): And(basestring)},  # @@@ Verify Valid URI
    Optional("Platforms"): [basestring],
    Optional("Supported-Platforms"): [basestring],
    Optional("Provides-Extras"): [And(basestring, lambda x: not set(x) - (set(string.digits + string.ascii_letters + string.punctuation) - set("[],")))],
    Optional("Setup-Requires-Dists"): [Use(version.VersionPredicate)],
    Optional("Requires-Dists"): [Use(version.VersionPredicate)],
    Optional("Provides-Dists"): [Use(version.VersionPredicate)],
    Optional("Obsoletes-Dists"): [Use(version.VersionPredicate)],
    Optional("Requires-Python"): basestring,  # @@@ Validate Version Specifier
    Optional("Requires-Externals"): [basestring],
    Optional("Extensions"): {basestring: {basestring: lambda x: True}},
})


if __name__ == "__main__":
    paths = sys.argv[1:]

    results = []

    print ""

    for path in paths:
        data = None

        with open(os.path.abspath(path)) as f:
            data = json.load(f)

        try:
            VALDIATOR.validate(data)
        except SchemaError as exc:
            results.append(dict(file=path, status="FAILED"))

            print path
            print "=" * 50
            print exc
            print ""
        else:
            results.append(dict(file=path, status="OK"))

    for result in results:
        print "{file: <40}[{status}]".format(**result)
