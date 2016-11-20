
function display_claim(order_type_value, claim, form) {
    // console.log(order_type_value, claim, form);
    var ORTHOTICS = 'o';
    if (order_type_value == ORTHOTICS) {
        // parent is col parent is form-group
        claim.parent().parent().show();
    }
    else {
        claim.parent().parent().hide();
    }
}

function form_callback(form) {
    var order_type = form.find('#id_order_type');
    var claim = form.find('#id_claim');

    display_claim(order_type.val(), claim, form);

    order_type.change(function() {
        display_claim($(this).val(), claim, form);
    });
}
