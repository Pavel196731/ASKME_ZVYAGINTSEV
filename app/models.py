from django.contrib.auth.models import User
from django.db import models
from django.db.models import OneToOneField, ManyToManyField, ForeignKey


class QuestionManager(models.Manager):

    def get_question_by_id(self, question_id):
        return self.get(pk=question_id)

    def new(self):
        return self.order_by('-created_at')

    def get_best_questions(self):
        return self.annotate(likes_count=models.Count('likes')).order_by('-likes_count')

    def get_questions_by_tag_name(self, tag_name):
        return self.filter(tags__name=tag_name)


class TagManager(models.Manager):
    def get_popular_n_tags(self, n=5):
        return self.annotate(questions_count=models.Count('questions')).order_by('-questions_count')[:n]


class Profile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, null=True)

    def __str__(self):
        return str(self.user)


class Tag(models.Model):
    tag = models.CharField(max_length=100)



    objects = TagManager()

    def __str__(self):
        return self.tag

class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(max_length=1000)
    tags = ManyToManyField(Tag, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class AnswerManager(models.Manager):
    def get_answers_by_question_id(self, question_id):
        return self.filter(question_id=question_id).annotate(likes_count=models.Count('likes')).order_by('-is_accepted',
                                                                                                         '-likes_count')


class ProfileManager(models.Manager):
    def top_users(self, limit=10):
        return self.annotate(
            total_likes=models.Count('user__questions__likes', distinct=True) + models.Count('user__answers__likes',
                                                                                             distinct=True)).order_by(
            '-total_likes')[:limit]


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    objects = AnswerManager()

    class Meta:
        ordering = ['-created_at']


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"({self.question.title} -- {self.tag.tag})"


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'answer')

    def __str__(self):
        return f"{self.answer} - {self.user}"

