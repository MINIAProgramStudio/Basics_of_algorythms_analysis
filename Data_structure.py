class Table:
    def __init__(self, column_names):
        self.column_names = column_names
        self.rows = []
    def __str__(self):
        output = ["\n"+str(row) for row in self.rows]

class Data:
    def __init__(self):
        self.tables = {}

    def create(self, table_name, column_names):
        if table_name in self.tables.keys():
            return -2 # table already exsists
        self.tables[table_name] = Table(column_names)
        return 0

    def __str__(self):
        output = "There are "+len(self.tables)" tables:"
        for key in self.tables.keys():
            output += "\n"+key
        return output