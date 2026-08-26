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

# Architecture

`cwl2datacite` is a Transpiler-Mate conversion plugin. Transpiler-Mate resolves
the source CWL document and supplies its Schema.org metadata to the plugin. The
plugin maps that metadata to Pydantic models generated for DataCite Metadata
Schema 4.6 and serializes the result as JSON.

```text
CWL document -> Transpiler-Mate metadata -> DataCite 4.6 models -> JSON
```

The relevant package layout is:

```text
src/cwl2datacite/
    plugin.py                 # CWL-to-DataCite field mapping and serialization
    datacite_4_6_models.py    # generated DataCite 4.6 output models
schemas/
    datacite-4.6.yaml         # source schema for the generated models
tests/
docs/
```

The schema version is explicit in both the model module and its source file.
Supporting a different DataCite release therefore requires an intentional
schema and mapping update; it is not assumed to be interchangeable with 4.6.

The project uses Hatch for packaging, testing environments, and build
orchestration. Documentation is organized according to Diátaxis so that
learning, task completion, lookup, and conceptual understanding remain
separated.
