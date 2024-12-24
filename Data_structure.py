import copy
import time

class TreeNode:
    def __init__(self, value, parent = None, pointers = [], left = None, right = None):
        self.parent = parent
        self.value = value
        self.pointers  = pointers
        self.left = left
        self.right = right
    def height(self):
        if self.right is None:
            if self.left is None:
                return 1
            else:
                return self.left.height() + 1
        else:
            if self.left is None:
                return self.right.height() + 1
            else:
                return max(self.right.height(), self.left.height()) + 1
    def balance_factor(self):
        if self.right is None:
            if self.left is None:
                return 0
            else:
                return -self.left.height()
        else:
            if self.left is None:
                return self.right.height()
            else:
                return self.right.height() - self.left.height()
    def all(self):
        if self.left is None:
            if self.right is None:
                return self.pointers
            else:
                return self.pointers + self.right.all()
        else:
            if self.right is None:
                return self.pointers + self.left.all()
            else:
                return self.pointers + self.left.all() + self.right.all()
    def equal(self, value):
        if value == self.value:
            return self.pointers
        elif value < self.value:
            if self.left is None:
                return []
            else:
                return self.left.equal(value)
        else:
            if self.right is None:
                return []
            else:
                return self.right.equal(value)
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
            if self.right is None:
                return self.pointers
            else:
                return self.pointers + self.right.all()
        else:
            if self.right is None:
                return []
            else:
                return self.pointers + self.right.greater_than(value)
    def add_pointer(self,pointer,value):
        balancing_needed = 0
        if value == self.value:
            if not pointer in self.pointers:
                self.pointers.append(pointer)
                return 0
        elif value < self.value:
            if self.left is None:
                self.left = TreeNode(value, parent =  self, pointers = [pointer])
                return 1
            else:
                balancing_needed = self.left.add_pointer(pointer,value)

        else:
            if self.right is None:
                self.right = TreeNode(value, parent =  self, pointers = [pointer])
                return 1
            else:
                balancing_needed = self.right.add_pointer(pointer,value)

        if balancing_needed == 0:
            return 0

        bf = self.balance_factor()


        if bf == 0:
            return 0
        if bf == 1:
            return 1
        if bf > 0:
            if self.right.left is None:
                self.right.rotate_left()
            else:
                self.right.rotate_right()
                self.right.parent.rotate_left()
        else:
            if self.left.right is None:
                self.left.rotate_right()
            else:
                self.left.rotate_left()
                self.left.parent.rotate_right()
        return 1




    def rotate_left(self):
        new_root = self.right
        self.right = new_root.left
        if new_root.left:
            new_root.left.parent = self
        new_root.parent = self.parent
        if self.parent is None:
            pass # Root node case
        elif self == self.parent.left:
            self.parent.left = new_root
        else:
            self.parent.right = new_root
        new_root.left = self
        self.parent = new_root

    def rotate_right(self):
        new_root = self.left
        self.left = new_root.right
        if new_root.right:
            new_root.right.parent = self
        new_root.parent = self.parent
        if self.parent is None:
            pass # Root node case
        elif self == self.parent.right:
            self.parent.right = new_root
        else:
            self.parent.left = new_root
        new_root.right = self
        self.parent = new_root


class BinarySearchTree:
    def __init__(self):
        self.root = None
    def append(self, pointer, value):
        if self.root is None:
            self.root = TreeNode(value, None, [pointer])
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
        else:
            self.indexing = False
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
        rows_to_return = [[]]*len(self.rows)
        if condition:
            if condition[0] in self.column_names:
                if condition[1] in self.column_names:
                    match condition[2]:
                        case "=":
                            column_1 = self.column_names.index(condition[0])
                            column_2 = self.column_names.index(condition[1])
                            for i in range(len(self.rows)):
                                if self.rows[i][column_1] == self.rows[i][column_2]:
                                    rows_to_return[rows_to_return.index([])] = self.rows[i]
                        case ">":
                            column_1 = self.column_names.index(condition[0])
                            column_2 = self.column_names.index(condition[1])
                            for i in range(len(self.rows)):
                                if self.rows[i][column_1] > self.rows[i][column_2]:
                                    rows_to_return[rows_to_return.index([])] = self.rows[i]
                        case "<":
                            column_1 = self.column_names.index(condition[0])
                            column_2 = self.column_names.index(condition[1])
                            for i in range(len(self.rows)):
                                if self.rows[i][column_1] < self.rows[i][column_2]:
                                    rows_to_return[rows_to_return.index([])] = self.rows[i]

                else:
                    match condition[2]:
                        case "=":
                            column = self.column_names.index(condition[0])
                            value = int(condition[1])
                            if self.indexing:
                                if self.indexing[column]:
                                    rows_to_return = copy.deepcopy(self.indexing[column].equal(value))
                                else:
                                    for i in range(len(self.rows)):
                                        if self.rows[i][column] == value:
                                            rows_to_return[rows_to_return.index([])] = self.rows[i]
                            else:
                                for i in range(len(self.rows)):
                                    if self.rows[i][column] == value:
                                        rows_to_return[rows_to_return.index([])] = self.rows[i]
                        case ">":
                            column = self.column_names.index(condition[0])
                            value = int(condition[1])
                            if self.indexing:
                                if self.indexing[column]:
                                    rows_to_return = copy.deepcopy(self.indexing[column].greater_than(value))
                                else:
                                    for i in range(len(self.rows)):
                                        if self.rows[i][column] > value:
                                            rows_to_return[rows_to_return.index([])] = self.rows[i]
                            else:
                                for i in range(len(self.rows)):
                                    if self.rows[i][column] > value:
                                        rows_to_return[rows_to_return.index([])] = self.rows[i]
                        case "<":
                            column = self.column_names.index(condition[0])
                            value = int(condition[1])
                            if self.indexing:
                                if self.indexing[column]:
                                    rows_to_return = copy.deepcopy(self.indexing[column].less_than(value))
                                else:
                                    for i in range(len(self.rows)):
                                        if self.rows[i][column] < value:
                                            rows_to_return[rows_to_return.index([])] = self.rows[i]
                            else:
                                for i in range(len(self.rows)):
                                    if self.rows[i][column] < value:
                                        rows_to_return[rows_to_return.index([])] = self.rows[i]
            else:
                return -3 # no such column
            if [] in rows_to_return:
                rows_to_return = rows_to_return[:rows_to_return.index([])]
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
                    match function.upper():
                        case "COUNT":
                            rows_for_search = [i[:delimiter] for i in rows_to_return]
                            for row in raw_rows:
                                grouped_row = [row[i] for i in group_by_columns]
                                if len(rows_to_return[rows_for_search.index(grouped_row)]) < len(group_by_columns_names):
                                    rows_to_return[rows_to_return.index(grouped_row)].append(1)
                                else:
                                    rows_to_return[rows_for_search.index(grouped_row)][-1] += 1
                        case "MAX":
                            rows_for_search = [i[:delimiter] for i in rows_to_return]
                            for row in raw_rows:
                                grouped_row = [row[i] for i in group_by_columns]
                                if len(rows_to_return[rows_for_search.index(grouped_row)]) < len(group_by_columns_names):
                                    rows_to_return[rows_for_search.index(grouped_row)].append(row[column])
                                else:
                                    rows_to_return[rows_for_search.index(grouped_row)][-1] = max(row[column], rows_to_return[rows_for_search.index(grouped_row)][-1])
                        case "AVG":
                            rows_for_search = [i[:delimiter] for i in rows_to_return]
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

