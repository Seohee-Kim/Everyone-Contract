from django.apps import AppConfig
from pages.KobertModule.classifier import ClassifierModule


class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'
    classifiermodule = ClassifierModule()
