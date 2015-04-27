"""
encodingcom service package.

Features:

Core Functionality:
* Wrap and deliver encoding.com with ease
* Handle processing of error returns, map to appropriate serviceable python exceptions
    Many encoding.com 2xx returns are reflection of a successful call, but in actual the call has failed.
    Handle these contextual error scenarios so client can handle more appropriately
* Uses JSON for core delivery and response content, much nicer than XML encoding.com defaults
    If clients desires XML output, package does NOT currently support this workflow
* Support Python native types for clients.
    Package converts python data structures to encodingcom normalized data format.
    For example:  ['1', '2', '3'] converts to '1, 2, 3'

Design Principles:
* No contract enforcements in Encoding.com Request Template, enables usage Encoding.com defaults to be used.
    ie. settings are missing from the client specified contents, defaults will be used.
    Client has to be aware and responsible of the defaults, as default settings will having varying outcomes.

* Basic key guards put into Encoding.com Request Template
    Minimize number of errors by provision key needed request template needs.
    Items such as keys, secret, response format, etc are automatically provisioned

* Key Job settomgs with defaults that can be overridden to accommodate clients needs
    For example: default_instant (undocumented in core docs) enables a job to be processed as soon as upload starts


"""