from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Memory, Files
from .forms import MemoryAddForm, FileForm
from authentication.models import Profile
from django.http import JsonResponse,HttpResponse
import json
from authentication.utils import validateSize, validate_file_type
# Create your views here.


def dashboardView(request):
    user = request.user
    if user.is_authenticated:
        profile = Profile.objects.get(user=user)
        memories = Memory.objects.filter(owner=profile)
        context = {
            'message': 'Success',
            'user': user,
            'profile': profile,
            'momories': memories,
        }
        return render(request, 'dashboard.html', context=context)
    else:
        context = {
            'message': 'Error',
            'error_id': 1,
            'reason': 'User authentication failed',
        }
        return render(request, 'error_page.html', context=context)


@login_required
def memoryDetailView(request, pk):
    user = request.user
    if user.is_authenticated:
        memory = Memory.objects.get(pk=pk)
        context = {
            'message': 'Success',
            'user': user,
            'memory': memory,
        }
        return render(request, 'memory_detail.html', context=context)
    else:
        context = {
            'message': 'Error',
            'error_id': 1,
            'reason': 'User authentication failed.',
        }
        return render(request, 'error_page.html', context=context)


def addMemoryView(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            print('request.POST = ',request.POST)
            print('request.FILE = ',request.FILES)
            form = MemoryAddForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.owner = request.user.profile
                #print("instance = ", instance.title)
                instance.save()
                files = request.FILES.getlist('files')
                print("from add memory view = ", files)
                if len(files) > 0:
                    print("hello")
                    for f in files:
                        #print("hi= ",f)
                        Files.objects.create(
                            file=f,
                            owner=request.user.profile,
                            memory=instance,
                            name=f.name,
                        )
                response = HttpResponse(json.dumps({'success': True, 'message': 'Congrats you have created your new memory.'}), content_type="application/json")
                #response.status_code = 200
                print('True')
                return response
            else:
                print("False")
                response = HttpResponse(json.dumps({'success': False, 'message':"Something not right with your form"}), content_type="application/json")
                #response.status_code = 200
                return response
        else:
            form = MemoryAddForm()
            return render(request, 'memory_add.html', {'form': form})
    else:
        context = {
            'message': 'Error',
            'error_id': 2,
            'reason': "User authentication failed in add Memory."
        }
        return render(request, 'error_page.html', context)


def validateFiles(request):
    if request.method == 'POST':
        try:
            files = request.FILES.getlist('files')
            data = request.POST
            print("data= ", data)
            print("files= ", files)
        except:
            response = JsonResponse(
                {'success': False, 'message': 'No files uploaded'})
            response.status_code = 200
        invalid_files = []
        valid_files = []
        for f in files:
            if validateSize(f):
                if(validate_file_type(f)):
                    valid_files.append(f.name)
                else:
                    invalid_files.append(f.name)
            else:
                invalid_files.append(f.name)
        if len(invalid_files) > 0:
            response = JsonResponse({'success': True, 'message': 'Some files are spoofed or exceed size limit',
                                     'invalid_files': invalid_files, 'valid_files': valid_files})
            response.status_code = 200
        else:
            response = JsonResponse({'success': True, 'message': 'All selected files are safe to be added in memory.',
                                     'invalid_files': invalid_files, 'valid_files': valid_files})
            response.status_code = 200
    else:
        response = JsonResponse(
            {'success': False, 'message': 'Bad Request', 'invalid_files': invalid_files})
        response.status_code = 200
    return response
