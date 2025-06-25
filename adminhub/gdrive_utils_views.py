from .drive_service import upload_file_to_folder
from django.shortcuts import render
from .decorators import role_required
import tempfile 
import os

@role_required('administrator')
def test_upload_to_drive(request):
    upload_result = None

    if request.method == 'POST' and request.FILES.get('upload_file'):
        uploaded_file = request.FILES['upload_file']

        # Get a safe temp path for your OS
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, uploaded_file.name)
        
        try:
            with open(file_path, 'wb+') as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)

            folder_id = 'YOUR_GOOGLE_FOLDER_ID_HERE'
            file_id, link = upload_file_to_folder(
                file_path, uploaded_file.name, uploaded_file.content_type, folder_id
            )
            upload_result = f'✅ Upload successful! <a class="text-blue-600 underline" href="{link}" target="_blank">View on Google Drive</a>'
        except Exception as e:
            upload_result = f"<span class='text-red-600'>❌ Upload failed: {str(e)}</span>"

    return render(request, 'adminhub/test_upload.html', {'upload_result': upload_result})

