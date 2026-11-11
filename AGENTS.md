# pybuoy

Agent instructions for `clairBuoyant/pybuoy`, a Python client for NDBC realtime
buoy data, NDBC's active station list and NOAA NDFD point forecasts.

## Layout

- `pybuoy/buoy.py`: `Buoy`, the entry point. It builds one HTTP client and hands
  it to the three sources.
- `pybuoy/realtime.py`, `stations.py`, `forecasts.py`: one module per data
  source. Each holds the request and a pure `parse_*` function.
- `pybuoy/models.py`: the frozen dataclasses returned to callers. A field's
  source column, unit and converter are declared once, in its `field` metadata.
- `pybuoy/_http.py`, `errors.py`: the HTTP client and the error types.
- `tests/fixtures/`: trimmed real NOAA/NDBC responses (see its README).

## Commands

Everything runs through `uv`, with versions from `uv.lock`.

- `./scripts/test`: lint, format check, type check and the offline tests.
- `./scripts/test -m live`: the tests that call NOAA and NDBC.
- `./scripts/lint`: apply lint fixes and formatting.
- `uv run sphinx-build -W docs docs/_build`: build the documentation.

## Container

The `Dockerfile` builds a development image with the locked toolchain:

```sh
docker build -t pybuoy-dev .
docker run --rm pybuoy-dev                           # ./scripts/test
docker run --rm -v "$PWD:/app" pybuoy-dev ./scripts/lint
```

The virtual environment lives at `/opt/venv`, so mounting the source over
`/app` keeps the installed dependencies.

## Conventions

- Tests come first and run offline. Parse real responses from
  `tests/fixtures/`; reach the network only in `tests/test_live.py`.
- To support another realtime dataset, add its dataclass to `models.py`, one
  entry to `_MODELS` in `realtime.py` and one `get` overload.
- Timestamps are timezone-aware UTC. Values are `None` when the source did not
  report them.
- Branch names match `(bug|chore|enhancement|feature|hotfix|release|wip)/name`.
  Commit messages follow Conventional Commits.
- Add user-visible changes to `CHANGES.rst`.
