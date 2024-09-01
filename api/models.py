from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class FirebaseUser(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, default=None)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    photo_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name or self.email or self.uid
    
class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Coupon(models.Model):
    amount = models.IntegerField(default=0)
    method_name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='./media', default=None)
    rate= models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return str(self.amount)


class WithdrawlRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, default='pending')
    def coupon_method(self):
        # Your custom logic here
        return self.coupon.method_name


class Game(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='./media')
    game_type=models.CharField(choices=[("Premium", "Premium"), ("Free", "Free")], default="Free", max_length=255)
    def __str__(self):
        return self.name
    
class Match(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=datetime.now())
    end_time = models.DateTimeField(default=datetime.now() + timedelta(hours=24))
    prize_per_game_play = models.DecimalField(max_digits=5, decimal_places=2, default=0.05)
    credentials = models.CharField(default=None, null=True, max_length=255)
    
    
    def __str__(self):
        return self.game.name + f" ({str(self.start_time)})"
    
class GameParticipant(models.Model):                         
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    number_of_gameplay = models.IntegerField(default=0)
    is_winner = models.BooleanField(default=False)