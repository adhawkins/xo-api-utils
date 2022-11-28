# xo-api-utils
A collection of utilities using the Xen Orchestra API

# Generating a token
As the user running XO:

`./xen-orchestra/node_modules/.bin/xo-cli --createToken <url> <user>`

Replace `<url>` with the URL you use to access XO, and `<user>` with the name of a user with appropriate access permissions.

Copy the `authentication-example.py` file to `authentication.py` and put the token returned from the previous command into it. This will be used by all of the utilities.

If you receive `401 Client Error: Unauthorized` running the utilities, then the token may need to be regenerated. Repeat the process above.

# Using the utilities
Run `setup.sh` to install the requirements into a venv and activate it.

# Utilities

## xo-sr-usage.py

Dumps the usage information of all SRs

```
usage: xo-sr-usage.py [-h] --xo-url XO_URL
```

The `--xo-url` parameter is required.
