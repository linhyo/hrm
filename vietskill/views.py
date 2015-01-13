from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from vietskill.models import StaffProfile
from vietskill.forms import ProfileForm


def index(request):
    return render(request, 'vietskill/index.html', {})


def about(request):
    return render(request, 'vietskill/about.html', {})


def profile_all(request):
    profile_list = StaffProfile.objects.all().order_by("name")
    context_dict = {'profiles': profile_list}
    return render(request, 'vietskill/profile_all.html', context_dict)


def profile_detail(request, pk):
    profile = get_object_or_404(StaffProfile, pk=pk)
    context_dict = {'profile': profile}
    return render(request, 'vietskill/profile_detail.html', context_dict)


def profile_add(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=True)
            return redirect('vietskill.views.profile_detail', pk=profile.pk)
        else:
            print form.errors
    else:
        form = ProfileForm()
    # form = ProfileForm()
    context_dict = {'form': form}
    return render(request, 'vietskill/profile_edit.html', context_dict)


def profile_edit(request, pk):
    profile = get_object_or_404(StaffProfile, pk=pk)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=True)
            return redirect('vietskill.views.profile_detail', pk=profile.pk)
        else:
            print form.errors
    else:
        form = ProfileForm(instance=profile)
    context_dict = {'form': form}
    return render(request, 'vietskill/profile_edit.html', context_dict)
    
    
def profile_delete(request, pk):
    profile = get_object_or_404(StaffProfile, pk=pk)
    profile.delete()
    return redirect('vietskill.views.profile_all')


#Statistics
def teaching_day(request):
    return render(request, 'statistics/teaching_day.html', {})


def online_day(request):
    return render(request, 'statistics/online_day.html', {})


def absent_day(request):
    return render(request, 'statistics/absent_day.html', {})


def mistake(request):
    return render(request, 'statistics/mistake.html', {})
