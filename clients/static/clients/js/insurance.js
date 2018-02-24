(function(generic_template) {

    function display_period_date(period_value, form, form_count) {
        var period_date = form.find(
            '#id_coverage_set-' + form_count + '-period_date'
        );

        // console.log(period_value, form, form_count, period_date);
        if (period_value == '1') {
            // parent is input-group parent is col parent is form-group
            period_date.parent().parent().parent().show();
        }
        else {
            period_date.parent().parent().parent().hide();
        }
    }

    generic_template.formset_add_form_callback = function(form, form_count) {
        var period = form.find('#id_coverage_set-' + form_count + '-period');

        display_period_date(period.val(), form, form_count);

        period.change(function() {
            display_period_date($(this).val(), form, form_count);
        });
    };

}(window.generic_template = window.generic_template || {}));
