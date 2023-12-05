from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from postingans.forms import EncryptedFileForm, KeyForm
from cryptography.fernet import Fernet
from django.http import HttpResponse, HttpResponseForbidden
from postingans.models import Postingans
from .utils import encrypt_file, decrypt_file, encrypt, decrypt
from django.contrib.auth.decorators import login_required
from data.models import UserData

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

    # Get the recipient's public key from UserData
    user_data = get_object_or_404(UserData, user=request.user)
    recipient_public_key = user_data.public_key

    # Encrypt the postingans encryption key with the user's public key
    encrypted_key = encrypt(postingans.encryption_key, recipient_public_key)

    integer_value = int.from_bytes(encrypted_key, byteorder='big')

    # You should implement a secure way to send the encrypted key to the user via email.
    # For demonstration purposes, this example sends an email with the encrypted key.
    subject = 'Your Encrypted Encryption Key'
    message = f'Please find your encrypted encryption key attached.\n\nKey: {integer_value}'
    from_email = 'EMAIL ANDA'  # Update with your email
    to_email = [request.user.email]

    send_mail(subject, message, from_email, to_email, fail_silently=False)

    return HttpResponse('Email sent successfully!')

@login_required
def download_with_key(request, postingans_id):
    postingans = get_object_or_404(Postingans, id=postingans_id)
    actual_key = postingans.encryption_key  # The actual encryption key

    if request.method == 'POST':
        form = KeyForm(request.POST)
        if form.is_valid():
            input_key_str = form.cleaned_data['input_key']

            try:
                input_key = int(input_key_str)
            except ValueError:
                return HttpResponseForbidden('Invalid input key format. Please enter a valid integer.')
            
            # Convert the integer input_key to binary
            byte_sequence2 = input_key.to_bytes((input_key.bit_length() + 7) // 8, byteorder='big')
            user_data = get_object_or_404(UserData, user=request.user)
            
            # Convert the binary key back to an integer before decryption
            decrypted_actual_key = decrypt(byte_sequence2, user_data.private_key)

            # Convert the actual key to a string for comparison
            actual_key_str = actual_key.decode()

            if decrypted_actual_key == actual_key_str:
                # Decrypt the file content
                decrypted_content = decrypt_file(postingans.encrypted_file.read(), actual_key)

                # Set appropriate content headers for the response
                response = HttpResponse(content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{postingans.title}.{postingans.file_format}"'

                # Write the decrypted file content to the response
                response.write(decrypted_content)

                return response
            else:
                return HttpResponseForbidden('Incorrect decryption key.')
    else:
        form = KeyForm()

    # Render the download_with_key.html template with the form
    return render(request, 'download_with_key.html', {'form': form, 'actual_key': actual_key, 'key_inputted': False})
