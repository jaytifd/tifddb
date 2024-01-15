from django.apps import AppConfig


class CampConfig(AppConfig):
    name = 'camp'
    def ready(self):
        # import the paypal signal handler
        import camp.signals
