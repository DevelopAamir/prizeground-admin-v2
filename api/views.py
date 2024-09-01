from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from prizeground.custom_auth import FirebaseAuthentication
from .utils import *
from rest_framework import status 
 
class LoginView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]

    def get(self, request):
        current_user = getFirebaseUser(request)
        return Response({'message': 'Login', "data": current_user})
    
    def post(self, request):
        if request.user:
            current_user = getFirebaseUser(request)
            return Response({'message': 'Login', 'data': current_user}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class Matches(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]

    def get(self, request):
        try:
            matches = getMatches(request)
            for match in matches:
                gameplays = getNumberOfGameplays(match)
                match["gameplays"] = gameplays
            return Response({'message': 'Matches', 'data': matches}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class JoinMatch(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]

    def get(self, request):
        print(request.query_params["match_id"])
        totalParticipants = getPartcipants(request.query_params["match_id"])
        return Response({'message': 'Matches', 'totalParticipants': totalParticipants}, status=status.HTTP_200_OK)

    def post(self, request):
        if request.data['match_id'] == None or request.data['score'] == None:
            return Response({"message": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            partcipent = joiMatch(request)
            totalParticipants = getPartcipants(request.data['match_id'])
            return Response({'message': 'Joined Match', 'data': partcipent, 'totalParticipants': totalParticipants}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class LoadWallet(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]

    def get(self, request):
        try:
            wallet = getWallet(request)
            return Response({'message': 'Wallet', 'data': wallet}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        wallet = getWallet(request, serialized=False)
        coupon = Coupon.objects.get(id= request.data["coupon_id"])

        if wallet.balance < coupon.amount / coupon.rate:
            return Response({"message": "Insufficient Balance"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            withdrawlRequest = WithdrawlRequest.objects.create(user=request.user, coupon= coupon)
            wallet.balance -= coupon.amount
            wallet.save()
            return Response({'message': 'Withdrawl Request Submitted'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class LoadCoupons(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]
    def get(self, request):
        try:
            coupons = getcoupons(request)
            return Response({'message': 'Coupons', 'data': coupons}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        

class Profile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]
    def get(self, request):
        try:
            withdraws =  getWithdrawalHistory(request)
            print(withdraws)
            req =  getFirebaseUser(request)
            return Response({'message': 'Profile', 'data': req, "withdraws": withdraws}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)