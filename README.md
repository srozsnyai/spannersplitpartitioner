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
```

# End-to-End Example

**Spanner Example Table:**

The primary key "id" consists of UUIDs

```
CREATE TABLE payments_ledger (
  id STRING(255),
  from_account STRING(255),
  to_account STRING(255),
  amount INT64,
  created_on TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP()),
) PRIMARY KEY (id);
```
## Create UUID-based Splits 

**Create 10 UUID splits:**

```
python uuid_partitioner.py -s 10 -t payments_ledger -y table > splits.txt
```

**splits.txt should have this content:**
```
TABLE payments_ledger ('00000000-0000-0000-0000-000000000000')
TABLE payments_ledger ('19999999-9999-9999-9999-999999999999')
TABLE payments_ledger ('33333333-3333-3333-3333-333333333333')
TABLE payments_ledger ('4ccccccc-cccc-cccc-cccc-cccccccccccc')
TABLE payments_ledger ('66666666-6666-6666-6666-666666666666')
TABLE payments_ledger ('7fffffff-ffff-ffff-ffff-ffffffffffff')
TABLE payments_ledger ('99999999-9999-9999-9999-999999999999')
TABLE payments_ledger ('b3333333-3333-3333-3333-333333333332')
TABLE payments_ledger ('cccccccc-cccc-cccc-cccc-cccccccccccc')
TABLE payments_ledger ('e6666666-6666-6666-6666-666666666665')
```

**Submit Split points to Spanner:**
```
gcloud spanner databases splits add DATABASE_ID \
--splits-file=splits.txt \
--instance=INSTANCE_ID \
--split-expiration-date='2025-05-07T10:00:00Z'
```
**Check if split points are active:**
```
gcloud spanner databases splits list DATABASE_ID \
  --instance INSTANCE_ID
```

**Output should look like this:**
```
TABLE_NAME       INDEX_NAME  INITIATOR               SPLIT_KEY                                              EXPIRE_TIME
payments_ledger              CloudAddSplitPointsAPI  payments_ledger(00000000-0000-0000-0000-000000000000)  2025-05-07T10:00:00Z
payments_ledger              CloudAddSplitPointsAPI  payments_ledger(19999999-9999-9999-9999-999999999999)  2025-05-07T10:00:00Z
payments_ledger              CloudAddSplitPointsAPI  payments_ledger(33333333-3333-3333-3333-333333333333)  2025-05-07T10:00:00Z
payments_ledger              CloudAddSplitPointsAPI  payments_ledger(4ccccccc-cccc-cccc-cccc-cccccccccccc)  2025-05-07T10:00:00Z
payments_ledger              CloudAddSplitPointsAPI  payments_ledger(66666666-6666-6666-6666-666666666666)  2025-05-07T10:00:00Z
payments_ledger              CloudAddSplitPointsAPI  payments_ledger(7fffffff-ffff-ffff-ffff-ffffffffffff)  2025-05-07T10:00:00Z
payments_ledger              CloudAddSplitPointsAPI  payments_ledger(99999999-9999-9999-9999-999999999999)  2025-05-07T10:00:00Z
payments_ledger              CloudAddSplitPointsAPI  payments_ledger(b3333333-3333-3333-3333-333333333332)  2025-05-07T10:00:00Z
payments_ledger              CloudAddSplitPointsAPI  payments_ledger(cccccccc-cccc-cccc-cccc-cccccccccccc)  2025-05-07T10:00:00Z
payments_ledger              CloudAddSplitPointsAPI  payments_ledger(e6666666-6666-6666-6666-666666666665)  2025-05-07T10:00:00Z
```

## Remove custom split points

**Adding a timestamp in the past (Year 2000)**
```
gcloud spanner databases splits add DATABASE_ID \
--splits-file=splits.txt \
--instance=INSTANCE_ID \
--split-expiration-date='2000-05-07T10:00:00Z'
```

**Check if the split points are empty**
```
gcloud spanner databases splits list DATABASE_ID \
  --instance INSTANCE_ID
```

**Output should look like this:**
```
Listed 0 items.
```