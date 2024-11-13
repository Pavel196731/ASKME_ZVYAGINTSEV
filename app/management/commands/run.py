from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import random

from django.db import IntegrityError, connection
from faker import Faker

from app.models import Tag, Profile, Question, Answer, QuestionLike, AnswerLike


class Command(BaseCommand):
    help = "Fill the database with test data using the given ratio"

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio of data population')

    def handle(self, *args, **options):
        fake = Faker()
        ratio = options['ratio']
        print('Hello1')
        usernames = set()
        users = []
        existing_usernames = set(User.objects.values_list('username', flat=True))
        while len(users) < ratio:
            username = fake.user_name()
            if username not in usernames and username not in existing_usernames:
                usernames.add(username)
                users.append(User(username=username))

        User.objects.bulk_create(users)
        saved_users = User.objects.filter(username__in=usernames)

        profiles = [Profile(user=user, avatar=fake.image_url()) for user in saved_users]
        Profile.objects.bulk_create(profiles)

        print('Hello2')
        tags = []
        for _ in range(ratio):
            tag_name = fake.word()
            tag, created = Tag.objects.get_or_create(tag=tag_name)
            tags.append(tag)
        print('Hello3')
        questions = []
        for i in range(ratio * 10):
            question = Question(
                user=random.choice(saved_users),
                title=fake.sentence(),
                text=fake.text(),
            )
            questions.append(question)

        Question.objects.bulk_create(questions)
        saved_questions = Question.objects.all()

        print('Hello4')
        answers = []
        for i in range(ratio * 100):
            answer = Answer(
                question=random.choice(saved_questions),
                user=random.choice(saved_users),
                text=fake.text()
            )
            answers.append(answer)

        Answer.objects.bulk_create(answers)

        question_likes = []
        for _ in range(ratio * 200):
            user = random.choice(users)
            question = random.choice(questions)
            if not QuestionLike.objects.filter(user=user, question=question).exists():
                question_like = QuestionLike.objects.create(user=user, question=question)
                question_likes.append(question_like)

        answer_likes = []
        for _ in range(ratio * 200):
            user = random.choice(users)
            answer = random.choice(answers)
            if not AnswerLike.objects.filter(user=user, answer=answer).exists():
                answer_like = AnswerLike.objects.create(user=user, answer=answer)
                answer_likes.append(answer_like)
        print('Hello5')

        self.stdout.write(self.style.SUCCESS('Database has been filled with test data using ratios'))
