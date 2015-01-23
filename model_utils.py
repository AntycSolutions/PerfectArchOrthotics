import collections


class FieldList():

    def get_all_fields(self):
        """Returns a list of all field names on the instance."""
        Fields = collections.namedtuple('Fields', ['labels',
                                                   'name_values'])

        # use OrderedDict so we can look up values later on
        name_values = collections.OrderedDict()
        labels = []
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
                name_values.update({f.name: value})
                labels.append(f.verbose_name)

        return Fields(labels, name_values)
