from django.core.files.storage import default_storage
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from functools import wraps
import os



API_KEYS = {
    'ApiKeyForUser1': 'Spider-Man',
    'ApiKeyForUser2': 'From-Local',
}

valid_statuses =['vehcle','person','no_face','New']


def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        request = args[1]
        api_key = request.headers.get('X-API-KEY')
        if api_key not in API_KEYS:
            return Response({'message': 'Invalid API Key'}, status=status.HTTP_403_FORBIDDEN)
        request.user = API_KEYS[api_key] 
        return f(*args, **kwargs)
    return decorated


class FileUploadView(APIView):

    @api_key_required
    def post(self, request, format=None):
        file = request.FILES.get('file')
        if not file:
            return Response({'message': 'No file part'}, status=status.HTTP_400_BAD_REQUEST)
        
        file_id = request.POST.get('id')  # or request.GET.get('id') if sent as a query parameter
        file_status = request.POST.get('status')  # same as above


        if not file_id or not file_id.isdigit() or len(file_id) != 4 :
            return Response({'message': 'Invalid id. ID must be a 6-digit number.'}, status=status.HTTP_400_BAD_REQUEST)

        if file_status not in valid_statuses:
            return Response({'message': 'Invalid status. Status must be either "Active" or "Deactivate".'}, status=status.HTTP_400_BAD_REQUEST)
        
        # print(file_id)
        # print(file_status)


        user_folder = os.path.join(settings.MEDIA_ROOT, request.user)
        id_folder = os.path.join(user_folder, file_id,file_status)
        os.makedirs(id_folder, exist_ok=True)
        filename = os.path.join(id_folder, file.name)

        with default_storage.open(filename, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return Response({'message': 'File uploaded successfully'}, status=status.HTTP_200_OK)


class UploadedFilesView(APIView):

    @api_key_required
    def get(self, request, format=None):
        user_folder = os.path.join(settings.MEDIA_ROOT, request.user)
        if not os.path.exists(user_folder):
            return Response({'message': 'No files found'}, status=status.HTTP_404_NOT_FOUND)

        files = os.listdir(user_folder)
        return Response({'files': files}, status=status.HTTP_200_OK)


# Ensure the media root directory exists
if not os.path.exists(settings.MEDIA_ROOT):
    os.makedirs(settings.MEDIA_ROOT)
