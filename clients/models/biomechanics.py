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
