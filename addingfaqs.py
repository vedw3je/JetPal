import sqlite3

# Connect to the existing faqs.db
db_file_path = 'faqs.db'
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# List of new FAQs to add
faqs_to_add = [
    # Indian Airlines
    ("How is Air India?",
     "Air India is India's flag carrier, known for its extensive domestic and international network, offering premium services and in-flight entertainment."),
    ("How is IndiGo?",
     "IndiGo is India's largest airline by market share, known for its punctuality, budget-friendly fares, and strong domestic network."),
    ("How is Vistara?",
     "Vistara is a premium full-service airline in India, offering excellent service, comfortable seating, and business-class options."),
    ("How is AirAsia India?",
     "AirAsia India is a low-cost carrier known for its competitive pricing, decent service, and growing domestic network."),
    ("How is Akasa Air?",
     "Akasa Air is India's newest budget airline, offering modern aircraft, comfortable seating, and competitive fares."),
    ("How is SpiceJet?",
     "SpiceJet is a budget airline in India, known for its affordable fares, decent service, and a mix of domestic and international routes."),
    ("How is Go First?",
     "Go First (formerly GoAir) is a budget airline with affordable fares and decent connectivity, though it has faced operational challenges."),
    ("How is Alliance Air?",
     "Alliance Air is a regional airline in India, serving smaller cities and remote destinations under the UDAN scheme."),

    # Major International Airlines
    ("How is Emirates?",
     "Emirates is one of the world's leading airlines, known for its luxurious cabins, excellent service, and extensive global network."),
    ("How is Qatar Airways?",
     "Qatar Airways is a top-rated airline offering premium services, comfortable seating, and one of the best business-class experiences."),
    ("How is Singapore Airlines?",
     "Singapore Airlines is consistently ranked among the world's best airlines, offering outstanding service, comfort, and in-flight amenities."),
    ("How is British Airways?",
     "British Airways is the UK’s flag carrier, known for its premium economy and business class services."),
    ("How is Lufthansa?",
     "Lufthansa is Germany’s largest airline, providing excellent service, modern aircraft, and extensive connectivity across Europe and beyond."),
    ("How is Etihad Airways?",
     "Etihad Airways is known for its luxury offerings, including The Residence and high-quality in-flight services."),
    ("How is Thai Airways?",
     "Thai Airways is Thailand’s national carrier, providing good service, spacious seats, and great hospitality."),
    ("How is Japan Airlines?",
     "Japan Airlines is known for its exceptional service, punctuality, and high-quality in-flight meals."),
    ("How is Turkish Airlines?",
     "Turkish Airlines has an extensive network and is praised for its service, in-flight entertainment, and comfortable seating."),
    ("How is Delta Airlines?",
     "Delta Airlines is a major US airline, known for its reliability, frequent flyer program, and solid customer service."),
    ("How is American Airlines?",
     "American Airlines is one of the largest airlines in the world, offering a vast network and decent service."),
    ("How is United Airlines?",
     "United Airlines is known for its extensive route network, especially in North America, and offers good premium services."),
    ("How is Cathay Pacific?",
     "Cathay Pacific is Hong Kong’s flagship airline, known for its excellent service and business-class experience."),
    ("How is Malaysia Airlines?",
     "Malaysia Airlines provides good service and comfortable flights, though it has faced operational challenges."),
    ("How is Korean Air?", "Korean Air is a top-rated Asian airline, known for its great in-flight meals and service."),
    ("How is Qantas?",
     "Qantas is Australia’s flagship airline, offering long-haul flights with excellent service and safety records."),
    ("How is Air France?",
     "Air France is a leading European airline, known for its elegant service, good food, and extensive global reach."),
    ("How is KLM Royal Dutch Airlines?",
     "KLM is the Netherlands’ national airline, providing good service, comfortable seats, and a strong European network."),
    ("How is Swiss International Air Lines?",
     "Swiss International Air Lines is known for its premium services, high-quality food, and comfortable cabins."),
    ("How is Aeroflot?",
     "Aeroflot is Russia’s national airline, known for its improved service and extensive international routes."),
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
