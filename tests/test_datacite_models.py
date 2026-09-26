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

import json
from datetime import date

from cwl2datacite.datacite_4_6_models import Date, DateType


def test_date_model_can_be_constructed_and_serialized() -> None:
    value = Date(
        date=date(2026, 8, 26),
        date_type=DateType.UPDATED,
        date_information="New version release",
    )

    compacted = value.model_dump(mode="json", by_alias=True)

    assert compacted == {
        "date": "2026-08-26",
        "dateType": "Updated",
        "dateInformation": "New version release",
    }
    assert json.dumps(compacted)
