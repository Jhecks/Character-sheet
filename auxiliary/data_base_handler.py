import json
import os
import sqlite3
import codecs

import pandas as pd


def spells_csv_to_db():
    df = pd.read_csv(os.getcwd() + '\\_internal\\_data_files\\spells.csv')
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    df.to_sql('spells', conn, if_exists='replace', index=False)
    conn.close()


def feats_csv_to_db():
    df = pd.read_csv(os.getcwd() + '\\_internal\\_data_files\\feats.csv')
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    df.to_sql('feats', conn, if_exists='replace', index=False)
    conn.close()


def traits_csv_to_db():
    df = pd.read_csv(os.getcwd() + '\\_internal\\_data_files\\traits.csv')
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    df.to_sql('traits', conn, if_exists='replace', index=False)
    conn.close()


def get_data_from_db_by_spell_name(name):
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        cur = conn.execute(f'SELECT school, subschool, full_text FROM spells where name = "{name}"')
        return cur.fetchone()


def get_all_names_of_spells():
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        names = [name[0] for name in conn.execute("SELECT name FROM spells ORDER BY name")]
        return names


def get_all_schools_of_spells():
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        schools = [job[0] for job in conn.execute("SELECT DISTINCT school FROM spells ORDER BY school")]
        return schools


def get_all_subschools_of_spells():
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        subschools = [job[0] for job in conn.execute("SELECT DISTINCT subschool FROM spells ORDER BY subschool")]
        return subschools


def get_all_names_of_feats():
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        names = [name[0] for name in conn.execute("SELECT name FROM feats ORDER BY name")]
        return names


def get_all_sources_of_feats():
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        sources = [source[0] for source in conn.execute("SELECT DISTINCT source FROM feats ORDER BY source")]
        return sources


def get_all_types_of_feats():
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        types = [job[0] for job in conn.execute("SELECT DISTINCT type FROM feats ORDER BY type")]
        return types


def get_data_from_db_by_feat_name(name):
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        cur = conn.execute(f'SELECT name, type, full_text, source FROM feats where name = "{name}"')
        return cur.fetchall()


def get_all_names_of_traits():
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        names = [name[0] for name in conn.execute("SELECT name FROM traits ORDER BY name")]
        return names


def get_all_sources_of_traits():
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        sources = [source[0] for source in conn.execute("SELECT DISTINCT source FROM traits ORDER BY source")]
        return sources


def get_all_types_of_traits():
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        types = [job[0] for job in conn.execute("SELECT DISTINCT type FROM traits ORDER BY type")]
        return types


def get_data_from_db_by_trait_name(name):
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        cur = conn.execute(f'SELECT name, type, full_text, source FROM traits where name = "{name}"')
        return cur.fetchall()


def get_data_from_db_by_trait_name_source(name, source):
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        cur = conn.execute(f'SELECT type, full_text FROM traits where name = "{name}" and source = "{source}"')
        return cur.fetchone()


def get_data_from_db_by_trait_name_type(name, type):
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        cur = conn.execute(f'SELECT source, full_text FROM traits where name = "{name}" and type = "{type}"')
        return cur.fetchone()


def insert_spell_data(spell_data):
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        sql = f"INSERT OR REPLACE INTO spells (name, school, subschool, full_text) VALUES ('{spell_data['name']}', '{spell_data['school']}', '{spell_data['subschool']}', '{spell_data['full_text']}')"
        conn.execute(sql)
        conn.commit()


def delete_spell_data(name):
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        sql = f"DELETE FROM spells WHERE name = '{name}'"
        conn.execute(sql)
        conn.commit()


def insert_feat_data(feat_data):
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        sql = (f"INSERT INTO feats (name, type, source, full_text) VALUES ('{feat_data['name']}', "
               f"'{feat_data['type']}', '{feat_data['source']}', '{feat_data['full_text']}')")
        conn.execute(sql)
        conn.commit()


def insert_trait_data(trait_data):
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        sql = (f"INSERT INTO traits (name, type, source, full_text) VALUES ('{trait_data['name']}', "
               f"'{trait_data['type']}', '{trait_data['source']}', '{trait_data['full_text']}')")
        conn.execute(sql)
        conn.commit()


def save_character_sheet(name, data):
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    data = json.dumps(data).encode(encoding='utf-8')
    data = codecs.encode(data, "base64").decode()
    with conn:
        sql = f'INSERT OR REPLACE INTO character_sheets (name, data) VALUES ("{name}", "{data}")'
        conn.execute(sql)
        conn.commit()


def get_character_sheet_names():
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        names = [name[0] for name in conn.execute("SELECT name FROM character_sheets")]
        return names


def get_character_sheet(name):
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        cur = conn.execute(f'SELECT data FROM character_sheets where name = "{name}"')
        data = cur.fetchone()[0]
        print(data)
        data = codecs.decode(data.encode(), "base64")
        data = data.decode()
        # data = json.loads(data)
        return data


def copy_data_from_feats_temp_to_feats():
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    cursor = conn.cursor()

    # Copy data
    cursor.execute("""
        INSERT INTO traits (name, type, source, full_text, url)
        SELECT name, type, source, full_text, url FROM traits
    """)

    conn.commit()
    conn.close()


# copy_data_from_feats_temp_to_feats()


def print_non_unique_combinations():
    # path = r'D:\Programs\Own Projects\Character Sheet\Character-sheet\_internal\_data_files\data_base.db'
    path = r'S:\Programs\Own Projects\Character Sheet\Character-sheet\_internal\_data_files\data_base.db'
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    # Query for non-unique combinations
    cursor.execute("""
        SELECT name, type, source, COUNT(*)
        FROM traits
        GROUP BY name, type
        HAVING COUNT(*) > 1
    """)

    # Print the non-unique combinations
    for row in cursor.fetchall():
        print(f"Name: {row[0]}, Type: {row[1]}, Source: {row[2]}, Count: {row[3]}")

    conn.close()


# print_non_unique_combinations()


def print_non_unique_name_source_combinations():
    db_path = r'S:\Programs\Own Projects\Character Sheet\Character-sheet\_internal\_data_files\data_base.db'
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL query to find non-unique combinations of name and source
    query = """
    SELECT name, COUNT(*)
    FROM feats
    GROUP BY name
    HAVING COUNT(*) > 1
    """

    try:
        cursor.execute(query)
        combinations = cursor.fetchall()
        if combinations:
            for combination in combinations:
                # print(f"Name: {combination[0]}, Source: {combination[1]}, Count: {combination[2]}")
                print(f"Name: {combination[0]}, Type: {combination[1]}, Count: {combination[2]}")
                # print(f"Name: {combination[0]}, Count: {combination[1]}")
        else:
            print("No non-unique name and source combinations found.")
    finally:
        # Ensure the connection is closed even if an error occurs
        conn.close()


# print_non_unique_name_source_combinations()


def print_non_unique_names():
    path = r'D:\Programs\Own Projects\Character Sheet\Character-sheet\_internal\_data_files\data_base.db'
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    # Query for non-unique names
    cursor.execute("""
        SELECT name, type, source, COUNT(*)
        FROM traits
        GROUP BY name
        HAVING COUNT(*) > 1
    """)

    # Print the non-unique names
    for row in cursor.fetchall():
        print(f"Name: {row[0]}, Type: {row[1]}, Source: {row[2]}, Count: {row[3]}")

    conn.close()


# print_non_unique_names()


def print_non_unique_names_with_all_data():
    path = r'D:\Programs\Own Projects\Character Sheet\Character-sheet\_internal\_data_files\data_base.db'
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    # Query for non-unique names
    cursor.execute("""
        SELECT name, COUNT(*)
        FROM traits
        GROUP BY name
        HAVING COUNT(*) > 1
    """)

    # Fetch the non-unique names
    non_unique_names = [row[0] for row in cursor.fetchall()]

    # For each non-unique name, print all its data
    for name in non_unique_names:
        cursor.execute("""
            SELECT name, type, source
            FROM traits
            WHERE name = ?
        """, (name,))

        # Print all data for the current non-unique name
        for row in cursor.fetchall():
            print(f"Name: {row[0]}, Type: {row[1]}, Source: {row[2]}")

    conn.close()


# print_non_unique_names_with_all_data()


def create_feats_table():
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')  # replace with your actual database path
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
        CREATE TABLE traits (
            name TEXT,
            type TEXT,
            source TEXT,
            full_text TEXT,
            url TEXT,
            PRIMARY KEY (name, type, source)
        )
    """)

    conn.commit()
    conn.close()


# create_feats_table()

# print(get_all_names_of_spells())

def testing_serialisation():
    path = os.getcwd() + '\\_internal\\_data_files\\Kiko_Sato.json'
    with (open(path, 'r', encoding='utf-8') as input_file):
        data = json.load(input_file)
    # data = {'name': 'test', 'type': 'test', 'source': 'test', 'description': "te'st"}
    json_dump = json.dumps(data).encode(encoding='utf-8')
    serialised_data = codecs.encode(json_dump, "base64").decode()
    print(serialised_data)
    data_from_serialisation = codecs.decode(serialised_data.encode(), "base64")
    print(json.loads(data_from_serialisation))


# testing_serialisation()
