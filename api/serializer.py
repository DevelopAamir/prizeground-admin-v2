from  rest_framework import serializers
from .models import *

class FirebaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirebaseUser
        fields = '__all__'



class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name', 'logo', 'game_type']

class MatchSerializer(serializers.ModelSerializer):
    game = GameSerializer(read_only=True)
    class Meta:
        model = Match
        fields = ['id', 'game', 'start_time', 'end_time', 'prize_per_game_play', 'credentials']

class GameParticipantSerializer(serializers.ModelSerializer):
    match = MatchSerializer(read_only=True)
    user = serializers.StringRelatedField()
    class Meta:
        model = GameParticipant
        fields = ['id', 'match', 'user', 'score', 'number_of_gameplay', 'is_winner']

class WalletSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance']

class CouponSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"

class WithdrawlRequestSerializer(serializers.ModelSerializer):
    coupon = CouponSerilizer(read_only = True)
    class Meta:
        model = WithdrawlRequest
        fields = "__all__"