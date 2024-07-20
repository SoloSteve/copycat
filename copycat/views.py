from django.shortcuts import render
import subprocess
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from .forms import Mp4form
from .models import Uploadmp4
from django.shortcuts import redirect
from django.contrib import messages
import os



def index_view(request):
    if request.method == 'POST':
        form = Mp4form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Video upload completed')
            return redirect('index')
    else:
         form = Mp4form()
         return render(request, 'index.html', {'form':form})

    if request.method == 'POST':
        input_num1 = request.POST.get('input_num1','')
        input_num2 = request.POST.get('input_num2','')
        input_num3 = request.POST.get('input_num3','')
        input_num4 = request.POST.get('input_num4','')
        input_num5 = request.POST.get('input_num5','')
        file_path = os.path.join('media', 'files', input_num1)
        result_baby = subprocess.run(['python3', 'copycat/main.py', '-f', file_path, '-k', input_num2, '-t', input_num3, '-s', input_num4, '-tc', input_num5], capture_output=True, text=True)
        result = result_baby.stdout
        return render(request, 'index.html', {'result': result})
    else:
        return render(request, 'index.html')

    