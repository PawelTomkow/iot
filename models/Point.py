from dataclasses import dataclass
from datetime import datetime

import uuid as uuid
from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Point:
    x: float
    y: float
    z: float
    id: str
    time: str = str(datetime.today())
