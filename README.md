<!--
Copyright 2026 Transpiler-Mate

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# CWL 2 DataCite

[![PyPI - Version](https://img.shields.io/pypi/v/cwl2datacite.svg)](https://pypi.org/project/cwl2datacite)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cwl2datacite.svg)](https://pypi.org/project/cwl2datacite)

CWL 2 DataCite is a Transpiler-Mate plugin that converts metadata from a
Common Workflow Language (CWL) document into JSON targeting version 4.6 of the
DataCite Metadata Schema.

DataCite 4.6 is the plugin's current conversion target. Compatibility with
earlier or later DataCite schema versions is not implied.

## Usage

Install the package, then invoke the plugin through the Transpiler-Mate CLI:

```console
pip install cwl2datacite
transpiler-mate cwl2datacite workflow.cwl --output datacite.json
```

The output path defaults to `datacite.json`.

## Project conventions

This project is templated a Hatch-based Python package with:

- Apache-2.0 license
- Keep a Changelog-compatible `CHANGELOG.md`
- Diátaxis documentation under `docs/`
- top-level `mkdocs.yaml`
- Taskfile integration with `Terradue/taskfile-utils`
- GitHub Actions CI

## Documentation

Project documentation is published at: https://Transpiler-Mate.github.io/cwl2datacite/

## Contribute

Submit a [Github issue](https://github.com/Transpiler-Mate/cwl2datacite/issues) if you have comments or suggestions.

### Local quality checks

Install [Hatch](https://hatch.pypa.io/) and [Taskfiles](https://taskfile.dev/docs/guide) then install the Git hook:

```console
task quality:pre-commit:install
```

Every commit runs Ruff (including the configured McCabe complexity limit),
Ruff formatting, strict mypy checks, and the pytest suite.

Run the complete hook explicitly with:

```console
task quality:pre-commit:run
```

## License

[![Apache License, Version 2.0](https://img.shields.io/badge/license-Apache%20License%202.0-blue)](https://www.apache.org/licenses/LICENSE-2.0)
