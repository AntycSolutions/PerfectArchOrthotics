from django import apps
from django.db.models import signals


class ClientsAppConfig(apps.AppConfig):
    name = 'clients'

    def ready(self):
        # import here to avoid circular import
        from clients import signals as clients_signals
        signals.pre_save.connect(
            clients_signals.claimcoverage_pre_save,
            sender=self.get_model('ClaimCoverage')
        )
        signals.post_delete.connect(
            clients_signals.claimcoverage_post_delete,
            sender=self.get_model('ClaimCoverage')
        )

        signals.pre_save.connect(
            clients_signals.referral_pre_save,
            sender=self.get_model('Referral')
        )
        signals.post_delete.connect(
            clients_signals.referral_post_delete,
            sender=self.get_model('Referral')
        )
