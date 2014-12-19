// Claim

$(document).ready(function() {
    // Show selected insurance's coverage types (or help msg)
    var insurance_class = '.insurance_' + $('#id_insurance').val();
    var insurance_selected = $(insurance_class);
    insurance_selected.show();
    // Disable other insurance's coverage types
    $('.insurance_content input').attr('disabled', 'disabled');
    // Enable selected insurance's coverage types
    $(insurance_class + ' input').removeAttr('disabled');

    var coverage_type_content_msg = $('.coverage_type_content_msg');
    // Show selected coverage type's items (or help msg)
    var show_coverage_type_content_message = true;
    $('.coverage_type_trigger').each(function() {
        coverage_type_content = '.' + $(this).data('rel');
        if ($(this).is(':checked')) {
            $(coverage_type_content).show();
            // Enable selected insurance's coverage types
            $(coverage_type_content + ' input').removeAttr('disabled');
            show_coverage_type_content_message = false;
        }
        else {
            $(coverage_type_content + ' input')
                .attr('disabled', 'disabled');
        }
    }).promise().done(function() {
        if (show_coverage_type_content_message) {
            coverage_type_content_msg.show();
        }
    });

    $('.insurance_trigger').change(function() {
        var value = this.value;
        // Hide other insurance's coverage types
        $('.insurance_content').hide('slow').promise().done(function() {
            // Show selected insurance's coverage types
            $('.insurance_' + value).show('slow');
        });
        $('.insurance_content input').attr('disabled', 'disabled');
        $('.insurance_' + value + ' input').removeAttr('disabled');
    });
    var ct_msg = 0;
    $('.coverage_type_trigger').click(function() {
        var rows_len = $('.' + $(this).data('rel') + ' .div_tr').length;
        var slide_time = rows_len * 50;
        if($(this).is(':checked')) {
            ct_msg++;
            if (ct_msg > 0) {
                coverage_type_content_msg.hide('slow');
            }
            // Show selected coverage types's items
            $('.' + $(this).data('rel')).delay(600).show(slide_time);
            $('.' + $(this).data('rel') + ' input').removeAttr('disabled');
        }
        else {
            // Hide selected coverage types's items
            $('.' + $(this).data('rel')).hide(slide_time);
            $('.' + $(this).data('rel') + ' input').attr('disabled',
                                                         'disabled');
            ct_msg--;
            if (ct_msg <= 0) {
                coverage_type_content_msg
                    .delay(slide_time).show('slow');
            }
        }
    });
});
