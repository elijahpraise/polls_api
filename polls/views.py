from django.shortcuts import render, get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status

from polls.models import *
from polls.serializers import *


class ChoiceList(generics.ListCreateAPIView):

    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs["pk"])
        return queryset
    serializer_class = ChoiceSerializer

    def post(self, request, *args, **kwargs):
        polls = Poll.objects.get(pk=self.kwargs["pk"])
        if not request.user == polls.created_by:
            raise PermissionDenied("You can not delete this poll.")
        return super().post(request, *args, **kwargs)


class CreateVote(APIView):
    serializer_class = ChoiceSerializer

    def post(self, request, pk, choice_pk):
        voted_by = request.data.get("voted_by")
        data = {'choice': choice_pk, 'poll': pk, 'voted_by': voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






