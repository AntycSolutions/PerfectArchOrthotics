from django.db import models
from django.core import urlresolvers

from .clients import Person
from .claims import Claim

from utils import model_utils


class BiomechanicalGait(models.Model, model_utils.FieldList):
    patient = models.ForeignKey(Person)

    provider = models.CharField(max_length=128)

    # Examination Findings
    arch_height_non_weight_high_left = models.BooleanField(default=False)
    arch_height_non_weight_high_right = models.BooleanField(default=False)
    arch_height_non_weight_medium_left = models.BooleanField(default=False)
    arch_height_non_weight_medium_right = models.BooleanField(default=False)
    arch_height_non_weight_low_left = models.BooleanField(default=False)
    arch_height_non_weight_low_right = models.BooleanField(default=False)

    arch_height_weight_high_left = models.BooleanField(default=False)
    arch_height_weight_high_right = models.BooleanField(default=False)
    arch_height_weight_medium_left = models.BooleanField(default=False)
    arch_height_weight_medium_right = models.BooleanField(default=False)
    arch_height_weight_low_left = models.BooleanField(default=False)
    arch_height_weight_low_right = models.BooleanField(default=False)

    gait_toe_in = models.BooleanField(default=False)
    gait_straight = models.BooleanField(default=False)
    gait_toe_out = models.BooleanField(default=False)

    supination = models.BooleanField(default=False)
    supination_mild_left = models.BooleanField(default=False)
    supination_mild_right = models.BooleanField(default=False)
    supination_moderate_left = models.BooleanField(default=False)
    supination_moderate_right = models.BooleanField(default=False)
    supination_severe_left = models.BooleanField(default=False)
    supination_severe_right = models.BooleanField(default=False)

    pronation = models.BooleanField(default=False)
    pronation_mild_left = models.BooleanField(default=False)
    pronation_mild_right = models.BooleanField(default=False)
    pronation_moderate_left = models.BooleanField(default=False)
    pronation_moderate_right = models.BooleanField(default=False)
    pronation_severe_left = models.BooleanField(default=False)
    pronation_severe_right = models.BooleanField(default=False)

    # Optional Findings
    ankle_dorsi_flexion_adequate_left = models.BooleanField(default=False)
    ankle_dorsi_flexion_adequate_right = models.BooleanField(default=False)
    ankle_dorsi_flexion_limited_left = models.BooleanField(default=False)
    ankle_dorsi_flexion_limited_right = models.BooleanField(default=False)

    general_foot_motion_restricted_left = models.BooleanField(default=False)
    general_foot_motion_restricted_right = models.BooleanField(default=False)
    general_foot_motion_normal_left = models.BooleanField(default=False)
    general_foot_motion_normal_right = models.BooleanField(default=False)
    general_foot_motion_hyper_mobile_left = models.BooleanField(default=False)
    general_foot_motion_hyper_mobile_right = models.BooleanField(default=False)

    forefoot_varus = models.BooleanField(default=False)
    forefoot_varus_mild_left = models.BooleanField(default=False)
    forefoot_varus_mild_right = models.BooleanField(default=False)
    forefoot_varus_moderate_left = models.BooleanField(default=False)
    forefoot_varus_moderate_right = models.BooleanField(default=False)
    forefoot_varus_severe_left = models.BooleanField(default=False)
    forefoot_varus_severe_right = models.BooleanField(default=False)

    forefoot_valgus = models.BooleanField(default=False)
    forefoot_valgus_mild_left = models.BooleanField(default=False)
    forefoot_valgus_mild_right = models.BooleanField(default=False)
    forefoot_valgus_moderate_left = models.BooleanField(default=False)
    forefoot_valgus_moderate_right = models.BooleanField(default=False)
    forefoot_valgus_severe_left = models.BooleanField(default=False)
    forefoot_valgus_severe_right = models.BooleanField(default=False)

    subtalar_joint_hyper_mobile = models.BooleanField(default=False)
    subtalar_joint_limited_rom = models.BooleanField(default=False)

    ankle_joint_hyper_mobile = models.BooleanField(default=False)
    ankle_joint_limited_rom = models.BooleanField(default=False)

    first_mpj_hyper_mobile = models.BooleanField(default=False)
    first_mpj_limited_rom = models.BooleanField(default=False)

    # Orthotics
    casual_functional_2mm = models.BooleanField(default=False)
    casual_functional_3mm = models.BooleanField(default=False)
    casual_functional_35mm = models.BooleanField(
        "Casual functional 3.5mm", default=False
    )
    casual_functional_34 = models.BooleanField(
        "Casual functional 3/4", default=False
    )
    casual_functional_sulcus = models.BooleanField(default=False)
    casual_functional_full_length = models.BooleanField(default=False)

    casual_kids_2mm = models.BooleanField(default=False)
    casual_kids_3mm = models.BooleanField(default=False)
    casual_kids_35mm = models.BooleanField("Casual kids 3.5mm", default=False)
    casual_kids_34 = models.BooleanField("Casual kids 3/4", default=False)
    casual_kids_full_length = models.BooleanField(default=False)

    casual_accommodative_2mm = models.BooleanField(default=False)
    casual_accommodative_sulcus = models.BooleanField(default=False)
    casual_accommodative_full_length = models.BooleanField(default=False)

    dress_dress_2mm = models.BooleanField(default=False)
    dress_dress_3mm = models.BooleanField(default=False)
    dress_dress_35mm = models.BooleanField("Dress dress 3.5mm", default=False)
    dress_dress_34 = models.BooleanField("Dress dress 3/4", default=False)
    dress_dress_sulcus = models.BooleanField(default=False)
    dress_dress_full_length = models.BooleanField(default=False)

    dress_fashion_2mm = models.BooleanField(default=False)
    dress_fashion_3mm = models.BooleanField(default=False)
    dress_fashion_35mm = models.BooleanField(
        "Dress fashion 3.5mm", default=False
    )
    dress_fashion_full_length = models.BooleanField(default=False)

    sport_sport_2mm = models.BooleanField(default=False)
    sport_sport_3mm = models.BooleanField(default=False)
    sport_sport_35mm = models.BooleanField("Sport sport 3.5mm", default=False)
    sport_sport_34 = models.BooleanField("Sport sport 3/4", default=False)
    sport_sport_sulcus = models.BooleanField(default=False)
    sport_sport_full_length = models.BooleanField(default=False)

    sport_run_2mm = models.BooleanField(default=False)
    sport_run_3mm = models.BooleanField(default=False)
    sport_run_35mm = models.BooleanField("Sport run 3.5mm", default=False)
    sport_run_sulcus = models.BooleanField(default=False)
    sport_run_full_length = models.BooleanField(default=False)

    sport_eagle_2mm = models.BooleanField(default=False)
    sport_eagle_3mm = models.BooleanField(default=False)
    sport_eagle_35mm = models.BooleanField("Sport eagle 3.5mm", default=False)
    sport_eagle_34 = models.BooleanField("Sport eagle 3/4", default=False)
    sport_eagle_sulcus = models.BooleanField(default=False)
    sport_eagle_full_length = models.BooleanField(default=False)

    sport_ski_2mm = models.BooleanField(default=False)
    sport_ski_3mm = models.BooleanField(default=False)
    sport_ski_35mm = models.BooleanField("Sport ski 3.5mm", default=False)
    sport_ski_sulcus = models.BooleanField(default=False)
    sport_ski_full_length = models.BooleanField(default=False)

    sport_skate_2mm = models.BooleanField(default=False)
    sport_skate_3mm = models.BooleanField(default=False)
    sport_skate_35mm = models.BooleanField("Sport skate 3.5mm", default=False)
    sport_skate_sulcus = models.BooleanField(default=False)
    sport_skate_full_length = models.BooleanField(default=False)

    sport_court_2mm = models.BooleanField(default=False)
    sport_court_3mm = models.BooleanField(default=False)
    sport_court_35mm = models.BooleanField("Sport court 3.5mm", default=False)
    sport_court_sulcus = models.BooleanField(default=False)
    sport_court_full_length = models.BooleanField(default=False)

    sport_soccer_2mm = models.BooleanField(default=False)
    sport_soccer_3mm = models.BooleanField(default=False)
    sport_soccer_35mm = models.BooleanField(
        "Sport soccer 3.5mm", default=False
    )
    sport_soccer_sulcus = models.BooleanField(default=False)
    sport_soccer_full_length = models.BooleanField(default=False)

    sport_safety_2mm = models.BooleanField(default=False)
    sport_safety_3mm = models.BooleanField(default=False)
    sport_safety_35mm = models.BooleanField(
        "Sport safety 3.5mm", default=False
    )
    sport_safety_sulcus = models.BooleanField(default=False)
    sport_safety_full_length = models.BooleanField(default=False)

    # Specialty Orthotics
    leather_sulcus = models.BooleanField(default=False)
    leather_full = models.BooleanField(default=False)
    leather_heel_spur_pad = models.BooleanField(default=False)
    leather_heel_lift = models.BooleanField(default=False)
    leather_heel_lift_l = models.CharField(max_length=5, blank=True)
    leather_heel_lift_r = models.CharField(max_length=5, blank=True)

    ucbl_1mm = models.BooleanField(default=False)
    ucbl_2mm = models.BooleanField(default=False)

    gait_plate_2mm = models.BooleanField(default=False)
    gait_plate_3mm = models.BooleanField(default=False)
    gait_plate_35mm = models.BooleanField("Gait plate 3.5mm", default=False)
    gait_plate_induce_toe_in = models.BooleanField(default=False)
    gait_plate_induce_toe_out = models.BooleanField(default=False)

    diabetic_34 = models.BooleanField("Diabetic 3/4", default=False)
    diabetic_sulcus = models.BooleanField(default=False)
    diabetic_full_length = models.BooleanField(default=False)

    # Patient Information
    weight = models.CharField(max_length=10, blank=True)
    height = models.CharField(max_length=10, blank=True)
    shoe_size = models.CharField(max_length=5, blank=True)
    shoe_type = models.CharField(max_length=16, blank=True)
    main_activities = models.CharField(max_length=32, blank=True)
    fabricate = models.BooleanField(default=False)

    # Chief Complaints / Special Instructions
    chief_complaints_special_instructions = models.TextField(blank=True)
    # TODO: circlable feet

    # Additions / Modifications
    full_heel_cushion = models.BooleanField(default=False)

    neuroma_pad = models.BooleanField(default=False)
    neuroma_pad_l_1 = models.CharField(max_length=5, blank=True)
    neuroma_pad_l_2 = models.CharField(max_length=5, blank=True)
    neuroma_pad_r_1 = models.CharField(max_length=5, blank=True)
    neuroma_pad_r_2 = models.CharField(max_length=5, blank=True)

    metatarsal_pad = models.BooleanField(default=False)
    metatarsal_pad_low_profile = models.BooleanField(default=False)
    metatarsal_pad_distal_placement = models.BooleanField(default=False)

    forefoot_pad_to_sulcus = models.BooleanField(default=False)
    forefoot_pad_to_sulcus_l = models.CharField(max_length=5, blank=True)
    forefoot_pad_to_sulcus_r = models.CharField(max_length=5, blank=True)

    sub_metatarsal_accommodation = models.BooleanField(default=False)
    sub_metatarsal_accommodation_l = models.CharField(max_length=5, blank=True)
    sub_metatarsal_accommodation_r = models.CharField(max_length=5, blank=True)

    heel_spur_pad = models.BooleanField(default=False)
    heel_spur_pad_l = models.CharField(max_length=5, blank=True)
    heel_spur_pad_r = models.CharField(max_length=5, blank=True)

    mortons_extension = models.BooleanField(default=False)
    mortons_extension_l = models.CharField(max_length=5, blank=True)
    mortons_extension_r = models.CharField(max_length=5, blank=True)

    reinforced_arch = models.BooleanField(
        "Reinforced arch (greater than 280lbs)", default=False
    )

    rearfoot_extrinsic_post = models.BooleanField(default=False)
    rearfoot_extrinsic_post_l = models.CharField(max_length=5, blank=True)
    rearfoot_extrinsic_post_r = models.CharField(max_length=5, blank=True)

    medial_skive = models.BooleanField(default=False)
    medial_skive_l = models.CharField(max_length=5, blank=True)
    medial_skive_r = models.CharField(max_length=5, blank=True)

    lateral_skive = models.BooleanField(default=False)
    lateral_skive_l = models.CharField(max_length=5, blank=True)
    lateral_skive_r = models.CharField(max_length=5, blank=True)

    hole_in_heel = models.BooleanField(default=False)
    hole_in_heel_l = models.CharField(max_length=5, blank=True)
    hole_in_heel_r = models.CharField(max_length=5, blank=True)
    hole_in_heel_with_foam_disk = models.BooleanField(default=False)

    reverse_mortons_extension = models.BooleanField(default=False)
    reverse_mortons_extension_l = models.CharField(max_length=5, blank=True)
    reverse_mortons_extension_r = models.CharField(max_length=5, blank=True)

    extrinsic_forefoot_post_34_length = models.BooleanField(
        "Extrinsic forefoot post (3/4 length)", default=False
    )
    extrinsic_forefoot_post_34_length_l = models.CharField(
        "Extrinsic forefoot post (3/4 length) L", max_length=5,
        blank=True
    )
    extrinsic_forefoot_post_34_length_r = models.CharField(
        "Extrinsic forefoot post (3/4 length) R", max_length=5,
        blank=True
    )

    heel_lift = models.BooleanField(default=False)
    heel_lift_l = models.CharField(max_length=5, blank=True)
    heel_lift_r = models.CharField(max_length=5, blank=True)

    deep_heel_cups = models.BooleanField(default=False)
    deep_heel_cups_l = models.CharField(max_length=5, blank=True)
    deep_heel_cups_r = models.CharField(max_length=5, blank=True)

    first_metatarsal_cut_out = models.BooleanField(default=False)
    first_metatarsal_cut_out_l = models.CharField(max_length=5, blank=True)
    first_metatarsal_cut_out_r = models.CharField(max_length=5, blank=True)

    extrinsic_forefoot_post_sulcus_length = models.BooleanField(
        "Extrinsic forefoot post (sulcus length)", default=False
    )
    extrinsic_forefoot_post_sulcus_length_l = models.CharField(
        "Extrinsic forefoot post (sulcus length) L", max_length=5,
        blank=True
    )
    extrinsic_forefoot_post_sulcus_length_r = models.CharField(
        "Extrinsic forefoot post (sulcus length) R", max_length=5,
        blank=True
    )

    vinyl_sandwich_bilateral = models.BooleanField(
        "Vinyl sandwich (bilateral)", default=False)

    medial_flange = models.BooleanField(default=False)
    medial_flange_l = models.CharField(max_length=5, blank=True)
    medial_flange_r = models.CharField(max_length=5, blank=True)

    lateral_flange = models.BooleanField(default=False)
    lateral_flange_l = models.CharField(max_length=5, blank=True)
    lateral_flange_r = models.CharField(max_length=5, blank=True)

    # Special Topcover Requests
    extra_foam_padding_topcover_18 = models.BooleanField(
        "Extra foam padding under topcover 1/8\"", default=False
    )
    extra_foam_padding_topcover_116 = models.BooleanField(
        "Extra foam padding under topcover 1/16\"", default=False
    )
    suede_leather_topcover = models.BooleanField(
        "Suede leather topcover on orthotic ($10 additional charge)",
        default=False
    )
    other_topcover = models.CharField(
        "Other topcover (please specify)", max_length=16,
        blank=True
    )

    signature_date = models.DateField(blank=True, null=True)

    def get_additional_data(self):
        # track client_id so we can look it up via auditlog
        # update api_helpers.HistoryMixin if this changes
        return {
            'client_id': self.patient_id,
        }

    def get_absolute_url(self):
        url = '{}?toggle=biomechanical_gaits#biomechanical_gait_{}'.format(
            urlresolvers.reverse(
                'client', kwargs={'client_id': self.patient.get_client().pk}
            ),
            self.pk
        )

        return url

    def __str__(self):
        return "{} - Patient ID: {}".format(self.provider, self.patient_id)


class BiomechanicalFoot(models.Model, model_utils.FieldList):
    claim = models.OneToOneField(Claim)

    exam_date = models.DateField()

    # Kinetic Stance
    ADD = 'D'
    ABD = 'B'
    ANGLE_OF_GAIT_CHOICES = (
        (ADD, 'ADD'),
        (ABD, 'ABD'),
    )
    angle_of_gait_left = models.CharField(
        max_length=1, choices=ANGLE_OF_GAIT_CHOICES,
        blank=True
    )
    angle_of_gait_right = models.CharField(
        max_length=1, choices=ANGLE_OF_GAIT_CHOICES,
        blank=True
    )

    base_of_gait = models.CharField(
        max_length=5,
        blank=True
    )

    TOE_HEEL_GAIT = 'T'
    FOREFOOT_SLAP = 'FO'
    EQUINUS = 'E'
    STEPPAGE_GAIT = 'S'
    FESTINATION = 'FE'
    CONTACT_PERIOD_CHOICES = (
        (TOE_HEEL_GAIT, 'Toe Heel Gait'),
        (FOREFOOT_SLAP, 'Forefoot Slap'),
        (EQUINUS, 'Equinus (Uncomp.)'),
        (STEPPAGE_GAIT, 'Steppage Gait'),
        (FESTINATION, 'Festination'),
    )
    contact_period = models.CharField(
        max_length=2, choices=CONTACT_PERIOD_CHOICES,
        blank=True
    )

    EXTENSOR_SUBSTITUION = 'EX'
    ABDUCTORY_TWIST = 'AB'
    EARLY_HEEL_OFF = 'EA'
    SCISSORS_GAIT = 'S'
    ATAXIC_GAIT = 'AT'
    TRENDELENBURG_GAIT = 'T'
    MIDSTANCE_PERIOD_CHOICES = (
        (EXTENSOR_SUBSTITUION, 'Extensor Substitution'),
        (ABDUCTORY_TWIST, 'Abductory Twist'),
        (EARLY_HEEL_OFF, 'Early Heel Off'),
        (SCISSORS_GAIT, 'Scissors Gait'),
        (ATAXIC_GAIT, 'Ataxic Gait'),
        (TRENDELENBURG_GAIT, 'Trendelenburg Gait'),
    )
    midstance_period = models.CharField(
        max_length=2, choices=MIDSTANCE_PERIOD_CHOICES,
        blank=True
    )

    ANTALGIA = 'A'
    CEREBELLAR_GAIT = 'CE'
    CALCANEUS_GAIT = 'CA'
    LACK_OF_1ST_MPJ_DORSIFLEXION = 'L'
    PROPULSIVE_PERIOD_CHOICES = (
        (ANTALGIA, 'Antalgia'),
        (CEREBELLAR_GAIT, 'Cerebellar Gait'),
        (CALCANEUS_GAIT, 'Calcaneus Gait'),
        (LACK_OF_1ST_MPJ_DORSIFLEXION, 'Lack of 1st MPJ Dorsiflexion'),
    )
    propulsive_period = models.CharField(
        max_length=2, choices=PROPULSIVE_PERIOD_CHOICES,
        blank=True
    )

    postural_considerations = models.CharField(
        max_length=64,
        blank=True
    )

    # Static Stance
    SUP = 'S'
    PRO = 'P'
    SUBTALAR_JOINT_CHOICES = (
        (SUP, 'SUP'),
        (PRO, 'PRO'),
    )
    subtalar_joint_left = models.CharField(
        max_length=2, choices=SUBTALAR_JOINT_CHOICES,
        blank=True
    )
    subtalar_joint_right = models.CharField(
        max_length=2, choices=SUBTALAR_JOINT_CHOICES,
        blank=True
    )

    subtalar_joint_comments = models.CharField(
        max_length=64,
        blank=True
    )

    INV = 'I'
    EV = 'E'
    MIDTARSAL_JOINT_CHOICES = (
        (INV, 'INV'),
        (EV, 'EV'),
    )
    midtarsal_joint_left = models.CharField(
        max_length=2, choices=MIDTARSAL_JOINT_CHOICES,
        blank=True
    )
    midtarsal_joint_right = models.CharField(
        max_length=2, choices=MIDTARSAL_JOINT_CHOICES,
        blank=True
    )

    midtarsal_joint_comments = models.CharField(
        max_length=64,
        blank=True
    )

    Y = 'Y'
    N = 'N'
    ANKLE_JOINT_CHOICES = (
        (Y, Y),
        (N, N),
    )
    ankle_joint_knee_extended_left = models.CharField(
        max_length=2, choices=ANKLE_JOINT_CHOICES,
        blank=True
    )
    ankle_joint_knee_extended_right = models.CharField(
        max_length=2, choices=ANKLE_JOINT_CHOICES,
        blank=True
    )
    ankle_joint_knee_flexed_left = models.CharField(
        max_length=2, choices=ANKLE_JOINT_CHOICES,
        blank=True
    )
    ankle_joint_knee_flexed_right = models.CharField(
        max_length=2, choices=ANKLE_JOINT_CHOICES,
        blank=True
    )

    DOR = 'D'
    PLN = 'P'
    FIRST_RAY_CHOICES = (
        (DOR, 'DOR'),
        (PLN, 'PLN'),
    )
    first_ray_left = models.CharField(
        max_length=2, choices=FIRST_RAY_CHOICES,
        blank=True
    )
    first_ray_right = models.CharField(
        max_length=2, choices=FIRST_RAY_CHOICES,
        blank=True
    )

    first_ray_comments = models.CharField(
        max_length=64,
        blank=True
    )

    FULL = 'F'
    LIM = 'L'
    MTP_JOINTS_CHOICES = (
        (FULL, 'FULL'),
        (LIM, 'LIM'),
    )
    first_mtp_joint_left = models.CharField(
        max_length=2, choices=MTP_JOINTS_CHOICES,
        blank=True
    )
    first_mtp_joint_right = models.CharField(
        max_length=2, choices=MTP_JOINTS_CHOICES,
        blank=True
    )

    first_mtp_joint_comments = models.CharField(
        max_length=64,
        blank=True
    )

    lesser_mtp_joints_2_left = models.CharField(
        max_length=2, choices=MTP_JOINTS_CHOICES,
        blank=True
    )
    lesser_mtp_joints_2_right = models.CharField(
        max_length=2, choices=MTP_JOINTS_CHOICES,
        blank=True
    )
    lesser_mtp_joints_3_left = models.CharField(
        max_length=2, choices=MTP_JOINTS_CHOICES,
        blank=True
    )
    lesser_mtp_joints_3_right = models.CharField(
        max_length=2, choices=MTP_JOINTS_CHOICES,
        blank=True
    )
    lesser_mtp_joints_4_left = models.CharField(
        max_length=2, choices=MTP_JOINTS_CHOICES,
        blank=True
    )
    lesser_mtp_joints_4_right = models.CharField(
        max_length=2, choices=MTP_JOINTS_CHOICES,
        blank=True
    )
    lesser_mtp_joints_5_left = models.CharField(
        max_length=2, choices=MTP_JOINTS_CHOICES,
        blank=True
    )
    lesser_mtp_joints_5_right = models.CharField(
        max_length=2, choices=MTP_JOINTS_CHOICES,
        blank=True
    )

    lesser_mtp_joints_comments = models.CharField(
        max_length=64,
        blank=True
    )

    # Treatment Recommendations
    treatment_recommendations = models.TextField(blank=True)

    def get_absolute_url(self):
        return urlresolvers.reverse_lazy(
            'biomechanical_foot_fill_out', kwargs={'claim_pk': self.claim.pk}
        )

    def __str__(self):
        return "Claim ID: {}".format(self.claim_id)


class BiomechanicalGait2(models.Model, model_utils.FieldList):
    patient = models.ForeignKey(Person)

    provider = models.CharField('Insurance', max_length=128)

    weight = models.CharField(max_length=10, blank=True)
    height = models.CharField(max_length=10, blank=True)
    shoe_size = models.CharField(max_length=5, blank=True)

    patient_history = models.TextField(blank=True)

    tight_calf_muscle = models.BooleanField(default=False)
    good_ankle_rom = models.BooleanField(
        verbose_name='good ankle ROM', default=False
    )
    spider_veins = models.BooleanField(default=False)
    shin_splint = models.BooleanField(default=False)

    heel_fat_pad_syndrome = models.BooleanField(default=False)
    plantar_fascitis = models.BooleanField(default=False)
    achilles_tendonitis = models.BooleanField(default=False)
    haglund = models.BooleanField(default=False)

    forefoot_valgus = models.BooleanField(default=False)
    forefoot_varus = models.BooleanField(default=False)
    falling_transverse_arch = models.BooleanField(default=False)
    metatarsalgia = models.BooleanField(default=False)
    morton_neuroma = models.BooleanField(default=False)

    hallux_valgus = models.BooleanField(default=False)
    hallux_rigidus_limitus = models.BooleanField(
        verbose_name='hallux rigidus / limitus', default=False
    )
    first_ray_plantar_flexed = models.BooleanField(
        verbose_name='1st ray plantar-flexed', default=False
    )
    first_ray_dorsi_flexed = models.BooleanField(
        verbose_name='1st ray dorsi-flexed', default=False
    )
    bunion_bunionette = models.BooleanField(
        verbose_name='bunion / bunionette', default=False
    )

    overlapping = models.BooleanField(default=False)
    hammer_toes = models.BooleanField(default=False)
    fungus = models.BooleanField(default=False)
    morton_foot = models.BooleanField(default=False)
    fifth_toe_varus = models.BooleanField(
        verbose_name='5th toe varus', default=False
    )

    pronated_ankle = models.BooleanField(default=False)
    neutral = models.BooleanField(default=False)
    supinated_ankle = models.BooleanField(default=False)

    low_medial_arch = models.BooleanField(default=False)
    medium_medial_arch = models.BooleanField(default=False)
    high_medial_arch = models.BooleanField(default=False)

    heel_valgus = models.BooleanField(default=False)
    heel_rectus = models.BooleanField(default=False)
    heel_varus = models.BooleanField(default=False)

    genu_valgum = models.BooleanField(default=False)
    straight_knees = models.BooleanField(default=False)
    genu_varum = models.BooleanField(default=False)

    varicose = models.BooleanField(default=False)
    leg_length_discrepancy = models.BooleanField(default=False)
    swelling = models.BooleanField(default=False)

    narrow_gait = models.BooleanField(
        verbose_name=(
            'Narrow Gait / Cross Over Gait.'
            ' Propels from 1st Metatarsal'
        ),
        default=False
    )
    toe_in_gait = models.BooleanField(
        verbose_name='Toe-In Gait Propels Through Midstance', default=False
    )
    toe_out_gait = models.BooleanField(
        verbose_name='Toe-Out Gait Propels Off Medial Hallux', default=False
    )
    neutral_gait = models.BooleanField(
        verbose_name=(
            'Neutral Gait Propels of 2nd and'
            ' 3rd MTH Pronation Through Midstance'
        ),
        default=False
    )
    medial_heel_pivot = models.BooleanField(
        verbose_name='Medial Heel Pivot Narrow Heel Base', default=False
    )
    abducted_gait = models.BooleanField(
        verbose_name=(
            'Abducted Gait Propels From Central MTH'
            ' Pronates Through Propultion'
        ),
        default=False
    )

    pes_cavus = models.BooleanField(default=False)
    mild_pes_platus = models.BooleanField(default=False)
    neutral_foot = models.BooleanField(default=False)
    moderate_pes_planus = models.BooleanField(default=False)
    abductovarus_forefoot = models.BooleanField(default=False)
    pes_planovalgus = models.BooleanField(default=False)

    plaster_moulding = models.BooleanField(default=False)
    foam_box = models.BooleanField(default=False)
    three_d_laser_scan = models.BooleanField('3D Laser Scan', default=False)

    high_density_eva = models.BooleanField(
        'High Density EVA 55 Duro', default=False
    )
    dual_density_eva = models.BooleanField(
        'Dual Density EVA 55/35', default=False
    )
    rigid_polyethylene = models.BooleanField(
        'Rigid Polyethylene RC500', default=False
    )

    full = models.BooleanField(default=False)
    sulcus = models.BooleanField(default=False)
    two_3_length = models.BooleanField('2/3', default=False)

    leather = models.BooleanField(default=False)
    poron_ppt = models.BooleanField('Poron PPT', default=False)
    eva_38 = models.BooleanField('EVA 38 duro', default=False)
    spenco = models.BooleanField(default=False)

    mild = models.BooleanField(default=False)
    good = models.BooleanField(default=False)

    lateral_ff = models.BooleanField(
        'Lateral FF Post Lateral RF Post', default=False
    )
    medial_rf = models.BooleanField(
        'Medial RF Post Lateral FF Post', default=False
    )
    rf_post = models.BooleanField(
        'RF Post Heel Cup Medium Arch', default=False
    )
    medial_rf_post_heel_cup = models.BooleanField(
        'Medial RF Post Heel Cup', default=False
    )
    medial_rf_post_medial_ff_post_heel_lift = models.BooleanField(
        'Medial RF Post Medial FF Post Heel Lift', default=False
    )
    medial_rf_post_medial_ff_posting_heel_cup = models.BooleanField(
        'Medial RF Post Medial FF Posting Heel Cup', default=False
    )

    date = models.DateField()

    def get_additional_data(self):
        # track client_id so we can look it up via auditlog
        # update api_helpers.HistoryMixin if this changes
        return {
            'client_id': self.patient_id,
        }

    def get_absolute_url(self):
        url = '{}?toggle=biomechanical_gaits_2#biomechanical_gait_2_{}'.format(
            urlresolvers.reverse(
                'client', kwargs={'client_id': self.patient.get_client().pk}
            ),
            self.pk
        )

        return url

    def __str__(self):
        return "{} - Patient ID: {}".format(self.provider, self.patient_id)
