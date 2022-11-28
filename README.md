# xo-api-utils
A collection of utilities using the Xen Orchestra API

# Generating a token
As the user running XO:

`./xen-orchestra/node_modules/.bin/xo-cli --createToken <url> <user>`

Replace `<url>` with the URL you use to access XO, and `<user>` with the name of a user with appropriate access permissions.

Copy the token returned into `authentication.py`. This will be used by all of the utilities

# Using the utilities
Run `setup.sh` to install the requirements into a venv and activate it.

# Utilities

## xo-sr-usage.py

Dumps the usage information of all SRs
