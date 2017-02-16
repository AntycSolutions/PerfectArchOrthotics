(function(reminders) {

    reminders.reminders_init = function(benefits_lookup) {
        var REQUIRED = 'r';
        var EMAIL = 'e';
        var TEXT = 't';
        var CALL = 'c';
        var COMPLETED = 'o';

        var NO_ANSWER = 'n';
        var VOICEMAIL = 'v';

        var ASSIGNMENT = 'a';

        var value_in_list = function(list, value) {
            return list.indexOf(value) !== -1;
        }

        var get_follow_up_vals = function(model_name, pk) {
            if (typeof model_name === 'undefined' && typeof pk === 'undefined') {
                throw new Error('incorrect arguments for get_follow_up_vals');
            }

            var follow_up = $(
                '#' + model_name + '_' + pk + '_follow_up'
            ).text().trim();
            var follow_up_vals = [];
            if (value_in_list(follow_up, 'Required')) {
                follow_up_vals.push(REQUIRED);
            }
            if (value_in_list(follow_up, 'Text')) {
                follow_up_vals.push(TEXT);
            }
            if (value_in_list(follow_up, 'Email')) {
                follow_up_vals.push(EMAIL);
            }
            if (value_in_list(follow_up, 'Call')) {
                follow_up_vals.push(CALL);
            }
            if (value_in_list(follow_up, 'Completed')) {
                follow_up_vals.push(COMPLETED);
            }
            if (!follow_up_vals) {
                throw new Error('Missing follow up value');
            }

            return follow_up_vals;
        }

        var reminder_modal_init = function(event) {
            var btn = $(event.relatedTarget);
            var pk = btn.data('pk');
            var model_name = btn.data('model-name');
            var modal = $(this);

            var follow_up_vals = get_follow_up_vals(model_name, pk);
            modal.find(
                'input[name="' + model_name + '-follow_up"]'
            ).val(follow_up_vals);

            var result = $(
                '#' + model_name + '_' + pk + '_result'
            ).text().trim();
            if (result === 'No answer') {
                result = NO_ANSWER;
            }
            else if (result === 'Voicemail') {
                result = VOICEMAIL;
            }
            else if (result === '') {
                // pass
            }
            else {
                throw new Error('Unhandled result ' + result);
            }
            modal.find('#id_' + model_name + '-result').val(result);

            modal.find('#' + model_name + '_pk').val(pk);

            var logs = btn.data('logs') || [];
            var logs_tbody = modal.find('#' + model_name + '_logs');
            logs_tbody.html('');
            for (var i = 0; i < logs.length; ++i) {
                var log = logs[i];
                logs_tbody.append(
                    $('<tr>').append(
                        $('<td>').text(log.type)
                    ).append(
                        $('<td>').text(log.created)
                    )
                );
            }
            var table_div = logs_tbody.parent().parent();
            logs.length ? table_div.show() : table_div.hide();

            // hide options
            if (benefits_lookup[pk] == ASSIGNMENT) {
                var text = modal.find('input[value="' + TEXT + '"]');
                text.prop('checked', false);
                text.parent().hide();
                var email = modal.find('input[value="' + EMAIL + '"]');
                email.prop('checked', false);
                email.parent().hide();
            }
            else {
                var text = modal.find('input[value="' + TEXT + '"]');
                text.parent().show();
                var email = modal.find('input[value="' + EMAIL + '"]');
                email.parent().show();
            }
        }
        $('#unpaidclaimreminder_modal').on(
            'show.bs.modal', reminder_modal_init
        );
        $('#orderarrivedreminder_modal').on(
            'show.bs.modal', reminder_modal_init
        );

        var months = [
            'Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 'Jul.', 'Aug.',
            'Sep.', 'Oct.', 'Nov.', 'Dec.',
        ];

        var reminder_save = function() {
            var form_id = $(this).attr('form-id');
            var form = $(form_id);

            var model_name = form.find('#model_name').val();

            var follow_up = [];
            form.find(
                'input[name="' + model_name + '-follow_up"]:checked'
            ).each(
                function() { follow_up.push($(this).val()); }
            );
            if (!follow_up.length) {
                window.alert('Please select a Follow up action.');
                return;
            }

            var pk = form.find('#' + model_name + '_pk').val();

            var old_follow_up = get_follow_up_vals(model_name, pk);
            var msg = '';
            var sending_email = (
                value_in_list(follow_up, EMAIL) &&
                !value_in_list(old_follow_up, EMAIL)
            );
            if (sending_email) {
                msg += 'Send email?';
            }
            var sending_text = (
                value_in_list(follow_up, TEXT) &&
                !value_in_list(old_follow_up, TEXT)
            );
            if (sending_text) {
                if (msg) { msg += '\nand\n'; }
                msg += 'Send text message?';
            }
            if (msg.length) {
                var c = window.confirm(msg);
                if (!c) { return; }
            }

            var result = form.find('#id_' + model_name + '-result').val();

            var data = {'follow_up': follow_up, 'result': result};

            var url = Urls['reminders:' + model_name + '_update'](pk);
            $.ajax(
                // traditional prevents jquery from appending [] to follow_up
                {url: url, data: data, method: "POST", traditional: true}
            ).done(function(data) {
                if ('pk' in data) {
                    var follow_up_vals = [];
                    if (value_in_list(follow_up, REQUIRED)) {
                        follow_up_vals.push('Required');
                    }
                    if (value_in_list(follow_up, TEXT)) {
                        follow_up_vals.push('Text');
                    }
                    if (value_in_list(follow_up, EMAIL)) {
                        follow_up_vals.push('Email');
                    }
                    if (value_in_list(follow_up, CALL)) {
                        follow_up_vals.push('Call');
                    }
                    if (value_in_list(follow_up, COMPLETED)) {
                        follow_up_vals.push('Completed');
                    }
                    if (!follow_up_vals.length) {
                        // defaults to Required
                    }
                    $('#' + model_name + '_' + pk + '_follow_up').html(
                        follow_up_vals.join(',<br />')
                    );

                    var calling = (
                        value_in_list(follow_up, CALL) &&
                        !value_in_list(old_follow_up, CALL)
                    );
                    if (sending_text || sending_email || calling) {
                        var logs = $(
                            '#' + model_name + '_' + pk + '_modal_btn'
                        ).data('logs');

                        var d = new Date();
                        var now = (
                            months[d.getMonth()] + ' ' +
                            d.getDate() + ', ' +
                            d.getFullYear() + ', ' +
                            (d.getHours() % 12 || 12) + ':' + // 24 -> 12
                            ('0' + d.getMinutes()).slice(-2) + ' ' + // 0 pad
                            ((d.getHours() >= 12) ? 'p.m.' : 'a.m.')
                        );

                        var type = '';
                        if (sending_text) {
                            type = 'Text';
                            logs.push({"type": type, "created": now});
                        }
                        if (sending_email) {
                            type = 'Email';
                            logs.push({"type": type, "created": now});
                        }
                        if (calling) {
                            type = 'Call';
                            logs.push({"type": type, "created": now});
                        }
                        if (!type) {
                            throw new Error('Unhandled message type');
                        }
                    }

                    if (result === NO_ANSWER) {
                        result = 'No answer';
                    }
                    else if (result === VOICEMAIL) {
                        result = 'Voicemail';
                    }
                    else if (result === '') {
                        // pass
                    }
                    else {
                        throw new Error('Unhandled result: ' + result);
                    }
                    $('#' + model_name + '_' + pk + '_result').text(result);

                    $('#' + model_name + '_modal').modal('hide');
                }
                else {
                    window.alert(
                        'Something went wrong... but the message was sent'
                    );
                }
            }).fail(function(xhr) {
                var json = {};
                try {
                    json = JSON.parse(xhr.responseText);
                }
                catch (e) {
                    // pass
                    console.log('Could not parse json');
                }
                var msg = '';
                if ('error' in json) {
                    msg = json['error'];
                }
                else {
                    for (var key in json) {
                        msg += json[key] + '\n';
                    }
                }
                if (!msg.length) {
                    msg = 'Something went wrong...';
                }
                window.alert(msg);
            });
        }
        $('#unpaidclaimreminder_save').on('click', reminder_save);
        $('#orderarrivedreminder_save').on('click', reminder_save);
    }

}(window.reminders = window.reminders || {}));
