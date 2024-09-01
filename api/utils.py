from  .models import *
from .serializer import *
from django.utils import timezone
from django.contrib import messages
from django.utils.timezone import now

def getFirebaseUser(request):
    serializer = FirebaseUserSerializer(FirebaseUser.objects.get(user = request.user))
    return serializer.data


def getMatches(request):
    matches = Match.objects.filter(end_time__gt=timezone.now(), start_time__lt=timezone.now())
    serializer = MatchSerializer(matches, many=True)

    return serializer.data

def getNumberOfGameplays(match):
    gameParticipant = GameParticipant.objects.filter(match_id=match['id'])
    gameplays = 0
    for i in gameParticipant:
        gameplays += i.number_of_gameplay
    return gameplays

def sendNotification(user):
    pass

def joiMatch(request):
    match = Match.objects.get(id=request.data['match_id'])
    partcipent, created = GameParticipant.objects.get_or_create(match=match, user=request.user)
    if not created:
        if partcipent.score < request.data['score']:
            partcipent.score = request.data['score']
    else:
        partcipent.score = request.data['score']

    partcipent.number_of_gameplay += 1
    partcipent.save()
    serializer = GameParticipantSerializer(partcipent)
    return serializer.data

def getPartcipants(match_id):
    firebaseUsers = FirebaseUser.objects.all()
    gameParticipant = GameParticipant.objects.filter(match_id=match_id)
    serializer = GameParticipantSerializer(gameParticipant, many=True)
    datas = serializer.data
    
    for data in datas:
        data["user"] = FirebaseUserSerializer(firebaseUsers.get(user__username=data["user"])).data

    print(datas)
    

    return datas

    
def calculatePrize(match_id):
    matche = Match.objects.get(id= match_id)
    participants = GameParticipant.objects.filter(match=matche)
    total_games = sum([x.number_of_gameplay for x in participants])

    prize = matche.prize_per_game_play * total_games
    return prize
    

def mark_as_winner(modeladmin, request, queryset):
    for participant in queryset:
        if participant.match.end_time > now():
            messages.warning(request, "Match not finished yet for {}".format(participant.match))
            continue  # Skip marking this participant as a winner if the match is not finished
        if participant.is_winner == True:
            return
        participant.is_winner = True
        participant.save()
        wallet, created = Wallet.objects.get_or_create(user_id=participant.user.id)
        wallet.balance += calculatePrize(participant.match.id)
        wallet.save()
        sendNotification(None)
        messages.success(request, "Winner marked")

mark_as_winner.short_description = "Mark selected participants as winners"

def unmark_as_winner(modeladmin, request, queryset):
    for participant in queryset:
        if participant.match.end_time > now():
            messages.warning(request, "Match not finished yet for {}".format(participant.match))
            continue  # Skip marking this participant as a winner if the match is not finished
        if participant.is_winner == False:
            return
        participant.is_winner = False
        participant.save()
        
        wallet, created = Wallet.objects.get_or_create(user_id=participant.user.id)
        prz = calculatePrize(participant.match.id)
        
        if wallet.balance >= prz:
            wallet.balance -= prz
            wallet.save()
        messages.warning(request, "Winner unmarked")

unmark_as_winner.short_description = "Unmark selected participants as winners"


def getWallet(request, serialized = True):
    wallet, created = Wallet.objects.get_or_create(user_id=request.user.id)
    serializer = WalletSerializer(wallet)
    return serializer.data if serialized else wallet

def paid(modeladmin, request, queryset):
    for payrequests in queryset:
        if payrequests.status == "Cancelled":
            continue
        payrequests.status = "Paid"
        payrequests.save()
paid.short_description = "Mark as paid"

def refund(modeladmin, request, queryset):
    for payrequests in queryset:
        if payrequests.status == "Cancelled":
            continue
        payrequests.status = "Cancelled"
        payrequests.save()
        userWallet = Wallet.objects.get(user = payrequests.user)
        userWallet.balance += payrequests.coupon.amount
        userWallet.save()
refund.short_description = "Mark as Cancelled"


def unpaid(modeladmin, request, queryset):
    for payrequests in queryset:
        if payrequests.status == "Cancelled":
            continue
        payrequests.status = "Pending"
        payrequests.save()
unpaid.short_description = "Mark as unpaid"


def getcoupons(request):
    coupons = Coupon.objects.all()
    serializer = CouponSerilizer(coupons, many=True)
    return serializer.data


def getWithdrawalHistory(request):
    withdrawalHistory = WithdrawlRequest.objects.filter(user=request.user).order_by('-id')
    serializer = WithdrawlRequestSerializer(withdrawalHistory, many=True)
    return serializer.data