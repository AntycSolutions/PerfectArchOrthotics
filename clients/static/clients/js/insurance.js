
function display_period_date(period_value, form, form_count) {
    var period_date = form.find(
        '#id_coverage_set-' + form_count + '-period_date'
    );

    // console.log(period_value, form, form_count, period_date);
    if (period_value == '1') {
        // parent is col parent is form-group
        period_date.parent().parent().show();
    }
    else {
        period_date.parent().parent().hide();
    }
}

function formset_add_form_callback(form, form_count) {
    var period = form.find('#id_coverage_set-' + form_count + '-period');

    display_period_date(period.val(), form, form_count);

    period.change(function() {
        display_period_date($(this).val(), form, form_count);
    });
}
