
STATIC_URL = '/static/'

# Django Pipeline
PIPELINE = {
    # if there are multiple source_filesnames and DEBUG = True
    #  we need to define debug_keys to keep fallback key unique
    'STYLESHEETS': {
        # templates
        'base': {
            'source_filenames': (
                'css/sticky-footer.css',
                'css/base.css',
                'session_security/style.css',
            ),
            'output_filename': 'css/base_all.css',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'base_all_css',
                'debug_fallback_keys': {
                    STATIC_URL + 'css/sticky-footer.css': 'sticky_footer_css',
                    STATIC_URL + 'css/base.css': 'base_css',
                    STATIC_URL + 'session_security/style.css': 'style_css',
                },
            },
        },
        'index': {
            'source_filenames': (
                'css/index.css',
            ),
            'output_filename': 'css/index_all.css',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'index_all_css',
            },
        },
        # clients
        'biomechanical_foot': {
            'source_filenames': (
                'clients/css/biomechanical_foot.css',
            ),
            'output_filename': 'css/biomechanical_foot_all.css',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'biomechanical_foot_all_css',
            },
        },
        'biomechanical_gait': {
            'source_filenames': (
                'clients/css/biomechanical_gait.css',
                'utils/css/typeahead.css',
            ),
            'output_filename': 'css/biomechanical_gait_all.css',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'biomechanical_gait_all_css',
                'debug_fallback_keys': {
                    STATIC_URL + 'clients/css/biomechanical_gait.css':
                        'biomechanical_gait_css',
                    STATIC_URL + 'utils/css/typeahead.css': 'typeahead_css',
                },
            },
        },
        'biomechanical_gait_2': {
            'source_filenames': (
                'clients/css/biomechanical_gait_2.css',
                'utils/css/typeahead.css',
            ),
            'output_filename': 'css/biomechanical_gait_2_all.css',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'biomechanical_gait_2_all_css',
                'debug_fallback_keys': {
                    STATIC_URL + 'clients/css/biomechanical_gait_2.css':
                        'biomechanical_gait_2_css',
                    STATIC_URL + 'utils/css/typeahead.css': 'typeahead_css',
                },
            },
        },
        'insurance': {
            'source_filenames': (
                'clients/css/insurance.css',
            ),
            'output_filename': 'css/insurance_all.css',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'insurance_all_css',
            },
        },
        'client': {
            'source_filenames': (
                'clients/css/client.css',
                'clients/css/form-static.css',
                'clients/css/anchor.css',
            ),
            'output_filename': 'css/client_all.css',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'client_all_css',
                'debug_fallback_keys': {
                    STATIC_URL + 'clients/css/client.css': 'client_css',
                    STATIC_URL + 'clients/css/form-static.css':
                        'form_static_css',
                    STATIC_URL + 'clients/css/anchor.css': 'anchor_css',
                },
            },
        },
        'claim': {
            'source_filenames': (
                'clients/css/form-static.css',
            ),
            'output_filename': 'css/claim_all.css',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'claim_all_css',
            },
        },
        # inventory
        'order_list': {
            'source_filenames': (
                'inventory/css/order_list.css',
            ),
            'output_filename': 'css/order_list_all.css',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'order_list_all_css',
            },
        },
        # reminders
        'reminders': {
            'source_filenames': (
                'utils/css/typeahead.css',
            ),
            'output_filename': 'css/reminders_all.css',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'reminders_all_css',
            },
        },
    },
    'JAVASCRIPT': {
        'base': {
            'source_filenames': (
                'session_security/script.js',
            ),
            'output_filename': 'js/base_all.js',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'base_all_js',
            },
        },
        # clients
        'client': {
            'source_filenames': (
                'utils/jquery_utils/ajax.js',
                'reminders/reminders.js',
            ),
            'output_filename': 'js/client_all.js',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'client_all_js',
            },
        },
        'insurance': {
            'source_filenames': (
                'clients/js/insurance.js',
            ),
            'output_filename': 'js/insurance_all.js',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'insurance_all_js',
            },
        },
        'claims': {
            'source_filenames': (
                'utils/jquery_utils/ajax.js',
            ),
            'output_filename': 'js/claims_all.js',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'claims_all_js'
            },
        },
        # inventory
        'coverage_order': {
            'source_filenames': (
                'inventory/js/coverage_order.js',
            ),
            'output_filename': 'js/coverage_order_all.js',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'coverage_order_all_js',
            },
        },
        # reminders
        'reminders': {
            'source_filenames': (
                'utils/jquery_utils/ajax.js',
                'reminders/reminders.js',
            ),
            'output_filename': 'js/reminders_all.js',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'reminders_all_js',
                'debug_fallback_keys': {
                    STATIC_URL + 'utils/jquery_utils/ajax.js': 'ajax_js',
                    STATIC_URL + 'reminders/reminders.js': 'reminders_js',
                },
            },
        },
    },
}
