from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from .models import Note, SharedNote, NoteChange
from .serializers import UserSerializer, LoginSerializer, NoteSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        Token.objects.create(user=user)  # Create a token for the new user
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(username=serializer.validated_data['username'],
                            password=serializer.validated_data['password'])
        if user:
            auth_login(request._request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_note(request):
    title = request.data["title"]
    content = request.data["content"]

    if not title or not content:
        return Response({'error': 'Title and content are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        note = Note.objects.create(
            title=title, content=content, owner=request.user)
        note.save()
        return Response({'message': 'Note created successfully'}, status=status.HTTP_201_CREATED)
    except:
        return Response({'error': 'Note could not be created'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def note_detail(request, id):
    if request.method == 'GET':
        try:
            note = Note.objects.get(id=id)
            if request.user == note.owner or SharedNote.objects.filter(note=note, user=request.user).exists():
                serializer = NoteSerializer(note)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': 'You do not have permission to access this note'}, status=status.HTTP_403_FORBIDDEN)
        except Note.DoesNotExist:
            return Response({'error': 'Note does not exist'}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == "PUT":
        try:
            note = Note.objects.get(id=id)
            if request.user == note.owner or SharedNote.objects.filter(note=note, user=request.user).exists():
                old_content = note.content
                new_content = request.data['content']
                note.content = new_content
                note.save()

                # Create a new NoteChange instance
                NoteChange.objects.create(
                    note=note,
                    user=request.user,
                    change_content=f'Changed from "{old_content}" to "{new_content}"'
                )
                return Response({'message': 'Note updated successfully'}, status=status.HTTP_200_OK)
            return Response({'error': 'You do not have permission to update this note'}, status=status.HTTP_403_FORBIDDEN)
        except Note.DoesNotExist:
            return Response({'error': 'Note does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def share_note(request):
    note_id = request.data.get('note_id')
    usernames = request.data.getlist('usernames')
    print("usernames:" + str(usernames))
    try:
        note = Note.objects.get(id=note_id)
        if request.user == note.owner:
            shared_users = User.objects.filter(username__in=usernames)
            print("shared_users:" + str(shared_users))
            for user in shared_users:
                SharedNote.objects.get_or_create(note=note,  user=user)
            return Response({'message': 'Note shared successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'You do not have permission to share this note'}, status=status.HTTP_403_FORBIDDEN)
    except Note.DoesNotExist:
        return Response({'error': 'Note does not exist'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_note_version_history(request, id):
    try:
        note = Note.objects.get(id=id)
        if request.user == note.owner or SharedNote.objects.filter(note=note, user=request.user).exists():
            changes = NoteChange.objects.filter(
                note=note).order_by('-timestamp')
            data = [{'timestamp': change.timestamp, 'user': change.user.username,
                     'change_content': change.change_content} for change in changes]
            return Response(data, status=status.HTTP_200_OK)
        return Response({'error': 'You do not have permission to access version history of this note'}, status=status.HTTP_403_FORBIDDEN)
    except Note.DoesNotExist:
        return Response({'error': 'Note does not exist'}, status=status.HTTP_404_NOT_FOUND)
