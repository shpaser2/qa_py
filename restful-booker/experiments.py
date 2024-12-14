from faker import Faker

# Initialize Faker
fake = Faker()

# Generate two random dates
date1 = fake.date_between(start_date='-1y', end_date='now')  # A random date in the last year
date2 = fake.date_between(start_date='-1y', end_date='now')  # Another random date in the last year

# Print the generated dates
print("Date 1:", date1)
print("Date 2:", date2)

# Compare the two dates to find the earlier one
earlier_date = date1 if date1 < date2 else date2
later_date = date1 if date1 > date2 else date2

print("The earlier date is:", earlier_date)
print("The later date is:", later_date)
print(f"{fake.words(nb=3, unique=True)}")
print(f"{fake.boolean()}")
