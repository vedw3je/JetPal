import sqlite3

# Connect to the existing faqs.db
db_file_path = 'faqs.db'
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# List of new FAQs to add
faqs_to_add = [
    ("Good work, Jetpal!", "Thank you! I'm glad you find my assistance helpful. I'm always here to help you with anything you need."),
    ("I'm very happy with Jetpal's service!", "Thank you for the kind words! It makes me happy to know that you're satisfied with my help."),
    ("Great job, Jetpal! Keep it up!", "Thank you! I'll keep working hard to provide the best assistance I can. Let me know if there's anything else I can help with."),
    ("Jetpal, you're doing amazing!", "Thank you! I'm thrilled to hear that you think so. Your satisfaction is my top priority."),
    ("I love Jetpal! The service is fantastic!", "Thank you for the compliment! I'm always here to provide the best service to make your experience seamless."),
    ("Jetpal, you're the best chatbot!", "Thank you! I'm happy to be of service. Let me know if you have any more questions or need assistance."),
    ("I always enjoy interacting with Jetpal. Great job!", "Thank you! I'm glad you enjoy our interactions. I'm here whenever you need me."),
    ("Jetpal is truly amazing, great service!", "Thank you! I strive to provide helpful and accurate information. Your feedback means a lot to me."),
    ("I had an excellent experience with Jetpal!", "Thank you for sharing your experience! I'm happy to know I was able to assist you effectively."),
    ("Thank you, Jetpal, for being so helpful!", "You're very welcome! I'm glad I could help. Feel free to reach out anytime you need assistance.")
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
