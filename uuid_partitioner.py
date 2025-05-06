"""
/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

UUID Partitioner

This script splits the range of UUIDs into equal partitions.

Parameters:
  -s, --splits:     Number of splits to create
  -t, --target:     Name of the table or index
  -y, --targettype: Either "index" or "table"

Usage Examples:
  # Basic usage with 3 splits for a table named 'Users'
  python uuid_partitioner.py -s 3 -t Users -y table
  
  # Create 5 splits for an index named 'UserIndex'
  python uuid_partitioner.py -s 5 -t UserIndex -y index
"""

import uuid
import sys
import argparse
from typing import List


class UUIDPartitioner:
    def __init__(self):
        self.min_uuid = uuid.UUID('00000000-0000-0000-0000-000000000000')
        self.max_uuid = uuid.UUID('ffffffff-ffff-ffff-ffff-ffffffffffff')

    def get_ranges(self, num_partitions: int) -> List[uuid.UUID]:
        if num_partitions <= 0:
            raise ValueError("Number of partitions must be positive")

        # Calculate total range
        total_uuid_int_range = int(self.max_uuid) - int(self.min_uuid)
        
        # Generate partition boundaries
        boundaries = []
        for i in range(num_partitions):
            start_int = int(self.min_uuid) + (i * total_uuid_int_range // num_partitions)
            boundaries.append(uuid.UUID(int=start_int))
            
        return boundaries


def parse_arguments():
    parser = argparse.ArgumentParser(description="Partition UUID ranges")
    
    parser.add_argument("-s", "--splits", type=int, required=True,
                        help="Number of splits to create")
    parser.add_argument("-t", "--target", type=str, required=True,
                        help="Name of the table or index")
    parser.add_argument("-y", "--targettype", type=str, required=True, choices=["table", "index"],
                        help="Type of target (table or index)")
    
    return parser.parse_args()


def main():
    args = parse_arguments()
    
    partitioner = UUIDPartitioner()
    
    try:
        boundaries = partitioner.get_ranges(num_partitions=args.splits)
        
        # Display the output
        target_type = "TABLE" if args.targettype.upper() == "TABLE" else "INDEX"
        
        for boundary in boundaries:
            print(f"{target_type} {args.target} ('{boundary}')")
                
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()