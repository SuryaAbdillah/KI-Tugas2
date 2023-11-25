from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from postingans.forms import EncryptedFileForm, KeyForm
from cryptography.fernet import Fernet
from django.http import HttpResponse, HttpResponseForbidden
from postingans.models import Postingans
from .utils import encrypt_file, decrypt_file
from django.contrib.auth.decorators import login_required

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = EncryptedFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Associate the postingans with the current user
            postingans = form.save(commit=False)
            postingans.user = request.user
            postingans.save()
            return redirect('success_page')
    else:
        form = EncryptedFileForm()
    return render(request, 'upload_file.html', {'form': form})

def display_file(request, file_id):
    custom_file = get_object_or_404(Postingans, id=file_id)

    # Retrieve the encryption key from the database as bytes
    encryption_key = custom_file.encryption_key

    # Create a Fernet cipher suite using the retrieved encryption key
    cipher_suite = Fernet(encryption_key)

    # Decrypt the file data
    decrypted_file_data = decrypt_file(custom_file.encrypted_file.read(), cipher_suite)

    # You can create a response to display or download the decrypted file
    response = HttpResponse(decrypted_file_data, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{custom_file.title}"'

    return response


@login_required
def success_page(request):
    return render(request, 'success_page.html')

@login_required
def postingans_list(request):
    postingans_list = Postingans.objects.all()
    return render(request, 'postingans_list.html', {'postingans_list': postingans_list})

@login_required
def user_postingans(request):
    user_postingans = Postingans.objects.filter(user=request.user)
    return render(request, 'user_postingans.html', {'user_postingans': user_postingans})

@login_required
def download_key(request, postingans_id):
    postingans = get_object_or_404(Postingans, id=postingans_id, user=request.user)

    # You should implement a secure way to provide the key to the user.
    # For demonstration purposes, this example returns a text response.
    response = HttpResponse(postingans.encryption_key, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{postingans.title}_key.txt"'
    return response

@login_required
def send_encryption_key_email(request, postingans_id):
    postingans = get_object_or_404(Postingans, id=postingans_id)

    # You should implement a secure way to send the key to the user via email.
    # For demonstration purposes, this example sends an email with the encryption key.
    subject = 'Your Encryption Key'
    message = f'Please find your encryption key attached.\n\nKey: {postingans.encryption_key.decode()}'
    from_email = 'suryaabdillah4@gmail.com'  # Update with your email
    to_email = [request.user.email]

    send_mail(subject, message, from_email, to_email, fail_silently=False)

    return HttpResponse('Email sent successfully!')

def download_with_key(request, postingans_id):
    postingans = get_object_or_404(Postingans, id=postingans_id)
    actual_key = ''

    if request.method == 'POST':
        form = KeyForm(request.POST)
        if form.is_valid():
            input_key = form.cleaned_data['input_key']

            # Convert the actual key to a string for comparison
            actual_key = postingans.encryption_key.decode()

            if input_key == actual_key:
                # Decrypt the file content
                decrypted_content = decrypt_file(postingans.encrypted_file.read(), actual_key)

                # Set appropriate content headers for the response
                response = HttpResponse(content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{postingans.title}.{postingans.file_format}"'

                # Write the decrypted file content to the response
                response.write(decrypted_content)

                return response
            else:
                return HttpResponseForbidden('Incorrect encryption key.')
    else:
        form = KeyForm()

    return render(request, 'download_with_key.html', {'form': form, 'actual_key': actual_key, 'key_inputted': False})