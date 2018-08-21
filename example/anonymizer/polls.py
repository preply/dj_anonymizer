from __future__ import absolute_import

from dj_anonymizer import anonym_field
from dj_anonymizer.register_models import AnonymBase, register_anonym

from polls.models import Question, Choice


class QuestionAnonym(AnonymBase):
    question_text = anonym_field.string("Jon Dou {seq}")

    class Meta:
        exclude_fields = ["pub_date"]


register_anonym([
    (Question, QuestionAnonym),
])
