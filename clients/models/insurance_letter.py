from django.conf import settings
from django.core import urlresolvers
from django.db import models

from .claims import Claim, Invoice


class InsuranceLetter(models.Model):
    claim = models.OneToOneField(
        Claim, verbose_name="Claim")

    practitioner_name = models.CharField(
        "Practitioner Name", max_length=4, choices=settings.PRACTITIONERS,
        default=settings.DM,
        blank=True)
    biomedical_and_gait_analysis_date = models.DateField(
        "Biomedical and Gait Analysis Date",
        blank=True, null=True)
    examiner = models.CharField(
        "Examiner", max_length=4, choices=settings.PRACTITIONERS,
        default=settings.DM,
        blank=True)
    dispensing_practitioner = models.CharField(
        "Dispensing Practitioner", max_length=4,
        choices=settings.PRACTITIONERS, default=settings.DM,
        blank=True)

    orthopedic_shoes = models.BooleanField(
        "Orthopedic Shoes", default=False)
    foot_orthotics_orthosis = models.BooleanField(
        "Foot Orthotics Orthosis", default=False)
    internally_modified_footwear = models.BooleanField(
        "Internally Modified Orthosis", default=False)

    foam_plaster = models.BooleanField(
        "Foam / Plaster", default=False)

    plantar_fasciitis = models.BooleanField(
        "Plantar Fasciitis", default=False)
    hammer_toes = models.BooleanField(
        "Hammer Toes", default=False)
    ligament_tear = models.BooleanField(
        "Ligament Tear / Sprain", default=False)
    knee_arthritis = models.BooleanField(
        "Knee Arthritis", default=False)
    metatarsalgia = models.BooleanField(
        "Metatarsalgia", default=False)
    drop_foot = models.BooleanField(
        "Drop Foot", default=False)
    scoliosis_with_pelvic_tilt = models.BooleanField(
        "Scoliosis With Pelvic Tilt", default=False)
    hip_arthritis = models.BooleanField(
        "Hip Arthritis", default=False)
    pes_cavus = models.BooleanField(
        "Pes Cavus", default=False)
    heel_spur = models.BooleanField(
        "Heel Spur", default=False)
    lumbar_spine_dysfunction = models.BooleanField(
        "Lumbar Spine Dysfunction", default=False)
    lumbar_arthritis = models.BooleanField(
        "Lumbar Arthritis", default=False)
    pes_planus = models.BooleanField(
        "Pes Planus", default=False)
    ankle_abnormal_rom = models.BooleanField(
        "Ankle: Abnormal ROM", default=False)
    leg_length_discrepency = models.BooleanField(
        "Leg Length Discrepancy", default=False)
    si_arthritis = models.BooleanField(
        "SI Arthritis", default=False)
    diabetes = models.BooleanField(
        "Diabetes", default=False)
    foot_abnormal_ROM = models.BooleanField(
        "Foot: Abnormal ROM", default=False)
    si_joint_dysfunction = models.BooleanField(
        "SI Joint Dysfunction", default=False)
    ankle_arthritis = models.BooleanField(
        "Ankle Arthritis", default=False)
    neuropathy = models.BooleanField(
        "Neuropathy", default=False)
    peroneal_dysfunction = models.BooleanField(
        "Peroneal Dysfunction", default=False)
    genu_valgum = models.BooleanField(
        "Genu Valgum", default=False)
    foot_arthritis = models.BooleanField(
        "Foot Arthritis", default=False)
    mtp_drop = models.BooleanField(
        "MTP Drop", default=False)
    interdigital_neuroma = models.BooleanField(
        "Interdigital Neuroma", default=False)
    genu_varum = models.BooleanField(
        "Genu Varum", default=False)
    first_mtp_arthritis = models.BooleanField(
        "1st MTP Arthritis", default=False)
    forefoot_varus = models.BooleanField(
        "Forefoot Varus", default=False)
    bunions_hallux_valgus = models.BooleanField(
        "Bunions / Hallux Valgus", default=False)
    abnormal_patellar_tracking = models.BooleanField(
        "Abnormal Patellar Tracking", default=False)
    rheumatoid_arthritis = models.BooleanField(
        "Rheumatoid Arthritis", default=False)
    forefoot_valgus = models.BooleanField(
        "Forefoot Valgus", default=False)
    abnormal_gait_tracking = models.BooleanField(
        "Abnormal Gait Timing", default=False)
    abnormal_gait_pressures = models.BooleanField(
        "Abnormal Gait Pressures", default=False)
    gout = models.BooleanField(
        "Gout", default=False)
    shin_splints = models.BooleanField(
        "Shin Splints", default=False)
    over_supination = models.BooleanField(
        "Over Supination", default=False)
    achilles_tendinitis = models.BooleanField(
        "Achilles Tendinitis", default=False)
    ulcers = models.BooleanField(
        "Ulcers", default=False)
    over_pronation = models.BooleanField(
        "Over Pronation", default=False)

    other = models.CharField(
        "Other", max_length=64,
        blank=True)

    signature_date = models.DateField(blank=True, null=True)

    # ForeignKey
    # Laboratory

    def dispense_date(self):
        try:
            invoice = self.claim.invoice
            if invoice.invoice_date:
                return invoice.invoice_date
        except (Claim.DoesNotExist, Invoice.DoesNotExist):
            pass

    def _verbose_name(self, field):
        return InsuranceLetter._meta.get_field(field).verbose_name

    def diagnosis(self):
        diagnosis = []

        if self.plantar_fasciitis:
            diagnosis.append(self._verbose_name('plantar_fasciitis'))
        if self.hammer_toes:
            diagnosis.append(self._verbose_name('hammer_toes'))
        if self.ligament_tear:
            diagnosis.append(self._verbose_name('ligament_tear'))
        if self.knee_arthritis:
            diagnosis.append(self._verbose_name('knee_arthritis'))
        if self.metatarsalgia:
            diagnosis.append(self._verbose_name('metatarsalgia'))
        if self.drop_foot:
            diagnosis.append(self._verbose_name('drop_foot'))
        if self.scoliosis_with_pelvic_tilt:
            diagnosis.append(self._verbose_name('scoliosis_with_pelvic_tilt'))
        if self.hip_arthritis:
            diagnosis.append(self._verbose_name('hip_arthritis'))
        if self.pes_cavus:
            diagnosis.append(self._verbose_name('pes_cavus'))
        if self.heel_spur:
            diagnosis.append(self._verbose_name('heel_spur'))
        if self.lumbar_spine_dysfunction:
            diagnosis.append(self._verbose_name('lumbar_spine_dysfunction'))
        if self.lumbar_arthritis:
            diagnosis.append(self._verbose_name('lumbar_arthritis'))
        if self.pes_planus:
            diagnosis.append(self._verbose_name('pes_planus'))
        if self.ankle_abnormal_rom:
            diagnosis.append(self._verbose_name('ankle_abnormal_rom'))
        if self.leg_length_discrepency:
            diagnosis.append(self._verbose_name('leg_length_discrepency'))
        if self.si_arthritis:
            diagnosis.append(self._verbose_name('si_arthritis'))
        if self.diabetes:
            diagnosis.append(self._verbose_name('diabetes'))
        if self.foot_abnormal_ROM:
            diagnosis.append(self._verbose_name('foot_abnormal_ROM'))
        if self.si_joint_dysfunction:
            diagnosis.append(self._verbose_name('si_joint_dysfunction'))
        if self.ankle_arthritis:
            diagnosis.append(self._verbose_name('ankle_arthritis'))
        if self.neuropathy:
            diagnosis.append(self._verbose_name('neuropathy'))
        if self.peroneal_dysfunction:
            diagnosis.append(self._verbose_name('peroneal_dysfunction'))
        if self.genu_valgum:
            diagnosis.append(self._verbose_name('genu_valgum'))
        if self.foot_arthritis:
            diagnosis.append(self._verbose_name('foot_arthritis'))
        if self.mtp_drop:
            diagnosis.append(self._verbose_name('mtp_drop'))
        if self.interdigital_neuroma:
            diagnosis.append(self._verbose_name('interdigital_neuroma'))
        if self.genu_varum:
            diagnosis.append(self._verbose_name('genu_varum'))
        if self.first_mtp_arthritis:
            diagnosis.append(self._verbose_name('first_mtp_arthritis'))
        if self.forefoot_varus:
            diagnosis.append(self._verbose_name('forefoot_varus'))
        if self.bunions_hallux_valgus:
            diagnosis.append(self._verbose_name('bunions_hallux_valgus'))
        if self.abnormal_patellar_tracking:
            diagnosis.append(self._verbose_name('abnormal_patellar_tracking'))
        if self.rheumatoid_arthritis:
            diagnosis.append(self._verbose_name('rheumatoid_arthritis'))
        if self.forefoot_valgus:
            diagnosis.append(self._verbose_name('forefoot_valgus'))
        if self.abnormal_gait_tracking:
            diagnosis.append(self._verbose_name('abnormal_gait_tracking'))
        if self.abnormal_gait_pressures:
            diagnosis.append(self._verbose_name('abnormal_gait_pressures'))
        if self.gout:
            diagnosis.append(self._verbose_name('gout'))
        if self.shin_splints:
            diagnosis.append(self._verbose_name('shin_splints'))
        if self.over_supination:
            diagnosis.append(self._verbose_name('over_supination'))
        if self.achilles_tendinitis:
            diagnosis.append(self._verbose_name('achilles_tendinitis'))
        if self.ulcers:
            diagnosis.append(self._verbose_name('ulcers'))
        if self.over_pronation:
            diagnosis.append(self._verbose_name('over_pronation'))
        if self.other:
            diagnosis.append(self.other)

        if diagnosis:
            diagnosis.append("as per prescription.")

        # Remove list characters
        return str(diagnosis).strip("[]").replace("'", "")

    def get_absolute_url(self):
        return urlresolvers.reverse_lazy(
            'fillOutInsurance', kwargs={'claim_id': self.claim.id}
        )

    def __str__(self):
        return "{} - Claim ID: {}".format(self.dispense_date(), self.claim_id)


class Laboratory(models.Model):
    # Dont set default on information, or itll mess up FormSets
    information = models.CharField(
        "Information", max_length=8, choices=settings.LABORATORIES)
    insurance_letter = models.ForeignKey(
        InsuranceLetter, verbose_name="Insurance Letter",
        null=True, blank=True)

    class Meta:
        verbose_name_plural = "Laboratories"

    def __str__(self):
        return self.get_information_display().split('\n')[0]
