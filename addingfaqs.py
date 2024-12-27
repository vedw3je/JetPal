import sqlite3

# Connect to the existing faqs.db
db_file_path = 'faqs.db'
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# List of new FAQs to add
faqs_to_add = [



]



# Insert new FAQs into the database
for question, answer in faqs_to_add:
    cursor.execute('''
        INSERT INTO faqs (question, answer)
        VALUES (?, ?)
    ''', (question, answer))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("New FAQs have been successfully added to the database!")
