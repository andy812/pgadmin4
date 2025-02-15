##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2019, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

"""
    Check if the result-set of a query is updatable, A resultset is
    updatable (as of this version) if:
        - All columns belong to the same table.
        - All the primary key columns of the table are present in the resultset
        - No duplicate columns
"""
from flask import render_template
from flask_babelex import gettext
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


def is_query_resultset_updatable(conn, sql_path):
    """
        This function is used to check whether the last successful query
        produced updatable results.

        Args:
            conn: Connection object.
            sql_path: the path to the sql templates.
    """
    columns_info = conn.get_column_info()

    if columns_info is None or len(columns_info) < 1:
        return return_not_updatable()

    table_oid = _check_single_table(columns_info)
    if not table_oid:
        return return_not_updatable()

    if not _check_duplicate_columns(columns_info):
        return return_not_updatable()

    if conn.connected():
        primary_keys, pk_names = _check_primary_keys(conn=conn,
                                                     columns_info=columns_info,
                                                     table_oid=table_oid,
                                                     sql_path=sql_path)

        has_oids = _check_oids(conn=conn,
                               columns_info=columns_info,
                               table_oid=table_oid,
                               sql_path=sql_path)

        if has_oids or primary_keys is not None:
            return True, has_oids, primary_keys, pk_names, table_oid
        else:
            return return_not_updatable()
    else:
        raise Exception(
            gettext('Not connected to server or connection with the '
                    'server has been closed.')
        )


def _check_single_table(columns_info):
    table_oid = columns_info[0]['table_oid']
    for column in columns_info:
        if column['table_oid'] != table_oid:
            return None
    return table_oid


def _check_duplicate_columns(columns_info):
    column_numbers = \
        [col['table_column'] for col in columns_info]
    is_duplicate_columns = len(column_numbers) != len(set(column_numbers))
    if is_duplicate_columns:
        return False
    return True


def _check_oids(conn, sql_path, table_oid, columns_info):
    # Remove the special behavior of OID columns from
    # PostgreSQL 12 onwards, so returning False.
    if conn.manager.sversion >= 120000:
        return False

    # Check that the table has oids
    query = render_template(
        "/".join([sql_path, 'has_oids.sql']), obj_id=table_oid)

    status, has_oids = conn.execute_scalar(query)
    if not status:
        raise Exception(has_oids)

    # Check that the oid column is selected in results columns
    oid_column_selected = False
    for col in columns_info:
        if col['table_column'] is None and col['display_name'] == 'oid':
            oid_column_selected = True
            break
    return has_oids and oid_column_selected


def _check_primary_keys(conn, columns_info, sql_path, table_oid):
    primary_keys, primary_keys_columns, pk_names = \
        _get_primary_keys(conn=conn,
                          table_oid=table_oid,
                          sql_path=sql_path)

    if not _check_primary_keys_uniquely_exist(primary_keys_columns,
                                              columns_info):
        primary_keys = None
        pk_names = None
    return primary_keys, pk_names


def _check_primary_keys_uniquely_exist(primary_keys_columns, columns_info):
    for pk in primary_keys_columns:
        pk_exists = False
        for col in columns_info:
            if col['table_column'] == pk['column_number']:
                pk_exists = True
                # If the primary key column is renamed
                if col['display_name'] != pk['name']:
                    return False
            # If a normal column is renamed to a primary key column name
            elif col['display_name'] == pk['name']:
                return False

        if not pk_exists:
            return False
    return True


def _get_primary_keys(sql_path, table_oid, conn):
    query = render_template(
        "/".join([sql_path, 'primary_keys.sql']),
        obj_id=table_oid
    )
    status, result = conn.execute_dict(query)
    if not status:
        raise Exception(result)

    primary_keys_columns = []
    primary_keys = OrderedDict()
    pk_names = []

    for row in result['rows']:
        primary_keys[row['attname']] = row['typname']
        primary_keys_columns.append({
            'name': row['attname'],
            'column_number': row['attnum']
        })
        pk_names.append(row['attname'])

    return primary_keys, primary_keys_columns, pk_names


def return_not_updatable():
    return False, False, None, None, None
