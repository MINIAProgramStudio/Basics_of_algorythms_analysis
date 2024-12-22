class Table:
    def __init__(self, column_names):
        self.column_names = column_names
        self.rows = []
    def __str__(self):
        output = str(self.column_names)
        output += ["\n"+str(row) for row in self.rows]
        return output
    def insert(self, row):
        self.rows.append(row)


class Data:
    def __init__(self):
        self.tables = {}

    def __str__(self):
        output = "There are "+len(self.tables.keys())+" tables:"
        for key in self.tables.keys():
            output += "\n"+key
        return output

    def create(self, table_name, column_names):
        if table_name in self.tables.keys():
            return -2 # table already exists
        self.tables[table_name] = Table(column_names)
        return 0

    def insert(self, table_name, values):
        if not table_name in self.tables.keys():
            return -2 # table does not exist
        if not len(self.tables[table_name].column_names) == len(values):
            return -3 # invalid number of values

        self.tables[table_name].insert(values)
        return 0