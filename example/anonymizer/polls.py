from __future__ import absolute_import

import datetime

from dj_anonymizer import fields
from dj_anonymizer.register_models import (
    AnonymBase,
    register_anonym,
    register_skip
)
from polls.models import Choice, Question


class QuestionAnonym(AnonymBase):
    question_text = fields.string("John Doe {seq}")
    pub_date = fields.function(datetime.datetime.now)

    class Meta:
        pass


register_anonym([
    (Question, QuestionAnonym),
])


register_skip([
    Choice
])
