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

# First steps

In this tutorial, you will install `cwl2datacite` and convert the metadata in a
CWL document to DataCite Metadata Schema 4.6 JSON.

## Install

```bash
pip install cwl2datacite
```

## Convert a CWL document

Choose a CWL document that contains Schema.org metadata and run:

```bash
transpiler-mate cwl2datacite workflow.cwl --output datacite.json
```

Replace `workflow.cwl` with the path to your document. The plugin reads the CWL
metadata resolved by Transpiler-Mate and writes the converted DataCite 4.6
metadata to `datacite.json`.

If `--output` is omitted, the plugin uses `datacite.json` in the current
directory.

## Inspect the result

Open `datacite.json` and check the converted creators, contributors, title,
publisher, publication year, descriptions, identifiers, dates, resource type,
and rights metadata. The generated structure targets DataCite 4.6; it is not a
version-neutral DataCite representation.

## Next step

Move to the how-to guides when you need to complete a specific operational task.
