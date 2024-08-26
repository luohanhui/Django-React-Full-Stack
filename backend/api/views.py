from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer,NoteSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]



# 创建 note
# ListCreateAPIView, do two things:
# listing all notes created by a user or create a new note
class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    # Cannot call this route, unless authenticated and pass a valid jwt token
    permission_classes = [IsAuthenticated]

    # overriding get_queryset(django docs)
    def get_queryset(self):
        user = self.request.user
        # get all notes written by this "user", that's what filter means
        return Note.objects.filter(author=user)

    # overriding perform_create(django docs)
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)

# 删除 note
class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

