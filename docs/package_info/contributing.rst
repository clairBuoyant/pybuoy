Contributing to pybuoy
======================

pybuoy gladly welcomes new contributions. We have an established consistent way of doing
things. A consistent style increases readability, decreases bug-potential and makes it
faster to understand how everything works together.

pybuoy follows :PEP:`8` and :PEP:`257`. `Pre-Commit`_ is used to
manage a suite of ``pre-commit`` hooks that enforce conformance with these PEPs along with
several other checks.

The following are pybuoy-specific guidelines in addition to those PEPs.

.. note::

    In order to use the ``pre-commit`` hooks, install pybuoy's ``[dev]`` group dependencies,
    followed by the appropriate ``pre-commit`` command:

    .. code-block:: bash

        . ./aliases
        init

Code
----

- Within a single file classes are sorted alphabetically where inheritance permits.
- Within a class, methods are sorted alphabetically within their respective groups with
  the following as the grouping order:

  - Static methods
  - Class methods
  - Properties
  - Instance Methods

- Use descriptive names for the catch-all keyword argument. E.g., ``**other_options``
  rather than ``**kwargs``.

Testing
-------

Contributions to pybuoy requires 100% test coverage. If you know how to add a feature, but
aren't sure how to write the necessary tests, please open a PR anyway so we can work
with you to write the necessary tests.

Running the Test Suite
~~~~~~~~~~~~~~~~~~~~~~

`Github Actions`_ automatically runs all updates to known branches and pull requests. However,
it's useful to be able to run the tests locally. The simplest way is via:

.. code-block:: bash

    pytest

Without any configuration or modification, all the tests should pass.

Documentation
-------------

- All publicly available functions, classes and modules should have a docstring.
- Use correct terminology.

Files to Update
---------------

CHANGES
~~~~~~~

For feature additions, bugfixes, or code removal please add an appropriate entry to
``CHANGES.rst``. If the ``Unreleased`` section does not exist at the top of
``CHANGES.rst`` please add it. See `commit eedf0e0`_ for
an example.

See Also
--------

Please also read `Contributing to clairBuoyant`_

.. _commit eedf0e0: https://github.com/clairBuoyant/pybuoy/commit/eedf0e08f15c66909d0911d9ae1362756fec30f5

.. _contributing to clairBuoyant: https://github.com/clairBuoyant/.github/blob/main/CONTRIBUTING.md

.. _github actions: https://github.com/clairBuoyant/pybuoy/actions

.. _pre-commit: https://pre-commit.com
