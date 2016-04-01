import os

from django.utils import timezone


def check_period_date():
    now = timezone.now()
    for insurance in models.Insurance.objects.all():
        for coverage in insurance.coverage_set.filter(period__isnull=False):
            if coverage.period == models.Coverage.TWELVE_ROLLING_MONTHS:
                pass
            elif coverage.period == models.Coverage.TWENTY_FOUR_ROLLING_MONTHS:
                pass
            elif coverage.period == models.Coverage.THIRTY_SIX_ROLLING_MONTHS:
                pass
            elif coverage.period == models.Coverage.BENEFIT_YEAR:
                pass
            elif coverage.period == models.Coverage.CALENDAR_YEAR:
                if coverage.period_date and coverage.period_date >= now:
                    # reset coverage amount
                    pass
            else:
                raise Exception('Unknown Coverage period')


if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'perfect_arch_orthotics.settings'
    import django
    django.setup()

    from clients import models

    check_period_date()
