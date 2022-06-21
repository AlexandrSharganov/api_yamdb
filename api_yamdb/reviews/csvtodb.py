import csv
import sqlite3


conn = sqlite3.connect(r'D:\Dev\api_yamdb\api_yamdb\db.sqlite3')
cur = conn.cursor()
with open(r"D:\Dev\api_yamdb\api_yamdb\static\data\genre_title.csv", 'r', encoding='UTF-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = next(csv_reader)
    for row in csv_reader:
        cur.execute("INSERT INTO reviews_genretitle(title_id,genre_id) VALUES (?,?)", (
            int(row[1]),
            int(row[2]),
        )
    )
    conn.commit()