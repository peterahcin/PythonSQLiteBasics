from resources.connection_details import USER, PSWD, HOST, ENVIRODUAL_DATA_BASE
import psycopg2
from contextlib import closing


def create_connection(user, password, host, database):
    """
    creates connection to specified database
    :param user:
    :param password:
    :param host:
    :param database:
    :return:
    """
    conn = None
    try:
        conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            database=database
        )
        print(conn.get_dsn_parameters(), '\n')
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    return conn


def main():
    conn = create_connection(USER, PSWD, HOST, database=ENVIRODUAL_DATA_BASE)
    with closing(conn.cursor()) as cursor:

        # Update ALL_CARRIERS entries with croation name for district heating with slovenian values
        org_term = "sekanci; naravni les', 'elko; daljinjska toplota"
        new_term = "sekanci; naravni les', 'elko; daljinska toplota"

        cursor.execute(f'UPDATE podatki_envirodual.poraba_energentov SET "ALL_CARRIERS"=%s '
                       f'WHERE "ALL_CARRIERS"=%s', (new_term, org_term))

        print(f'Number of changed entries: ', cursor.rownumber)


if __name__ == '__main__':
    main()
