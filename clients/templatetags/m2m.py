from django import template
register = template.Library()


@register.assignment_tag
def claim_coverage_type_actual_amount_claimed(claim, coverage_type):
    try:
        return claim.claimcoveragetype_set.get(
            claim=claim, coverage_type=coverage_type).actual_amount_claimed
    except:
        return 0


@register.assignment_tag
def claim_coverage_type_actual_expected_back(claim, coverage_type):
    try:
        return claim.claimcoveragetype_set.get(
            claim=claim, coverage_type=coverage_type).actual_expected_back
    except:
        return 0


@register.assignment_tag
def claim_item_quantity(claim, item):
    try:
        return claim.claimitem_set.get(
            claim=claim, item=item).quantity
    except:
        return 1
