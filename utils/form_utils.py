from django.forms import widgets
from django.utils import safestring


class ConfirmFileWidget(widgets.ClearableFileInput):
    script = '''
        <script>
            document.getElementById("%(form_id)s").addEventListener(
                "submit", function(event) {
                    var clear = document.getElementById("%(clear_id)s");
                    var file = document.getElementById("%(file_field_id)s");
                    if (clear.checked) {
                        var c = confirm("Are you sure you want to clear"
                                        + " %(file_name)s?");
                        if (!c) { event.preventDefault(); }
                    }
                }
            );
        </script>
    '''

    def __init__(self, *args, **kwargs):
        if 'form_id' not in kwargs:
            raise Exception('ConfirmFileWidget requires the form id.')
        if 'form' not in kwargs:
            raise Exception('ConfirmFileWidget requires the form instance.')

        self.form_id = kwargs.pop('form_id')
        self.form = kwargs.pop('form')

        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        html = super().render(name, value, attrs)
        if name in self.form.initial and self.form.initial[name]:
            html += self.script % {
                'file_field_id': attrs['id'],
                'clear_id': '{0}-clear_id'.format(name),
                'form_id': self.form_id,
                'file_name': self.form.initial[name]
            }

        return safestring.mark_safe(html)
