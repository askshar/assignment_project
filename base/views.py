from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UserFile, FileText

import os
import io
from PIL import Image
import pytesseract
from wand.image import Image as wi



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
		validator = file_exc.split('.')[-1].lower()
		if validator == 'png' or validator == 'jpeg' or validator == 'jpg' or validator == 'pdf':
			new_file = UserFile.objects.create(
				user=user,
				file=file,
				filename=file
			)
			new_file.save()

			# Handles text extraction from uploaded file and save in text database model

			"""Code goes here"""

			pdfFile = wi(filename = f"docs/user_uploads/{file}", resolution = 300)
			image = pdfFile.convert('jpeg')

			imageBlobs = []

			for img in image.sequence:
				imgPage = wi(image = img)
				imageBlobs.append(imgPage.make_blob('jpeg'))

			extract = []

			for imgBlob in imageBlobs:
				image = Image.open(io.BytesIO(imgBlob))
				text = pytesseract.image_to_string(image, lang = 'eng')
				extract.append(text)
			file_text = ""
			for i in extract:
				file_text+=i
			extracted_file_text = FileText(file=new_file, filename=new_file.filename, text=file_text)
			extracted_file_text.save()
			messages.success(request, 'File uploaded successfully.')
			return redirect('index')


			"""Code ends here"""

		else:
			messages.info(request, 'This file format not supported, choose a valid file format.')
			return redirect('upload_file')

	return render(request, 'base/upload_file.html')


def file_detail(request, file_id):

	file_obj = get_object_or_404(UserFile, id=file_id)
	file = file_obj.file
	file_text = file_obj.filetext
	filename = file_obj.filename
	uploaded = file_obj.uploaded_at

	context = {'file': file, 'filename': filename, 'uploaded': uploaded, 'text': file_text.text}
	return render(request, 'base/file_detail.html', context)