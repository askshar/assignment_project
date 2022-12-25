from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UserFile, FileText



def index(request):
    # Filtering all files, uploaded by current user(request.user)
    user = request.user
    user_files = user.userfile_set.all().order_by('-uploaded_at')
    file_count = user_files.count()

    context = {'user_files': user_files, 'file_count': file_count}
    return render(request, 'base/index.html', context)


def upload_file(request):

    # Handles file uploads and create a new file object in database
    if request.method == 'POST':
        file = request.FILES['doc']
        user = request.user

        file_exc = str(file)
        if (file_exc.split('.')[-1].lower()) == 'pdf':
            new_file = UserFile.objects.create(
                user=user,
                file=file,
                filename=file
            )
            new_file.save()
            messages.success(request, "File uploaded.")
            return redirect('index')
        else:
            messages.info(request, 'Please select \'pdf\' file')
            return redirect('upload_file')

    # Handles text extraction from uploaded file and save in text database model

    """Code goes here"""

    return render(request, 'base/upload_file.html')


def file_detail(request, file_id):

    file_obj = get_object_or_404(UserFile, id=file_id)
    file = file_obj.file
    filename = file_obj.filename
    uploaded = file_obj.uploaded_at

    context = {'file': file, 'filename': filename, 'uploaded': uploaded}
    return render(request, 'base/file_detail.html', context)