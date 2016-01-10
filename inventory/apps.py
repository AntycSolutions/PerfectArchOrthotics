from django import apps
from django.db.models import signals


class InventoryAppConfig(apps.AppConfig):
    name = 'inventory'

    def ready(self):
        # import here to avoid circular import
        from clients import signals as clients_signals
        signals.pre_save.connect(
            clients_signals.shoeorder_pre_save,
            sender=self.get_model('ShoeOrder')
        )
        signals.post_delete.connect(
            clients_signals.shoeorder_post_delete,
            sender=self.get_model('ShoeOrder')
        )

        signals.pre_save.connect(
            clients_signals.coverageorder_and_adjustmentorder_pre_save,
            sender=self.get_model('CoverageOrder')
        )
        signals.post_delete.connect(
            clients_signals.coverageorder_and_adjustmentorder_post_delete,
            sender=self.get_model('CoverageOrder')
        )

        signals.pre_save.connect(
            clients_signals.coverageorder_and_adjustmentorder_pre_save,
            sender=self.get_model('AdjustmentOrder')
        )
        signals.post_delete.connect(
            clients_signals.coverageorder_and_adjustmentorder_post_delete,
            sender=self.get_model('AdjustmentOrder')
        )

        signals.pre_save.connect(
            clients_signals.shoe_pre_save,
            sender=self.get_model('Shoe')
        )
