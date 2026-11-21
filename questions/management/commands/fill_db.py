import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from faker import Faker
from questions.models import Question, Answer, QuestionLike, AnswerLike
from core.models import Tag

fake = Faker('ru_RU')

class Command(BaseCommand):
    help = 'Заполняет базу тестовыми данными'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Коэффициент пропорциональности')

    @transaction.atomic
    def handle(self, *args, **options):
        ratio = options['ratio']
        self.stdout.write(f'Генерация данных с ratio={ratio}...')

        # 1. Пользователи
        users = []
        for _ in range(ratio):
            user = User(username=fake.unique.user_name(), email=fake.email())
            user.set_password('password123')
            users.append(user)
        User.objects.bulk_create(users)
        users = list(User.objects.all())

        # 2. Теги
        tags = []
        for _ in range(ratio):
            tags.append(Tag(name=fake.unique.word()))
        Tag.objects.bulk_create(tags)
        tags = list(Tag.objects.all())

        # 3. Вопросы
        questions = []
        for _ in range(ratio * 10):
            questions.append(Question(
                title=fake.sentence(nb_words=6),
                text=fake.paragraph(nb_sentences=3),
                author=random.choice(users)
            ))
        Question.objects.bulk_create(questions)
        questions = list(Question.objects.all())

        # 4. Связь вопросов и тегов
        question_tags = []
        for q in questions:
            selected_tags = random.sample(tags, k=random.randint(1, 3))
            for tag in selected_tags:
                question_tags.append(q.tags.through(question_id=q.id, tag_id=tag.id))
        Question.tags.through.objects.bulk_create(question_tags)

        # 5. Ответы
        answers = []
        for _ in range(ratio * 100):
            answers.append(Answer(
                question=random.choice(questions),
                text=fake.paragraph(nb_sentences=2),
                author=random.choice(users),
                is_correct=random.choice([True, False, False, False])
            ))
        Answer.objects.bulk_create(answers)
        answers = list(Answer.objects.all())

        # 6. Лайки вопросов
        q_likes = []
        for _ in range(ratio * 200):
            q_likes.append(QuestionLike(
                user=random.choice(users),
                question=random.choice(questions),
                value=random.choice([1, -1])
            ))
        QuestionLike.objects.bulk_create(q_likes, ignore_conflicts=True)

        # 7. Лайки ответов
        a_likes = []
        for _ in range(ratio * 200):
            a_likes.append(AnswerLike(
                user=random.choice(users),
                answer=random.choice(answers),
                value=random.choice([1, -1])
            ))
        AnswerLike.objects.bulk_create(a_likes, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS('База успешно заполнена!'))