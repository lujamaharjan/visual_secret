from PIL import Image
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, View
import os
from numpy import *
from .encryption import imageEncryption, imageDecryption, changeImageToMatrix
from .models import EncryptionData


class HomeView(TemplateView):
    template_name = 'index.html'


class EncryptView(View):
    participants = [
        {"value": 3, "key": "Three"},
        {"value": 4, "key": "Four"},
        {"value": 5, "key": "Five"},
        {"value": 6, "key": "Six"},
        {"value": 7, "key": "Seven"},
        {"value": 8, "key": "Eight"},
        {"value": 9, "key": "Nine"}
    ]

    def get(self, request):
        return render(request, 'encrypt.html', {"participants": self.participants})

    def post(self, request):
        emails = []
        unique_string = request.POST['unique_string']
        db_ustring = EncryptionData.objects.filter(unique_string=unique_string)
        if db_ustring:
            return render(request, 'encrypt.html', {'participants': self.participants, "error": 'error'})
        else:
            participants = int(request.POST['participants'])
            threshold = int(request.POST['threshold'])

            for i in range(participants):
                emails.append(request.POST['email' + str(i)])

            image = request.FILES['image']
            share_list = imageEncryption(participants, threshold, image)
            en_str = ""
            for i in range(len(list(share_list))):
                for j in range(len(list(share_list[i]))):
                    for k in range(len(list(share_list[i][j]))):
                        for l in range(len(list(share_list[i][j][k]))):
                            en_str += str(share_list[i][j][k][l])
            for i in range(participants):
                im = Image.fromarray(share_list[i])
                im.save("image" + str(i) + ".png")
                subject = "secret image"
                text_content = 'your secret string is ' + unique_string
                message = EmailMultiAlternatives(subject, text_content, 'sachin.proshore@gmail.com', [emails[i]])
                message.attach_file('image' + str(i) + ".png")
                message.send()
                if os.path.exists("image" + str(i) + ".png"):
                    os.remove("image" + str(i) + ".png")
            print(type(share_list))
            print(type(share_list[0]))
            EncryptionData.objects.create(unique_string=unique_string,
                                          participants=participants,
                                          threshold=threshold,
                                          shares=en_str,
                                          orginal_image=image)
            messages.success(request, "Image is encrypted sucessfully!")
            return redirect(reverse('secretapp:home'))


class VerifyView(View):
    def get(self, request):
        return render(request, 'verify.html')

    def post(self, request):
        unique_string = request.POST['unique_string']
        udb_string = EncryptionData.objects.filter(unique_string=unique_string)
        if udb_string is None:
            messages.error(request, "Unique string you have inputed did'nt matched in database!")
            return redirect(reverse('secretapp:verify'))
        else:
            request.session['unique_string'] = unique_string
            return redirect(reverse('secretapp:decrypt'))


class DecryptView(View):

    def get(self, request):
        unique_string = request.session['unique_string']
        if unique_string:
            decryption_data = EncryptionData.objects.get(unique_string=unique_string)
            shares_num = range(decryption_data.threshold)
            return render(request, 'decrypt.html', {'shares_num': shares_num})
        else:
            messages.error(request, "verify the unique string first")
            return render(request, 'verify.html')

    def post(self, request):
        unique_string = request.session['unique_string']
        if unique_string:
            match = True
            decryption_data = EncryptionData.objects.get(unique_string=unique_string)
            threshold = decryption_data.threshold
            shares = decryption_data.shares
            duplicate_check = ""
            for i in range(threshold):
                img = changeImageToMatrix(request.FILES["image" + str(i)])
                img_str = ""
                for b in range(len(list(img))):
                    for j in range(len(list(img[b]))):
                        for k in range(len(list(img[b][j]))):
                            img_str += str(img[b][j][k])

                if img_str in duplicate_check:
                    match = False
                if img_str not in shares:
                    match = False
                if match == False:
                    messages.success(request, "You haven't meet minimum criteria to decryption!")
                    return redirect(reverse('secretapp:decrypt'))
                duplicate_check += img_str
            return redirect(reverse('secretapp:success'))
        else:
            messages.error(request, "Unique string did not matched!")
            return redirect(reverse('secretapp:verify'))


class SuccessView(View):
    def get(self, request):
        unique_string = request.session['unique_string']
        if unique_string:
            decryption_data = EncryptionData.objects.get(unique_string=unique_string)
            return render(request, 'success.html', {'image': decryption_data.orginal_image.url})
        else:
            messages.error(request, "Something went wrong")
            return redirect(reverse('secretapp:home'))
