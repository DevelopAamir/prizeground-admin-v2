from django.contrib import admin
from .models import *
from .utils import *
from django.contrib import messages






# Register your models here.

admin.site.register(FirebaseUser)
admin.site.register(Game)
admin.site.register(Match)
class GameParticipantAdmin(admin.ModelAdmin):
    list_display = ('match', 'user', 'score','number_of_gameplay', 'is_winner')
    ordering = ['-score']
    actions = [mark_as_winner, unmark_as_winner]
    list_filter = ['match']
admin.site.register(GameParticipant, GameParticipantAdmin)

class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')

admin.site.register(Wallet, WalletAdmin)

class CouponAdmin(admin.ModelAdmin):
    list_display = ('amount', 'method_name')

admin.site.register(Coupon, CouponAdmin)

class WidthdrawRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'coupon', 'created_at', 'status', 'coupon_method')
    actions = [paid,refund, unpaid]
    list_filter = ['status', 'coupon']

admin.site.register(WithdrawlRequest, WidthdrawRequestAdmin)