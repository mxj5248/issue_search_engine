class WhereClause:
    @classmethod
    def build_query(cls, *args, **kwargs):
        raise NotImplementedError()


class Between(WhereClause):
    @classmethod
    def build_query(cls, column_name, left, right):
        return "`{}` BETWEEN {} AND {}".format(column_name, left, right)


class Greater_than_equal(WhereClause):
    @classmethod
    def build_query(cls, column_name, date):
        return column_name + ">='" + date + "'"

class Less_than_equal(WhereClause):
    @classmethod
    def build_query(cls, column_name, date):
        return column_name + "<='" + date + "'"
    
class In(WhereClause):
    @classmethod
    def build_query(cls, column_name, set_value):
        return column_name + " in " + str(set_value)
    
class Not_in(WhereClause):
    @classmethod
    def build_query(cls, column_name, set_value):
        return column_name + " not in " + str(set_value)
    
class Equal_str(WhereClause):
    @classmethod
    def build_query(cls, column_name, val):
        return column_name + " ='" + val +"'"

class Equal_num(WhereClause):
    @classmethod
    def build_query(cls, column_name, val):
        return column_name + " = " + str(val)

class Not_Equal_str(WhereClause):
    @classmethod
    def build_query(cls, column_name, val):
        return column_name + " !='" + val +"'"

class Not_Equal_num(WhereClause):
    @classmethod
    def build_query(cls, column_name, val):
        return column_name + " !=" + str(val)
    

def build_query(fields, tables, filters):
    query_select = """SELECT {}
    """
    
    query_field = """FROM {}
        {}
    """
    
    query_base = query_select.format(",".join("`{}`".format(field) for field in fields), "{}")
    query_from = query_field.format(",".join("`{}`".format(table) for table in tables), "{}")
    
    if filters:
        query = query_from.format(
            "WHERE "+ " AND ".join(
                filter_item["operator"].build_query(filter_item["column"], filter_item["value"])
                for filter_item in filters
            )
        )
    else:
        query = query_from.format("")

    
    return query_base + query 