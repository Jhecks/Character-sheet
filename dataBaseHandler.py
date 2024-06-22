import os
import sqlite3
import time

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
        cur = conn.execute(f"SELECT school, subschool, full_text FROM spells where name = '{name}'")
        return cur.fetchone()


def get_all_names_of_spells():
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        names = [name[0] for name in conn.execute("SELECT name FROM spells")]
        return names


def get_all_schools_of_spells():
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        schools = [job[0] for job in conn.execute("SELECT DISTINCT school FROM spells")]
        return schools


def get_all_subschools_of_spells():
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        subschools = [job[0] for job in conn.execute("SELECT DISTINCT subschool FROM spells")]
        return subschools


def get_all_names_of_feats():
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        names = [name[0] for name in conn.execute("SELECT name FROM feats")]
        return names


def get_all_types_of_feats():
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        types = [job[0] for job in conn.execute("SELECT DISTINCT type FROM feats")]
        return types


def get_data_from_db_by_feat_name(name):
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        cur = conn.execute(f"SELECT type, full_text FROM feats where name = '{name}'")
        return cur.fetchone()


def get_all_names_of_traits():
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        names = [name[0] for name in conn.execute("SELECT name FROM traits")]
        return names


def get_all_types_of_traits():
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        types = [job[0] for job in conn.execute("SELECT DISTINCT type FROM traits")]
        return types


def get_data_from_db_by_trait_name(name):
    conn = sqlite3.connect(os.getcwd() + '\\_internal\\_data_files\\data_base.db')
    with conn:
        cur = conn.execute(f"SELECT type, full_text FROM traits where name = '{name}'")
        return cur.fetchone()


start_time = time.time()
print(get_all_names_of_spells())
print(get_all_schools_of_spells())
print(get_all_subschools_of_spells())
print(get_data_from_db_by_spell_name('Skim'))
print()
print(get_all_names_of_feats())
print(get_all_types_of_feats())
print(get_data_from_db_by_feat_name('Skill Focus'))
print()
print(get_all_names_of_traits())
print(get_all_types_of_traits())
print(get_data_from_db_by_trait_name('Adaptive Magic'))
print()
print("--- db get spell data ---", time.time() - start_time)
