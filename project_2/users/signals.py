import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Логирование успешного входа (ЛР6)"""
    logger.info(f"User '{user.username}' logged in successfully")


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """Логирование выхода (ЛР6)"""
    if user:
        logger.info(f"User '{user.username}' logged out")
    else:
        logger.info("User logged out (anonymous)")


@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    """Логирование неудачной попытки входа (ЛР6)"""
    username = credentials.get('username', 'unknown')
    logger.warning(f"Failed login attempt for username: '{username}'")