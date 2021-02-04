class ArXivManuscriptIdRaw:
    def __init__(self, id_string):
        self.id_string = id_string

    def id(self):
        """
        Converts ArXiv id into its base form (i.e. removes revision number if present)
        """
        if 'v' in self.id_string:
            return self.id_string.split('v')[0]
        return self.id_string
