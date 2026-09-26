# Copyright 2026 Terradue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import pytest
from pydantic import AnyUrl
from transpiler_mate.api import Organization, Person

from cwl2datacite.plugin import _to_creator


@pytest.mark.parametrize(
    "identifier",
    [
        None,
        "https://orcid.org/0000-0001-2345-6789",
        AnyUrl("https://orcid.org/0000-0001-2345-6789"),
    ],
)
@pytest.mark.parametrize("multiple_affiliations", [False, True])
def test_creator_preserves_scalar_identifiers_and_affiliations(
    identifier: str | AnyUrl | None, multiple_affiliations: bool
) -> None:
    organization = Organization(name="Example", identifier="https://ror.org/12345")
    author = Person(
        given_name="Ada",
        family_name="Lovelace",
        email="ada@example.org",
        identifier=identifier,
        affiliation=[organization, Organization(name="No identifier")]
        if multiple_affiliations
        else organization,
    )

    creator = _to_creator(author)

    if identifier is None:
        assert creator.name_identifiers is None
    else:
        assert creator.name_identifiers is not None
        assert len(creator.name_identifiers) == 1
        name_identifier = creator.name_identifiers[0]
        assert name_identifier.name_identifier == str(identifier)
        assert name_identifier.name_identifier_scheme == "ORCID"
        assert name_identifier.scheme_uri == AnyUrl("https://orcid.org")
    assert creator.affiliation is not None
    assert len(creator.affiliation) == 1
    affiliation = creator.affiliation[0]
    assert affiliation.affiliation_identifier == "https://ror.org/12345"
    assert affiliation.affiliation_identifier_scheme == "ROR"
    assert affiliation.scheme_uri == AnyUrl("https://ror.org")
