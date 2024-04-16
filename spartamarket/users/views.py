from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model

# Create your views here.
def profile(request, user_id):
	user = get_object_or_404(get_user_model(), pk=user_id)
	context = {'user':user}
	return render(request, 'users/profile.html', context)

@require_POST
def follow(request, user_id):
	if request.user.is_authenticated:
		user = get_object_or_404(get_user_model(), pk=user_id)
		if user != request.user:
			if user.followers.filter(pk=request.user.pk).exists():
				user.followers.remove(request.user)
			else:
				user.followers.add(request.user)
			return redirect('users:profile', user_id=user_id)
	return redirect('accounts:login')