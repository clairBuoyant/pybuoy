Change Log
==========

0.5.9 (2025-08-13)
------------------

Internal
~~~~~~~~

- Update all dependencies to latest.
- Update pre-commit hooks to latest.

Security
~~~~~~~~

- Address CVE-2024-47081 by updating ``requests`` to ``2.32.4``.
- Address CVE-2025-50181 by updating ``urllib3`` to ``2.5.0``.
- Address CVE-2025-50182 by updating ``urllib3`` to ``2.5.0``.

0.5.8 (2025-05-18)
------------------

Internal
~~~~~~~~

- Update all dependencies to latest.

Security
~~~~~~~~

- Address CVE-2025-27516 by updating ``jinja2`` to ``3.1.6``.

0.5.7 (2024-12-26)
------------------

Internal
~~~~~~~~

- Update all dependencies to latest.

Security
~~~~~~~~

- Update ``jinja2`` to 3.1.5 (CVE-2024-56201, CVE-2024-56326)

0.5.6 (2024-10-19)
------------------

Fix
~~~

- ``lxml``: parsing error by converting unicode strings responses with encoding declaration
  to bytes.

Internal
~~~~~~~~

- Update all dependencies to latest.

0.5.5 (2024-07-04)
------------------

Internal
~~~~~~~~

- Update all dependencies to latest

Security
~~~~~~~~

- Update ``requests`` to 2.32.3 (CVE-2024-35195)
- Update ``jinja2`` to 3.1.4 (CVE-2024-34064)
- Update ``urllib3`` to 2.2.2 (CVE-2024-37891)

0.5.4 (2024-04-13)
------------------

Internal
~~~~~~~~

- Replace ``black``, ``flake8``, and ``isort`` with ``ruff``.
- Update all dependencies to latest.

Security
~~~~~~~~

- Update ``black`` to 24.3.0  (CVE-2024-21503)
- Update ``idna`` to 3.7.0    (CVE-2024-3651)

0.5.3 (2024-01-15)
------------------

Internal
~~~~~~~~

- Update ``certifi`` to 2023.7.22 (CVE-2023-37920)
- Update ``jinja2`` to 3.1.3     (CVE-2024-22195)
- Update ``urllib3`` to 2.1.0    (CVE-2023-43804, CVE-2023-45803)

0.5.2 (2023-05-24)
------------------

Internal
~~~~~~~~

- Bump ``requests`` to 2.31.0 (CVE-2023-32681)
- Bump all dependencies to latest.

0.5.1 (2023-03-26)
------------------

Fix
~~~

- **Forecasts**: ``.value`` of ``ForecastObservation`` will default to ``None`` (type: NoneType)
  when datum missing instead of ``nan`` (type: float) to support ``JSON``.

0.5.0 (2023-03-04)
------------------

Buoy
~~~~

- **Forecasts**: ``get`` returns an iterable ``ForecastObservations`` object. The type of
  iterable provided is ``ForecastObservation``.

Internal
~~~~~~~~

- Bump certifi to 2022.12.07. (CVE-2022-23491)
- Update all dependencies to latest.

0.4.3 (2022-09-19)
------------------

Documentation
~~~~~~~~~~~~~

- Scaffold and publish documentation.

Internal
~~~~~~~~

- Update all dependencies to latest.
- Organize dependencies in ``pyproject.toml`` by groups (e.g., "dev" and "docs").

0.4.2 (2022-09-05)
------------------

mypy
~~~~

- **Types**: ``realtime.get`` `infers exact return type`_ from user-provided value for ``dataset``.

ObservationDatum
~~~~~~~~~~~~~~~~

Refers to a particular piece of data from an ``Observation``. Metadata can be accessed
with ``.label``, ``.unit``, and ``.value`` (e.g., ``wind_direction.value``).

- **ObservationFloatDatum**: validate numeric values (previously ``ObservationDatum``).
- **ObservationStringDatum**: validate non-numeric values.

Observation
~~~~~~~~~~~

Weather observation recorded at unique datetime by type of ``dataset`` (e.g., meteorological).

- **MeteorologicalObservation**: attributes return either ``ObservationFloatDatum``
  or `ObservationStringDatum` after validating data provided from NDBC.
- **WaveSummaryObservation**: attributes return either ``ObservationFloatDatum``
  or ``ObservationStringDatum`` after validating data provided from NDBC.

Observations
~~~~~~~~~~~~

The following models were extended from ``Observations`` to support static typing:

- **MeteorologicalObservations**: can use ``+=`` syntax on an instance
  of this class in order to append ``MeteorologicalObservation`` records.
- **WaveSummaryObservations**: can use ``+=`` syntax on an instance
  of this class in order to append ``WaveSummaryObservation`` records.

Internal
~~~~~~~~

- Bump all development dependencies to latest.
- Extend tests to check for expected attributes.

0.4.1 (2022-08-31)
------------------

Observation
~~~~~~~~~~~

- **MeteorologicalObservation**: change ``dominate_wave_period`` to
  ``dominant_wave_period``.

0.4.0 (2022-08-29)
------------------

Buoy
~~~~

- **Realtime**: ``get`` now supports Wave Summary data (i.e., dataset="spec").

Observation
~~~~~~~~~~~

- **MeteorologicalObservation**: new model of type ``Observation``
  to represent API calls for realtime meteorological data. Attributes
  return instances of ``ObservationDatum`` by label (snaked cased).
  This directly supports enhancements for static type checking introduced
  in this release.

- **WaveSummaryObservation**: new model of type ``Observation`` to
  represent API calls for realtime wave summary data. Attributes
  return instances of ``ObservationDatum`` by label (snaked cased).
  This directly supports enhancements for static type checking
  introduced in this release.

- **ObservationDatum**: renamed ``Observation`` to ``ObservationDatum``.
  This represents a piece of data that was observed by a buoy at a unique
  datetime and contains metadata like unit of measurement (i.e., ``.unit``).
  It is renamed to better define its function and purpose.

mypy
~~~~

- **Types**: extend type checking support to all objects and iterables.

Internal
~~~~~~~~

- Update tests to account for incoming changes.
- Bump all dependencies to latest.

Breaking Changes
-------------------

Observations
~~~~~~~~~~~~

- **Observation**: is now ``ObservationDatum``; the original purpose of
  ``Observation``, which was introduced in v0.3.0, has been moved to
  this new object.

- **ObservationDatum**: value will default to ``None`` (type: NoneType)
  when datum missing instead of ``nan`` (type: float). This change should
  improve experience when working with ``JSON`` objects or databases.

- **Observations**: container for models of type ``Observation`` such as
  ``MeteorologicalObservation``, which will be new response type for all
  API calls.

Buoy
~~~~

- **Realtime**: ``get`` returns an iterable ``Observations`` object. The type of
  iterable provided depends on the query. If requesting meteorological data, type
  of ``Observation`` would be ``MeteorologicalObservation``. The primary purpose
  of these types of ``Observation`` objects is to define available attributes.

0.3.0 (2022-08-12)
------------------

Buoy
~~~~

- **Realtime**: ``get`` returns list of ``Observation`` instances. Instance
  of ``Observation`` will default to ``nan`` (type: float) when datum is missing.

mypy
~~~~

- **Types**: provide type annotations to support static type checking.

Internal
~~~~~~~~

- Add new ``pre-commit`` hooks and update all other hooks to latest version.
- Address PEP8 warnings identified by flake8.
- Refactor all imports to absolute from relative.
- Bump all dependencies to latest.

Documentation
~~~~~~~~~~~~~

- Fix broken href in CONTRIBUTING.
- Update `doc/examples`_ with examples of query response.

0.2.0 (2022-07-10)
------------------

Buoy
~~~~

- **Realtime**: ``get`` returns ``None`` when data cannot be successfully retrieved.

Documentation
~~~~~~~~~~~~~

- Update documentation and examples with revised syntax.

Breaking Changes
----------------

Buoy
~~~~

- **Realtime**: ``Buoy`` class instantiation no longer accepts arguments.
  - ``station_id`` must now be provided as an argument for every request (see examples in docs).

0.1.1 (2022-07-04)
------------------

Documentation
~~~~~~~~~~~~~

- Add examples and installation instructions.

0.1.0 (2022-07-04)
------------------

🎉 **Initial release** 🎉

Features
~~~~~~~~

- Get realtime data for buoy by ``station_id``.
  - encapsulates realtime data with ``Observation`` class.
- Get list of all active stations.

Internal
~~~~~~~~

- Incorporate githooks with ``pre-commit`` for development workflow.

.. _doc/examples: https://github.com/clairBuoyant/pybuoy/tree/main/docs/examples
..  _infers exact return type: https://github.com/clairBuoyant/pybuoy/pull/14#issue-1362358830
