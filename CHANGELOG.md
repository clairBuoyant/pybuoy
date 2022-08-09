## Unreleased

### Internal

- **mypy**: provide type annotations to support static type checking.

## 0.2.0 (2022-07-10)

### Buoy

- **Realtime**: `get` returns `None` when data cannot be successfully retrieved.

### Documentation

- Update documentation and examples with revised syntax.

## Breaking Changes

### Buoy

- **Realtime**: `Buoy` class instantiation no longer accepts arguments.
  - `station_id` must now be provided as an argument for every request (see examples in docs).

## 0.1.1 (2022-07-04)

### Documentation

- Add examples and installation instructions.

## 0.1.0 (2022-07-04)

🎉 **Initial release** 🎉

## Features

- Get realtime data for buoy by `station_id`.
  - encapsulates realtime data with `Observation` class.
- Get list of all active stations.

## Internal

- Incorporate githooks with `pre-commit` for development workflow.
