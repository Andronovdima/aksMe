from django.db import models
# from django.conctrib.auth.models import User
# from django.conf import settings
# Create your models here.

#
# class Profile (models.Model):
# 	# user = models.OnetoOneField(to = User , on_delete = models.CASCADE)
# 	user = models.OnetoOneField(settings.AUTH_USER_MODEL , on_delete = models.CASCADE)
# 	raiting = models.IntegerField (default = 0)
#
# 	def __str__ (self) :
# 		return self.user.username
#


class Question(models.Model):
    # objects = QuestionManager
    # author = models.ForeignKey(
    #     to = Profile , on_delete=models.CASCADE
    # )
    title = models.CharField(max_length = 128)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)




class Answers (models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question , on_delete = models.CASCADE)


class Profile (models.Model):
    login = models.CharField(max_length = 128)