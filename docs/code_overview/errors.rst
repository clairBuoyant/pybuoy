Errors
======

Every error pybuoy raises derives from :class:`pybuoy.PybuoyError`. Invalid arguments raise
``ValueError`` before any request is made.

.. autoclass:: pybuoy.PybuoyError

.. autoclass:: pybuoy.RequestError
    :members: status

.. autoclass:: pybuoy.StationNotFoundError

.. autoclass:: pybuoy.ParseError
