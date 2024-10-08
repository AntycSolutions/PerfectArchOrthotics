from auditlog.registry import auditlog

from .biomechanics import (
    BiomechanicalFoot, BiomechanicalGait, BiomechanicalGait2
)
from .claims import Claim, ClaimAttachment, ClaimCoverage, ClaimItem, \
    ProofOfManufacturing, Receipt, Invoice
from .clients import Person, Client, Dependent, Note
from .credit_devisor import CreditDivisor
from .insurance_info import Insurance, Coverage
from .insurance_letter import InsuranceLetter, Laboratory
from .items import Item, ItemHistory
from .referrals import Referral
from .blue_cross import BlueCross


auditlog.register(Person)
auditlog.register(Client)
auditlog.register(Note)
auditlog.register(Dependent)
auditlog.register(Insurance)
auditlog.register(Coverage)
auditlog.register(Item)
auditlog.register(ItemHistory)
auditlog.register(Invoice)
auditlog.register(Claim)
auditlog.register(ClaimAttachment)
auditlog.register(ClaimCoverage)
auditlog.register(ClaimItem)
auditlog.register(InsuranceLetter)
auditlog.register(ProofOfManufacturing)
auditlog.register(BiomechanicalGait)
auditlog.register(BiomechanicalGait2)
auditlog.register(BiomechanicalFoot)
auditlog.register(Laboratory)
auditlog.register(BlueCross)
auditlog.register(Referral)
auditlog.register(Receipt)
auditlog.register(CreditDivisor)
