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

CWL 2 DataCite converts metadata from a Common Workflow Language (CWL)
document into JSON targeting version 4.6 of the DataCite Metadata Schema.
It is distributed as a plugin for Transpiler-Mate.

!!! note "Supported DataCite version"

    DataCite 4.6 is the current conversion target. These docs do not claim
    compatibility with earlier or later versions of the DataCite Metadata
    Schema.

Use these docs by intent:

- [Tutorials](tutorials/index.md): learn by completing a guided path.
- [How-to guides](how-to/index.md): solve specific tasks.
- [Reference](reference/index.md): look up commands, APIs, and configuration.
- [Explanation](explanation/index.md): understand design decisions and concepts.

## Quick start

```bash
pip install cwl2datacite
transpiler-mate cwl2datacite workflow.cwl --output datacite.json
```
