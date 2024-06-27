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
        cur = conn.execute(f'SELECT type, full_text, source FROM feats where name = "{name}"')
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
        cur = conn.execute(f'SELECT type, full_text, source FROM traits where name = "{name}"')
        return cur.fetchall()


def insert_spell_data(spell_data):
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        sql = f"INSERT OR REPLACE INTO spells (name, school, subschool, full_text) VALUES ('{spell_data['name']}', '{spell_data['school']}', '{spell_data['subschool']}', '{spell_data['full_text']}')"
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
    path = r'S:\Programs\Own Projects\Character Sheet\Character-sheet\_internal\_data_files\data_base.db'
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    # Query for non-unique combinations
    cursor.execute("""
        SELECT name, type, source, COUNT(*)
        FROM feats
        GROUP BY name, type
        HAVING COUNT(*) > 1
    """)

    # Print the non-unique combinations
    for row in cursor.fetchall():
        print(f"Name: {row[0]}, Type: {row[1]}, Source: {row[2]}, Count: {row[3]}")

    conn.close()


# print_non_unique_combinations()


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
