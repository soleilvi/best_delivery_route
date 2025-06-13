import csv
from package import Package

def load_data(file_path):
    packages = []
    # new_package = Package()

    with open(file_path, 'r') as file:
        data = csv.reader(file, delimiter=',')

        # Skip the next 11 lines of the CSV file
        for num in range(8):
            next(data) 

        for row in data:
            # new_package = Package()
            # if row[0] == '0':
            #     if new_package.package_id != 0:
            #         packages.append(new_package)
            #     new_package = Package()
            new_package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            packages.append(new_package)
    return packages

packages = load_data('./data/package_data.csv')
for package in packages:
    print(f"Package ID: {package.id}, Address: {package.address}, City: {package.city}, State: {package.state}, Zip: {package.zip}, Deadline: {package.deadline}, Weight: {package.weight}, Dependencies: {package.dependencies}")