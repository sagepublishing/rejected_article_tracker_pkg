class AuthorNames:
    def __init__(self, names_string):
        self.names_string = self.__required(names_string)

    def names(self):
        """
        Converts name into a simple form suitable for the CrossRef search
        """
        names = self.names_string.split(';')
        out = list(map(self.__parse_name, names))
        return ', '.join(out)

    @staticmethod
    def __parse_name(full_name):
        return '+'.join(reversed([name.strip() for name in full_name.split(',')]))

    @staticmethod
    def __required(item):
        if not item:
            raise ValueError('field "authors" is required')
        return item
