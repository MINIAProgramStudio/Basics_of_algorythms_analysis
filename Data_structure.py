import copy

class TreeNode:
    def __init__(self, value, pointers = [], left = None, right = None):
        self.value = value
        self.pointers  = pointers
        self.left = left
        self.right = right
    def all(self):
        output = self.pointers
        if not self.left is None:
            output += self.left.all()
        if not self.right is None:
            output += self.right.all()
        return output
    def equal(self, value):
        if value == self.value:
            return self.pointers
        elif value < self.value:
            if self.left is None:
                return []
            else:
                return self.left.equal(None)
        else:
            if self.right is None:
                return []
            else:
                return self.right.equal(None)
    def less_than(self, value):
        if value > self.value:
            output = self.pointers
            if not self.left is None:
                output += self.left.all()
            return output
        else:
            output = []
            if not self.left is None:
                output += self.left.less_than(value)
            return output
    def greater_than(self, value):
        if value > self.value:
            output = self.pointers
            if not self.right is None:
                output += self.right.all()
            return output
        else:
            output = []
            if not self.right is None:
                output += self.right.greater_than(value)
            return output
    def add_pointer(self,pointer,value):
        if value == self.value:
            if not pointer in self.pointers:
                self.pointers.append(pointer)
        elif value < self.value:
            if self.left is None:
                self.left = TreeNode(value,[pointer])
            else:
                self.left.add_pointer(pointer,value)
        else:
            if self.right is None:
                self.right = TreeNode(value,[pointer])
            else:
                self.right.add_pointer(pointer,value)

class BinarySearchTree:
    def __init__(self):
        self.root = None
    def append(self, pointer, value):
        if self.root is None:
            self.root = TreeNode(value, [pointer])
        else:
            self.root.add_pointer(pointer, value)

    def equal(self, value):
        return self.root.equal(value)
    def greater_than(self, value):
        return self.root.greater_than(value)
    def less_than(self,value):
        return self.root.greater_than


class Table:
    def __init__(self, column_names, indexing = False):
        self.column_names = column_names
        if indexing:
            self.indexing = []
            for index in indexing:
                if index:
                    self.indexing.append(BinarySearchTree())
                else:
                    self.indexing.append(False)
        self.rows = []
    def __str__(self):
        output = str(self.column_names)
        output += ["\n"+str(row) for row in self.rows]
        return output
    def insert(self, row):
        self.rows.append(row)
        if self.indexing:
            for column in range(len(self.column_names)):
                if self.indexing[column]:
                    self.indexing[column].append(self.rows[-1], row[column])


    def select(self, aggregation = False, condition = False, group_by_columns = False):
        rows_to_return = []
        if condition:
            if condition[0] in self.column_names:
                if condition[1] in self.column_names:
                    rows_to_return = copy.deepcopy(self.rows)
                    column_1 = self.column_names.index(condition[0])
                    column_2 = self.column_names.index(condition[1])
                    i = len(rows_to_return) - 1
                    while i > 0:
                        if not rows_to_return[i][column_1] == rows_to_return[i][column_2]:
                            rows_to_return.pop(i)
                        i -= 1
                else:
                    column = self.column_names.index(condition[0])
                    value = int(condition[1])
                    if self.indexing[column]:
                        rows_to_return = copy.deepcopy(self.indexing[column].equal(value))
                    else:
                        rows_to_return = copy.deepcopy(self.rows)
                        i = len(rows_to_return) - 1
                        while i > 0 :
                            if not rows_to_return[i][column] == value:
                                rows_to_return.pop(i)
                            i-=1
            else:
                return -3 # no such column
        else:
            rows_to_return = copy.deepcopy(self.rows)
        # end if condition////////////////////////////////////////////////////////////////////////////////////////////

        if group_by_columns:
            delimiter = len(group_by_columns)
            group_by_columns_names = group_by_columns
            group_by_columns = [self.column_names.index(i) for i in group_by_columns]
            raw_rows = copy.deepcopy(rows_to_return)
            rows_to_return = []
            for row in raw_rows:
                row = [row[i] for i in group_by_columns]
                if not row in rows_to_return:
                    rows_to_return.append(row)

            if aggregation:
                for pair in aggregation:
                    function = pair[0]
                    column = pair[1]
                    if not column in self.column_names:
                        return -3  # no such column
                    group_by_columns_names.append(str(function) + "(" + str(column) + ")")
                    column = self.column_names.index(column)
                    match function:
                        case "COUNT":
                            rows_for_search = [i[:delimiter] for i in rows_to_return]
                            for row in raw_rows:
                                grouped_row = [row[i] for i in group_by_columns]
                                if len(rows_to_return[rows_for_search.index(grouped_row)]) < len(group_by_columns_names):
                                    rows_to_return[rows_to_return.index(grouped_row)].append(1)
                                else:
                                    rows_to_return[rows_for_search.index(grouped_row)][-1] += 1
                        case "MAX":
                            for row in raw_rows:
                                grouped_row = [row[i] for i in group_by_columns]
                                if len(rows_to_return[rows_for_search.index(grouped_row)]) < len(group_by_columns_names):
                                    rows_to_return[rows_for_search.index(grouped_row)].append(row[column])
                                else:
                                    rows_to_return[rows_for_search.index(grouped_row)][-1] = max(row[column], rows_to_return[rows_to_return.index(grouped_row)][-1])
                        case "AVG":
                            counter = [0]*len(rows_to_return)
                            for row in raw_rows:
                                grouped_row = [row[i] for i in group_by_columns]
                                if len(rows_to_return[rows_for_search.index(grouped_row)]) < len(group_by_columns_names):
                                    rows_to_return[rows_for_search.index(grouped_row)].append(row[column])
                                    counter[rows_for_search.index(grouped_row)] += 1
                                else:
                                    rows_to_return[rows_for_search.index(grouped_row)][-1] += row[column]
                                    counter[rows_for_search.index(grouped_row)] += 1

                            i = 0
                            while i < len(rows_to_return):
                                rows_to_return[i][-1] = float(rows_to_return[i][-1]) / float(counter[i])
                                i+=1
                        case _:
                            return -4 # no such function
            # end if aggregation///////////////////////////////////////////////////////////////////////////////////////
            return [group_by_columns_names, rows_to_return]
        # end if group_by_columns///////////////////////////////////////////////////////////////////////////////////////
        return [self.column_names, rows_to_return]






class Data:
    def __init__(self):
        self.tables = {}

    def __str__(self):
        output = "There are "+str(len(self.tables.keys()))+" tables:"
        for key in self.tables.keys():
            output += "\n"+key
        return output

    def create(self, table_name, column_names, indexing = False):
        if table_name in self.tables.keys():
            return -2 # table already exists
        if indexing:
            if len(indexing) != len(column_names):
                return -3 # number of column names and number of values in indexing list must match
        self.tables[table_name] = Table(column_names, indexing)
        return 0

    def insert(self, table_name, values):
        if not table_name in self.tables.keys():
            return -2 # table does not exist
        if not len(self.tables[table_name].column_names) == len(values):
            return -3 # invalid number of values
        self.tables[table_name].insert(values)
        return 0

    def select(self, table_name, aggregation = False, condition = False, group_by_columns = False):
        if not table_name in self.tables.keys():
            return -2  # table does not exist
        return self.tables[table_name].select(aggregation,condition,group_by_columns)

