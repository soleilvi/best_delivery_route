import csv
from package import Package

hash_table = [None] * 35  # Set the size of the hash table to the average number of packages + 5

def load_data(file_path):
    packages = []

    with open(file_path, 'r') as file:
        data = csv.reader(file, delimiter=',')

        # Skip the next 11 lines of the CSV file
        for num in range(8):
            next(data) 

        for row in data:
            new_package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            packages.append(new_package)
    return packages

# keep in mind that the size of the list should be adjusted to the average number of packages if adjusting for another city
def load_hash(package_list, hash_list):
    for package in package_list:
        key = int(package.id)
        index = (key - 1) % len(hash_list)  # Division method for hashing
        
        # Initialize with the package if the bucket is empty
        if hash_list[index] is None:
            hash_list[index] = [package]

        # Collision handling (chaining)
        else:
            hash_list[index].append(package)


# Print packages data        
packages = load_data('./data/package_data.csv')

# Print hash
load_hash(packages, hash_table)
for i, bucket in enumerate(hash_table):
    if bucket is not None:
        if isinstance(bucket, list):
            for package in bucket:
                print(f"Hash Index: {i}, Package ID: {package.id}, Address: {package.address}, City: {package.city}, State: {package.state}, Zip: {package.zip}, Deadline: {package.deadline}, Weight: {package.weight}, Dependencies: {package.dependencies}")
        else:
            print(f"Hash Index: {i}, Package ID: {bucket.id}, Address: {bucket.address}, City: {bucket.city}, State: {bucket.state}, Zip: {bucket.zip}, Deadline: {bucket.deadline}, Weight: {bucket.weight}, Dependencies: {bucket.dependencies}")
    else:
        print(f"Hash Index: {i} is empty.")