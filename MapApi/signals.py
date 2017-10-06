from django.dispatch import Signal
user_login = Signal(providing_args=["request", "user"])