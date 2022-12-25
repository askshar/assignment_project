from django.shortcuts import render, redirect
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

    if request.method == 'POST':
        file = request.FILES['doc']
        user = request.user

        new_file = UserFile.objects.create(
            user=user,
            file=file,
            filename=file
        )
        new_file.save()
        messages.success(request, "File uploaded.")
        return redirect('index')

    return render(request, 'base/upload_file.html')