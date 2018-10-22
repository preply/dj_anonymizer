from __future__ import absolute_import

import datetime

from dj_anonymizer import anonym_field
from dj_anonymizer.register_models import (
    AnonymBase,
    register_anonym,
    register_skip
)
from polls.models import Choice, Question


class QuestionAnonym(AnonymBase):
    question_text = anonym_field.string("John Doe {seq}")
    pub_date = anonym_field.function(datetime.datetime.now)


register_anonym([
    (Question, QuestionAnonym),
])


register_skip([
    Choice
])
