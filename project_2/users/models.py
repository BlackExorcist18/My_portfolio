from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя"""
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', verbose_name="Аватар", blank=True, null=True)
    bio = models.TextField(verbose_name="О себе", blank=True, null=True)
    birth_date = models.DateField(verbose_name="Дата рождения", blank=True, null=True)
    
    # Для соцсети (друзья)
    friends = models.ManyToManyField('self', symmetrical=False, blank=True, verbose_name="Друзья")
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    
    def __str__(self):
        return self.username
    
    def add_friend(self, friend):
        """Добавить друга"""
        if friend != self and not self.friends.filter(id=friend.id).exists():
            self.friends.add(friend)
            return True
        return False
    
    def remove_friend(self, friend):
        """Удалить друга"""
        if self.friends.filter(id=friend.id).exists():
            self.friends.remove(friend)
            return True
        return False
    
    def is_friend(self, user):
        """Проверить, является ли пользователь другом"""
        return self.friends.filter(id=user.id).exists()