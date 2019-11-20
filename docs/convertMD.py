from m2r import parse_from_file
import os

with open('README.rst', 'w') as f:
    f.write(parse_from_file(os.path.join('..','README.md')))
