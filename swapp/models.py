from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as l

def val(value):
    if value > 10 or value < 6:
        raise ValidationError(
            l('Valutazione inesistente. Inserisci un valore da 6 a 10.'),
        )

class Usernew(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        coins = models.IntegerField()
        liv = models.IntegerField()
        coins_earned = models.IntegerField()
        coins_spent = models.IntegerField()
        asks_resolved = models.IntegerField()
        asks_made = models.IntegerField()
        evaluation = models.IntegerField()
        def __str__(self):
            return self.user.get_username()

class Ask(models.Model):
    done = models.BooleanField(default=False)
    coins = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=30)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    file = models.ImageField(blank=True, null=True, upload_to="img")
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE, blank=True, null=True)
    usernew = models.ForeignKey(Usernew, related_name="usernew", on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.title

class Reply(models.Model):
    done = models.BooleanField(default=False)
    yn = models.BooleanField(default=False)
    ask = models.ForeignKey(Ask, on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    file = models.ImageField(blank=True, null=True, upload_to="img")
    from_user = models.ForeignKey(User, related_name="from_user", on_delete=models.CASCADE, blank=True, null=True)
    from_usernew = models.ForeignKey(Usernew, related_name="from_usernew", on_delete=models.CASCADE, blank=True, null=True)
    to_user = models.ForeignKey(User, related_name="to_user", on_delete=models.CASCADE, blank=True, null=True)
    to_usernew = models.ForeignKey(Usernew, related_name="to_usernew", on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.text
    def day_past(self):
        return not (self.date >= timezone.now() - datetime.timedelta(days=1))

class Bad(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.text

class Yes(models.Model):
    evaluation = models.IntegerField()
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.reply.text

class Solved(models.Model):
    bad = models.ForeignKey(Bad, on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField()
    coins_ask = models.IntegerField()
    coins_reply = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.text

class Chat(models.Model):
    user = models.ForeignKey(User, related_name="chat_user", on_delete=models.CASCADE, blank=True, null=True)
    usernew = models.ForeignKey(Usernew, related_name="chat_usernew", on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=500)
    text = models.TextField()
    done = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.text