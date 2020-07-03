from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Memory
from authentication.models import Profile
# Create your views here.


@login_required
def dashboardView(request):
    user = request.user
    if user.is_authenticated:
        profile = Profile.objects.get(user=user)
        memories = Memory.objects.filter(owner=Profile)
        context = {
            'message': 'Success',
            'user': user,
            'profile': profile,
            'momories': memories,
        }
        return render(request, 'memories.html', context=context)
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
            'message':'Success',
            'user':user,
            'memory':memory,
        }
        return render(request, 'memory_detail.html',context=context)
    else:
        context = {
            'message':'Error',
            'error_id':1,
            'reason':'User authentication failed',
        }
        return render(request,'error_page.html',context=context)
