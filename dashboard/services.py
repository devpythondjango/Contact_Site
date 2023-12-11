from django.db import connection
from contextlib import closing


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]


def dictfetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return False
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def get_app_create_all():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""
            SELECT * FROM contact_application 
            INNER JOIN contact_applicationcreate 
            ON contact_applicationcreate.application_id = contact_application.id
            INNER JOIN contact_hujumturi 
            ON contact_hujumturi.id = contact_application.hujumturi_id
            INNER JOIN contact_tuman
            ON contact_tuman.id = contact_application.district_id;
        """)
        application = dictfetchall(cursor)
        return application
