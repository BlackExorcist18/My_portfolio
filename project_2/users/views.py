import logging
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()

# Создаём логгер для модуля users (ЛР6)
logger = logging.getLogger(__name__)


def register(request):
    """Регистрация пользователя с логированием (ЛР6)"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Успешная регистрация → INFO
            logger.info(f"Successful registration: User '{user.username}' registered")
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('users:profile')
        else:
            # Ошибки валидации → WARNING
            logger.warning(f"Registration failed for {request.POST.get('username', 'unknown')}: {form.errors}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    """Логирование входа (используется стандартный LoginView, но можно добавить через сигнал)"""
    # Логирование будет через сигнал (см. ниже)
    pass


@login_required
def profile_edit(request):
    """Редактирование профиля с обработкой ошибок изображения (ЛР6)"""
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        try:
            if form.is_valid():
                form.save()
                logger.info(f"Profile updated successfully for user '{request.user.username}'")
                messages.success(request, 'Профиль успешно обновлен!')
                return redirect('users:profile')
            else:
                logger.warning(f"Profile update validation failed for {request.user.username}: {form.errors}")
        except Exception as e:
            # Логирование ошибки с exc_info=True (ЛР6)
            logger.error(f"Error updating profile for {request.user.username}: {str(e)}", exc_info=True)
            messages.error(request, f'Ошибка при обновлении профиля: {str(e)}')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'users/profile_edit.html', {'form': form})


@login_required
def add_friend(request, pk):
    """Добавление друга с логированием (ЛР6)"""
    friend = get_object_or_404(User, pk=pk)
    if request.user.add_friend(friend):
        logger.info(f"User '{request.user.username}' added friend '{friend.username}'")
        messages.success(request, f'{friend.username} добавлен в друзья!')
    else:
        logger.warning(f"User '{request.user.username}' failed to add friend '{friend.username}'")
        messages.warning(request, 'Не удалось добавить в друзья')
    return redirect('users:user_detail', pk=pk)


@login_required
def remove_friend(request, pk):
    """Удаление друга с логированием (ЛР6)"""
    friend = get_object_or_404(User, pk=pk)
    if request.user.remove_friend(friend):
        logger.info(f"User '{request.user.username}' removed friend '{friend.username}'")
        messages.success(request, f'{friend.username} удален из друзей!')
    else:
        logger.warning(f"User '{request.user.username}' failed to remove friend '{friend.username}'")
        messages.warning(request, 'Не удалось удалить из друзей')
    return redirect('users:user_detail', pk=pk)
@login_required
def profile(request):
    """Страница профиля пользователя"""
    return render(request, 'users/profile.html', {'user': request.user})


@login_required
def user_list(request):
    """Список всех пользователей (для добавления в друзья)"""
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'users/user_list.html', {'users': users})


@login_required
def user_detail(request, pk):
    """Страница другого пользователя"""
    viewed_user = get_object_or_404(User, pk=pk)
    
    # Проверка: можно ли смотреть страницу незнакомца
    if not request.user.is_friend(viewed_user) and request.user != viewed_user:
        messages.error(request, 'Вы можете просматривать только страницы своих друзей!')
        return redirect('users:user_list')
    
    return render(request, 'users/user_detail.html', {'viewed_user': viewed_user})