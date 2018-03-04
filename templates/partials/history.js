// History
function getActorStr(actor) {
    var str = '';
    if (actor) {
        if (actor.first_name) {
            str += actor.first_name;
            if (actor.last_name) {
                str += ' ' + actor.last_name;
            }
        }
        else {
            str += actor.email;
        }
    }

    return str;
}

function title(text) {
    // capitalize all words
    var title = text.replace(/\b\w/g, function (first_letter) {
        return first_letter.toUpperCase();
    });

    return title;
}

// define url before including this
var history_fetched = false;
$('#history_panel').on('show.bs.collapse', function() {
    if (history_fetched) { return; }

    $history_msg = $('#history_msg');
    $history_msg.text(' loading...');

    $.get(url).done(function(data) {
        if (data) {
            var history = data.history;
            for (var i = history.length - 1; i >= 0; --i) {
                var history_item = history[i];

                var $tr = $('#history_item');
                var $trClone = $tr.clone();

                for (var key in history_item) {
                    var data = history_item[key];
                    var requiresTitle = (
                        [
                            'content_type', 'get_action_display'
                        ].indexOf(key) !== -1
                    )
                    if (key === 'actor') {
                        data = getActorStr(data);
                    }
                    else if (requiresTitle) {
                        data = title(data);
                    }
                    else if (key ==='changes') {
                        $trClone.find('.' + key).html(data);

                        continue;
                    }
                    $trClone.find('.' + key).text(data);
                }

                $trClone.show();
                $tr.after($trClone);
            }
            if (!history.length) {
                $('#no-history-msg').show();
            }
            history_fetched = true;
            $history_msg.fadeOut();
        }
        else {
            $.post(
                "{% url 'js_reporter' %}",
                {'url': url, 'json': JSON.stringify(data)}
            );

            window.alert(
                'Something went wrong...'
            );
        }
    }).fail(function(xhr) {
        var response = xhr.responseText;
        var json = {};
        try {
            json = JSON.parse(response);
            response = '';
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

        $.post(
            "{% url 'js_reporter' %}",
            {
                'url': url,
                'json': JSON.stringify(json),
                'response': response,
            }
        );

        window.alert(msg);
    });
});
