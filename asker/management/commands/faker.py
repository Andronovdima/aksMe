from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from asker.models import Question, Profile,Tag,Answer, Like
from faker import Faker
from random import choice, sample, randint

fake = Faker();


class Command(BaseCommand):
    def add_arguments (self , parser):
        parser.add_argument('--questions' , type = int)
        parser.add_argument('--users', type=int)
        parser.add_argument('--tags', type=int)
        parser.add_argument('--answers', type=int)
        parser.add_argument('--likes', type=int)

    @transaction.atomic()
    def handle(self, *args, **options):
        users_cnt = options['users']
        questions_cnt = options['questions']
        tags_cnt = options['tags']
        answers_cnt = options['answers']
        likes_cnt = options['likes']

        if users_cnt is not None:
            self.generate_users(users_cnt)

        if tags_cnt is not None:
            self.generate_tags(tags_cnt)

        if questions_cnt is not None:
            self.generate_questions(questions_cnt)

        if answers_cnt is not None:
            self.generate_answers(answers_cnt)

        if likes_cnt is not None:
            self.generate_likes(likes_cnt)

    def generate_users(self, users_cnt):
        print(f"GENERATE USERS {users_cnt}")
        for i in range(users_cnt):
            u = User.objects.create_user(
                username=fake.user_name() + str(i),
                email=fake.email(),
                password='pass')
            Profile.objects.create(user=u)
        print("OK")

    def generate_questions(self, questions_cnt):
        print("GENERATE_QUESIONS", questions_cnt)
        uids = list(Profile.objects.values_list('id', flat=True))
        tids = list(Tag.objects.values_list('id', flat=True))
        for i in range(questions_cnt):
            r = randint(1, 3)
            tag_ids = sample(tids, r)
            q = Question.objects.create(
                author_id=choice(uids),
                title=fake.sentence(),
                text='\n'.join(fake.sentences(fake.random_int(2, 5))),
            )
            q.save()
            for j in range(r):
                q.tags.add(tag_ids[j])
        print("OK")


    def generate_tags(self,tags_cnt):
        print("GENERATE_TAGS", tags_cnt)
        for i in range(tags_cnt):
            Tag.objects.create(
                tagname=fake.word() + str(i),
            )

    def generate_answers (self, answers_cnt):
        print("Generating_Answers", answers_cnt)
        uids = list(Profile.objects.values_list('id', flat=True))
        qids = list(Question.objects.values_list('id', flat=True))
        for i in range(answers_cnt):
            Answer.objects.create(
                author_id=choice(uids),
                text='\n'.join(fake.sentences(fake.random_int(2, 5))),
                correct=fake.boolean(chance_of_getting_true=50),
                question_id=choice(qids),
                rating=fake.random_int(0, 1000)
            )
        print("OK")

    def generate_likes(self, likes_cnt):
        print("Generating_Likes", likes_cnt)
        uids = list(Profile.objects.values_list('id', flat=True))
        qids = list(Question.objects.values_list('id', flat=True))
        aids = list(Answer.objects.values_list('id', flat=True))
        for i in range(likes_cnt):
            ch = randint(1, 2)
            if (ch == 1):
                Like.objects.create(
                    author_id=choice(uids),
                    question_id=choice(qids),
                )
            elif (ch == 2):
                Like.objects.create(
                    author_id=choice(uids),
                    answer_id=choice(aids),
                )
        print("OK")

