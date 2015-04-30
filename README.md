encodingcom
===========

Python 3 service package for Encoding.com api.

Key Features:
* Design principle follows using encoding.com defaults, and enabling callers to override should details be stated.
* Enforce key JSON data needs for success of a call to minimize poorly constructed or 
    missing data components during call
* Exception handling for all responses
* Standardize on JSON


Revision History

0.1.0
* Complete rewrite from original hard contract binding specifics to 
    variable/kwargs driven principle enable client to specify data specifics for call structure.

* Design principle follows using encoding.com defaults, and enabling callers to override should details be stated.

* Enforce key JSON data needs for success of a call to minimize poorly constructed or 
    missing data components during call

* Exception handling for all responses... as encoding.com embeds all errors within a HTTP status 200 call.
    Not restful or complies with https://tools.ietf.org/html/rfc7231
* Errors parsed are thrown as exceptions enabling caller to catch and process accordingly

* Unit tests initial set for positive and negative
    Core and needs to grow more fo
    
* Helpers to keep parse and retrieve key content from the encoding.com response

* Poorly documented thumbnail data specifics now reflect email from devops at encoding.com

* HTTP(S) support

* Request package adoption, move away from URLLib


0.0.5
* PEP8 Compliant
* Pythonic handling of imports
* Fix all warnings
* Pythonic practice of auto-initialzer when invoking Encoding class objects
* zip_safe flag is false as we want source code to be installed in site_packages.
  This package is so small, zip is not warranted


0.0.4
* Original distribution to PyPi


