


with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            _, created = Teacher.objects.get_or_create(
                first_name=row[0],
                last_name=row[1],
                middle_name=row[2],
                )
            # creates a tuple of the new object or
            # current object and a boolean of if it was created