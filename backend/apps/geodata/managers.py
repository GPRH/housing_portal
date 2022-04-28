from rest_framework_mvt.managers import MVTManager
from django.core.exceptions import FieldError
from rest_framework.serializers import ValidationError


class GPRHMVTManager(MVTManager):

    def _build_query(self, filters={}):
        """
        Args:
            filters (dict): keys represent column names and
            values represent column values to filter on.
        Returns:
            tuple:
            A tuple of length two.  The first element is a string representing a
            parameterized SQL query.  The second element is a list
            of parameters used as inputs to the query's WHERE clause.
        """
        table = self.model._meta.db_table.replace('"', "")
        select_statement = self._create_select_statement()
        parameterized_where_clause, where_clause_parameters = (
            self._create_where_clause_with_params(
                table, filters,
            )
        )
        query = f"""
            SELECT ST_AsMVT(q, 'default', 4096, 'mvt_geom', 'id')
            FROM (SELECT {select_statement}
                ST_AsMVTGeom(
                    ST_Transform({table}.{self.geo_col}, 3857),
                    ST_Transform(ST_SetSRID(ST_GeomFromText(%s), 4326), 3857),
                    4096, 256, true
                ) AS mvt_geom
            FROM {table}
            WHERE {parameterized_where_clause}
            LIMIT %s
            OFFSET %s) AS q;
        """
        return (query.strip(), where_clause_parameters)

    def _create_where_clause_with_params(self, table, filters):
        """
        Args:
            table (str): A string representing the name of the table to query on.
            filters (dict): keys represent column names and values represent column
                            values to filter on.
        Returns:
            tuple:
            A tuple of length two.  The first element is a string representing a
            parameterized SQL query WHERE clause.  The second element is a list
            of parameters used as inputs to the WHERE clause.
        """
        try:
            sql, params = self.filter(**filters).query.sql_with_params()
        except FieldError as error:
            raise ValidationError(str(error))
        extra_wheres = " AND " + \
            sql.split("WHERE")[1].strip() if params else ""
        where_clause = (
            f"ST_Intersects({table}.{self.geo_col}, "
            f"ST_SetSRID(ST_GeomFromText(%s), 4326)){extra_wheres}"
        )
        return where_clause, list(params)
