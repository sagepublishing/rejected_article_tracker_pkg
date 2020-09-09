class ManuscriptIdRaw:
    def __init__(self, id_string):
        self.id_string = id_string

    def id(self):
        """
        Coverts ScholarOne MS_ID into its base form (i.e. removes revision number if present)
        """
        if '.R' in self.id_string:
            return self.id_string.split('.R')[0]
        return self.id_string
