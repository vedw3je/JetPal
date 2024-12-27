import sqlite3

# Connect to your database
conn = sqlite3.connect('faqs.db')
cursor = conn.cursor()

# Example: Delete FAQ based on the question
faq_to_delete = "What’s your name?"

# Execute the DELETE SQL statement
cursor.execute("DELETE FROM faqs WHERE question = ?", (faq_to_delete,))

# Commit the changes
conn.commit()

# Check if the row was deleted successfully
if cursor.rowcount > 0:
    print("FAQ deleted successfully.")
else:
    print("FAQ not found.")

# Close the connection
conn.close()
