# Copyright 2026 Transpiler-Mate
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

"""transpiler-mate plugin for CWL 2 DataCite."""

from __future__ import annotations

import json
import time
import uuid
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Any
from urllib.parse import urlparse

from loguru import logger
from pydantic import AnyUrl, BaseModel, ConfigDict, Field
from transpiler_mate.api import (
    AuthorRole,
    ContributorRole,
    CreativeWork,
    Organization,
    Person,
    PluginExecutionError,
    SoftwareApplication,
    transpiler_plugin,
)

from .datacite_4_6_models import (
    Affiliation,
    Contributor,
    ContributorType,
    Creator,
    DataCiteAttributes,
    Date,
    DateType,
    Description,
    DescriptionType,
    Identifier,
    NameIdentifier,
    NameType,
    Publisher,
    RelatedIdentifier,
    RelatedIdentifierType,
    RelationType,
    ResourceType,
    ResourceTypeGeneral,
    Right,
    Title,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

    from transpiler_mate.api import TranspilerContext

__ROLES_MAPPING_: Mapping[AnyUrl, ContributorType] = {
    AnyUrl(
        "https://credit.niso.org/contributor-roles/conceptualization/"
    ): ContributorType.RESEARCHER,
    AnyUrl(
        "https://credit.niso.org/contributor-roles/data-curation/"
    ): ContributorType.DATA_CURATOR,
    AnyUrl(
        "https://credit.niso.org/contributor-roles/formal-analysis/"
    ): ContributorType.RESEARCHER,
    AnyUrl(
        "https://credit.niso.org/contributor-roles/funding-acquisition/"
    ): ContributorType.OTHER,
    AnyUrl(
        "https://credit.niso.org/contributor-roles/investigation/"
    ): ContributorType.RESEARCHER,
    AnyUrl(
        "https://credit.niso.org/contributor-roles/methodology/"
    ): ContributorType.RESEARCHER,
    AnyUrl(
        "https://credit.niso.org/contributor-roles/project-administration/"
    ): ContributorType.PROJECT_MANAGER,
    AnyUrl(
        "https://credit.niso.org/contributor-roles/resources/"
    ): ContributorType.OTHER,
    AnyUrl(
        "https://credit.niso.org/contributor-roles/software/"
    ): ContributorType.OTHER,
    AnyUrl(
        "https://credit.niso.org/contributor-roles/supervision/"
    ): ContributorType.SUPERVISOR,
    AnyUrl(
        "https://credit.niso.org/contributor-roles/validation/"
    ): ContributorType.RESEARCHER,
    AnyUrl(
        "https://credit.niso.org/contributor-roles/visualization/"
    ): ContributorType.PRODUCER,
    AnyUrl(
        "https://credit.niso.org/contributor-roles/writing-original-draft/"
    ): ContributorType.OTHER,
    AnyUrl(
        "https://credit.niso.org/contributor-roles/writing-review-editing/"
    ): ContributorType.OTHER,
}


class CWL2DataCiteOptions(BaseModel):
    """Options accepted by the CWL 2 DataCite plugin."""

    model_config = ConfigDict(extra="forbid")

    output: Annotated[
        Path,
        Field(default=Path("datacite.json"), description="The output file path"),
    ]


def _to_contributor(author: Person | ContributorRole) -> Contributor:
    contributor_type = ContributorType.OTHER

    if isinstance(author, ContributorRole):
        if author.additional_type:
            contributor_type = __ROLES_MAPPING_.get(
                author.additional_type, ContributorType.OTHER
            )

        author = author.contributor

    contributor: Contributor = Contributor(
        contributor_type=contributor_type,
        name_type=NameType.PERSONAL,
        name=f"{author.family_name}, {author.given_name}",
        given_name=author.given_name,
        family_name=author.family_name,
    )

    _finalize(author=author, creator=contributor)

    return contributor


def _to_creator(author: Person | AuthorRole) -> Creator:
    if isinstance(author, AuthorRole):
        author = author.author

    creator: Creator = Creator(
        name_type=NameType.PERSONAL,
        name=f"{author.family_name}, {author.given_name}",
        given_name=author.given_name,
        family_name=author.family_name,
    )

    _finalize(author=author, creator=creator)

    return creator


def _finalize(author: Person | Organization, creator: Creator):
    if author.identifier:
        creator.name_identifiers = []
        for identifier in (
            author.identifier
            if isinstance(author.identifier, list)
            else [author.identifier]
        ):
            scheme, netloc, _, _, _, _ = urlparse(str(identifier))
            creator.name_identifiers.append(
                NameIdentifier(
                    name_identifier=str(identifier),
                    name_identifier_scheme=netloc.split(".")[0].upper(),
                    scheme_uri=AnyUrl(f"{scheme}://{netloc}"),
                )
            )

    if isinstance(author, Person):
        creator.affiliation = []
        for affiliation in (
            author.affiliation
            if isinstance(author.affiliation, list)
            else [author.affiliation]
        ):
            if affiliation.identifier:
                for identifier in (
                    affiliation.identifier
                    if isinstance(affiliation.identifier, list)
                    else [affiliation.identifier]
                ):
                    scheme, netloc, _, _, _, _ = urlparse(str(identifier))
                    creator.affiliation.append(
                        Affiliation(
                            affiliation_identifier=str(identifier),
                            affiliation_identifier_scheme=netloc.split(".")[0].upper(),
                            scheme_uri=AnyUrl(f"{scheme}://{netloc}"),
                        )
                    )


@transpiler_plugin(
    name="cwl2datacite",
    description="CWL 2 DataCite Transpiler-Mate Plugin.",
    options_model=CWL2DataCiteOptions,
)
def cwl2datacite(context: TranspilerContext, options: CWL2DataCiteOptions) -> None:
    """CWL 2 DataCite Transpiler-Mate Plugin."""
    metadata_source: SoftwareApplication = context.metadata

    datacite_attributes: DataCiteAttributes = DataCiteAttributes(
        doi=str(metadata_source.identifier) if metadata_source.identifier else None,
        types=ResourceType(
            resource_type=metadata_source.name,
            resource_type_general=ResourceTypeGeneral.SOFTWARE,
        ),
        identifiers=[
            Identifier(
                identifier_type="DOI", identifier=str(metadata_source.identifier)
            )
            if metadata_source.identifier
            else Identifier(
                identifier_type="URN", identifier=f"urn:uuid:{uuid.uuid4()}"
            )
        ],  # supply a fake required identifier if the DOI hasn't been associated yet
        related_identifiers=[
            RelatedIdentifier(
                related_identifier=str(metadata_source.same_as),
                related_identifier_type=RelatedIdentifierType.DOI,
                relation_type=RelationType.IS_IDENTICAL_TO,
                resource_type_general=ResourceTypeGeneral.SOFTWARE,
            )
        ]
        if metadata_source.same_as
        else [],
        titles=[Title(title=metadata_source.name)],
        descriptions=[
            Description(
                description=metadata_source.description,
                description_type=DescriptionType.TECHNICAL_INFO,
            )
        ],
        publisher=Publisher(name=metadata_source.publisher.name),
        publication_year=metadata_source.date_created.year,
        dates=[
            Date(
                date=date.fromtimestamp(time.time()),
                date_type=DateType.UPDATED,
                date_information="New version release",
            )
        ],
        rights_list=[
            Right(
                rights=metadata_source.license.name
                or str(
                    metadata_source.license.identifier
                    or metadata_source.license.url
                    or metadata_source.license
                )
                if isinstance(metadata_source.license, CreativeWork)
                else str(metadata_source.license),
                rights_uri=metadata_source.license.url
                if isinstance(metadata_source.license, CreativeWork)
                else None,
                rights_identifier=str(metadata_source.license.identifier)
                if isinstance(metadata_source.license, CreativeWork)
                else None,
                rights_identifier_scheme="SPDX",
            )
        ]
        if metadata_source.license
        else None,
        creators=list(
            map(
                _to_creator,
                metadata_source.author
                if isinstance(metadata_source.author, list)
                else [metadata_source.author],
            )
        ),
        contributors=list(
            map(
                _to_contributor,
                metadata_source.contributor
                if isinstance(metadata_source.contributor, list)
                else [metadata_source.contributor],
            )
        )
        if metadata_source.contributor
        else None,
    )

    try:
        datacite_data: Mapping[str, Any] = datacite_attributes.model_dump(
            mode="json", exclude_none=True, by_alias=True
        )

        options.output.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Serializing DataCite metadata to {options.output.absolute()}")

        with options.output.open("w") as output_stream:
            json.dump(datacite_data, output_stream, indent=2)

        logger.success(
            f"DataCite metadata successfully serialized to {options.output.absolute()}"
        )
    except Exception as e:
        raise PluginExecutionError(
            f"An error occurred when serializing to {options.output.absolute()}, see nested exception"
        ) from e
