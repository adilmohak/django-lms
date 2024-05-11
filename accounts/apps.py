from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "accounts"

    def ready(self) -> None:
        from django.db.models.signals import post_save
        from .models import User
        from .signals import post_save_account_receiver

        post_save.connect(post_save_account_receiver, sender=User)

        return super().ready()
