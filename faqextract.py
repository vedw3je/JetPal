import pandas as pd
import sqlite3

# Step 1: Load CSV file
csv_file_path = 'airlinefaqs.csv'
df = pd.read_csv(csv_file_path)

# Step 2: Extract only the required columns
faq_data = df[['faqQuestion', 'faqAnswer']]

# Step 3: Connect to SQLite database
db_file_path = 'faqs.db'
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# Step 4: Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS faqs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT
    )
''')

# Step 5: Insert FAQ data into the table
for index, row in faq_data.iterrows():
    if pd.notnull(row['faqQuestion']) and pd.notnull(row['faqAnswer']):
        cursor.execute('''
            INSERT INTO faqs (question, answer)
            VALUES (?, ?)
        ''', (row['faqQuestion'], row['faqAnswer']))

# Step 6: Commit changes and close the connection
conn.commit()
conn.close()

print(f"FAQs have been successfully imported into {db_file_path}")
conn = sqlite3.connect('faqs.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM faqs')
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
