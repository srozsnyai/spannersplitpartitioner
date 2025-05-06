# Spanner Pre-Splitting Partitioning Utils

## UUID Partitioner

This script splits the range of UUIDs into equal partitions.

**Parameters:**
```
  -s, --splits:     Number of splits to create
  -t, --target:     Name of the table or index
  -y, --targettype: Either "index" or "table"
```


**Usage Examples:**
```
  # Basic usage with 3 splits for a table named 'Users'
  python uuid_partitioner.py -s 3 -t Users -y table
  
  # Create 5 splits for an index named 'UserIndex'
  python uuid_partitioner.py -s 5 -t UserIndex -y index
```

## Nano ID Partitioner

This script splits the range of Nano IDs into equal partitions

**Parameters:**
```
  -s, --splits:     Number of splits to create
  -t, --target:     Name of the table or index
  -y, --targettype: Either "index" or "table"
  -l, --length:     Length of the Nano ID (default: 21)
  -a, --alphabet:   Type of alphabet to use (standard, no_underscore, alphanumeric, 
                    numbers, lowercase, uppercase) or custom alphabet string
```

**Usage Examples:**
```
  # Basic usage with 3 splits for a table named 'Users'
  python nanoid_partitioner.py -s 3 -t Users -y table

  # Create 5 splits for an index named 'UserIndex'
  python nanoid_partitioner.py -s 5 -t UserIndex -y index
  
  # Specify a custom Nano ID length of 10 characters
  python nanoid_partitioner.py -s 3 -t Users -y table -l 10
  
  # Use alphanumeric alphabet only (a-z, A-Z, 0-9)
  python nanoid_partitioner.py -s 3 -t Users -y table -a alphanumeric
  
  # Use numbers-only alphabet (0-9)
  python nanoid_partitioner.py -s 3 -t Products -y table -a numbers
  
  # Define a custom alphabet
  python nanoid_partitioner.py -s 3 -t SpecialData -y index -a "ABC123"

