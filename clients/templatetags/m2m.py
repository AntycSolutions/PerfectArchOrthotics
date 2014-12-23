from django import template
register = template.Library()


@register.assignment_tag
def claim_coverage_amount_claimed(claim, coverage):
    try:
        return claim.claimcoverage_set.get(
            claim=claim, coverage=coverage).amount_quantity_claimed[0]
    except:
        return 0


@register.assignment_tag
def claim_coverage_quantity_claimed(claim, coverage):
    try:
        return claim.claimcoverage_set.get(
            claim=claim, coverage=coverage).amount_quantity_claimed[1]
    except:
        return 0


@register.assignment_tag
def claim_coverage_expected_back(claim, coverage):
    try:
        return claim.claimcoverage_set.get(
            claim=claim, coverage=coverage).expected_back
    except:
        return 0


@register.assignment_tag
def claim_item_quantity(claim, item):
    try:
        return claim.claimitem_set.get(
            claim=claim, item=item).quantity
    except:
        return 1
