from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


class AnswerManager(models.Manager):
    def noth(self):
        return self.order_by('-rating')


class ProfileManager (models.Manager):
    def user_top(self):
        return self.order_by('-rating') [:8]


class QuestionManager (models.Manager):
    def new(self):
        return self.order_by ('-created_at')

    def hot(self):
        return self.order_by('-rating')

    def answers(self, question):
        return question.answer_set.all()

    def amount_answer(self, question):
        return len(question.answer_set.all())


class TagManager(models.Manager):
    def questions(self, tag):
        return tag.question_set.all().order_by('-rating')

    def popular_tags(self):
        return self.order_by('-count')[:20]



class Profile (models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    # avatar = models.ImageField(
        # upload_to='avatar/%Y/%m/%d',
        # default = 'avatar/default.jpg' #default avatar
        # height_field=64,
        # width_field=64,
        # max_length=100)
    objects = ProfileManager()

    def __str__(self):
        return self.user.username


class Tag (models.Model):
    tagname = models.CharField(max_length = 128)
    objects = TagManager()
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.tagname


class Question(models.Model):

    author = models.ForeignKey(
        to=Profile, on_delete=models.CASCADE
    )
    rating = models.IntegerField(default=0)
    title = models.CharField(max_length=128)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(to=Tag)
    objects = QuestionManager()

    def __str__(self):
        return self.title


class Answer (models.Model):
    author = models.ForeignKey(to=Profile, on_delete=models.CASCADE )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(to=Question , on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    objects = AnswerManager()

    def __str__(self):
        return self.question.title


class Like (models.Model):
    author = models.OneToOneField(to=Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(to=Answer, on_delete=models.CASCADE, null=True)


