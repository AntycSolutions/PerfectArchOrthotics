import collections


class FieldList():

    def get_all_fields(self):
        """Returns a list of all field names on the instance."""
        Field = collections.namedtuple('Field', ['field', 'value'])

        # use OrderedDict so we can look up values later on
        fields = collections.OrderedDict()
        for f in self._meta.fields:
            fname = f.name
            # resolve picklists/choices, with get_xyz_display() function
            get_choice = 'get_' + fname + '_display'
            if hasattr(self, get_choice):
                value = getattr(self, get_choice)()
            else:
                try:
                    value = getattr(self, fname)
                except:
                    print("Could not get value of field.")
                    value = None

            if f.editable:
                fields.update({f.name: Field(f, value)})

        return fields
