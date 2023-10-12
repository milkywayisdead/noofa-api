class DfPreparer:
    def __init__(self, db):
        self.db = db

    @property
    def records(self):
        return self.db.to_dict(orient='records')