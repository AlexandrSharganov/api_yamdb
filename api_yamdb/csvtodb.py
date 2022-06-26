import csv
import sqlite3
from pathlib import Path
import datetime


path_to_db = Path('db.sqlite3')
conn = sqlite3.connect(path_to_db)
cur = conn.cursor()


path_to_data = Path('static', 'data', 'category.csv')
with open(
    path_to_data,
    'r',
    encoding='UTF-8'
) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = next(csv_reader)
    for row in csv_reader:
        cur.execute(
            "INSERT INTO reviews_categories(name,slug) VALUES (?,?)",
            (
                str(row[1]),
                str(row[2]),
            )
        )
    conn.commit()

path_to_data = Path('static', 'data', 'comments.csv')
with open(
    path_to_data,
    'r',
    encoding='UTF-8'
) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = next(csv_reader)
    for row in csv_reader:
        cur.execute(
            """INSERT INTO reviews_comment(review_id,text,author_id,pub_date)
            VALUES (?,?,?,?)""",
            (
                str(row[1]),
                str(row[2]),
                str(row[3]),
                str(row[4]),
            )
        )
    conn.commit()

path_to_data = Path('static', 'data', 'genre_title.csv')
with open(
    path_to_data,
    'r',
    encoding='UTF-8'
) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = next(csv_reader)
    for row in csv_reader:
        cur.execute(
            "INSERT INTO reviews_genretitle(title_id,genre_id) VALUES (?,?)",
            (
                int(row[1]),
                int(row[2]),

            )
        )
    conn.commit()

path_to_data = Path('static', 'data', 'genre.csv')
with open(
    path_to_data,
    'r',
    encoding='UTF-8'
) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = next(csv_reader)
    for row in csv_reader:
        cur.execute(
            "INSERT INTO reviews_genres(name,slug) VALUES (?,?)",
            (
                str(row[1]),
                str(row[2]),

            )
        )
    conn.commit()

path_to_data = Path('static', 'data', 'review.csv')
with open(
    path_to_data,
    'r',
    encoding='UTF-8'
) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = next(csv_reader)
    for row in csv_reader:
        cur.execute(
            """INSERT INTO reviews_review(title_id,text,author_id,score,pub_date)
            VALUES (?,?,?,?,?)""",
            (
                int(row[1]),
                str(row[2]),
                int(row[3]),
                int(row[4]),
                str(row[5]),
            )
        )
    conn.commit()

path_to_data = Path('static', 'data', 'titles.csv')
with open(
    path_to_data,
    'r',
    encoding='UTF-8'
) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = next(csv_reader)
    for row in csv_reader:
        cur.execute(
            "INSERT INTO reviews_title(name,year,category_id) VALUES (?,?,?)",
            (
                str(row[1]),
                int(row[2]),
                int(row[3]),
            )
        )
    conn.commit()

path_to_data = Path('static', 'data', 'users.csv')
current_date = datetime.datetime.now()
date_data = current_date.strftime('%m/%d/%Y')
with open(
    path_to_data,
    'r',
    encoding='UTF-8'
) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = next(csv_reader)
    for row in csv_reader:
        cur.execute(
            """INSERT INTO
            reviews_user(id,username,password,is_superuser,is_staff,is_active,date_joined,confirmation_code,
            email,role,bio,first_name,last_name)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                int(row[0]),
                str(row[1]),
                str('anonym'),
                str('False'),
                str('False'),
                str('False'),
                date_data,
                str('Empty'),
                str(row[2]),
                str(row[3]),
                str(row[4]),
                str(row[5]),
                str(row[6]),
            )
        )
    conn.commit()
