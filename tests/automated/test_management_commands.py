import json

import pytest
from django.core.management import call_command

from core.models import Option, Question, Subject


@pytest.mark.django_db
@pytest.mark.integration
def test_import_questions_command_uses_current_option_model(tmp_path):
    subject = Subject.objects.create(
        name='Pathology',
        code='PATH',
        description='Command test subject',
        year_applicable='all',
        is_active=True,
    )
    import_file = tmp_path / 'questions.json'
    import_file.write_text(
        json.dumps(
            [
                {
                    'topic': 'Inflammation',
                    'question': 'Which cell is most abundant in acute inflammation?',
                    'difficulty': 'easy',
                    'explanation': 'Neutrophils dominate early acute inflammation.',
                    'reference': 'Robbins',
                    'options': ['Lymphocyte', 'Neutrophil', 'Plasma cell', 'Eosinophil'],
                    'correct_answer': 1,
                }
            ]
        ),
        encoding='utf-8',
    )

    call_command(
        'import_questions',
        file=str(import_file),
        format='json',
        subject=subject.code,
    )

    question = Question.objects.get(topic__subject=subject, topic__name='Inflammation')
    assert question.question_text == 'Which cell is most abundant in acute inflammation?'
    assert Option.objects.filter(question=question).count() == 4
    assert question.correct_option.option_text == 'Neutrophil'

