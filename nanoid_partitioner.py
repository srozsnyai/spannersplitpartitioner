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
 
Nano ID Partitioner

This script splits the range of Nano IDs into equal partitions

Parameters:
  -s, --splits:     Number of splits to create
  -t, --target:     Name of the table or index
  -y, --targettype: Either "index" or "table"
  -l, --length:     Length of the Nano ID (default: 21)
  -a, --alphabet:   Type of alphabet to use (standard, no_underscore, alphanumeric, 
                    numbers, lowercase, uppercase) or custom alphabet string

Usage Examples:
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
"""

import argparse
import string
import sys
from enum import Enum
from typing import List, Tuple


class AlphabetType(Enum):
    STANDARD = "standard"  # Default nanoid alphabet (with underscore)
    NO_UNDERSCORE = "no_underscore"  # Without underscore
    ALPHANUMERIC = "alphanumeric"  # Just letters and numbers
    NUMBERS = "numbers"  # Only numbers
    LOWERCASE = "lowercase"  # Lowercase letters only
    UPPERCASE = "uppercase"  # Uppercase letters only


class NanoidRangeSplitter:
    ALPHABETS = {
        AlphabetType.STANDARD: string.ascii_lowercase + string.ascii_uppercase + string.digits + '-_',
        AlphabetType.NO_UNDERSCORE: string.ascii_lowercase + string.ascii_uppercase + string.digits + '-',
        AlphabetType.ALPHANUMERIC: string.ascii_lowercase + string.ascii_uppercase + string.digits,
        AlphabetType.NUMBERS: string.digits,
        AlphabetType.LOWERCASE: string.ascii_lowercase,
        AlphabetType.UPPERCASE: string.ascii_uppercase
    }

    # Default Nano ID length
    DEFAULT_LENGTH = 21

    def __init__(self, alphabet_type: AlphabetType = AlphabetType.NO_UNDERSCORE, custom_alphabet: str = None):
        if custom_alphabet is not None:
            self.alphabet = ''.join(sorted(set(custom_alphabet)))  # Remove duplicates and sort
        else:
            self.alphabet = self.ALPHABETS[alphabet_type]

        self.alphabet_size = len(self.alphabet)

        if self.alphabet_size == 0:
            raise ValueError("Alphabet cannot be empty")

    def _to_base(self, num: int, length: int) -> str:
        if num < 0:
            raise ValueError("Number must be non-negative")

        result = []
        while num:
            num, rem = divmod(num, self.alphabet_size)
            result.append(self.alphabet[rem])
        
        result = result + [self.alphabet[0]] * (length - len(result))
        return ''.join(reversed(result))

    def get_ranges(self, num_partitions: int, id_length: int) -> List[str]:
        if num_partitions <= 0:
            raise ValueError("Number of partitions must be positive")
        if id_length <= 0:
            raise ValueError("ID length must be positive")
        
        # Calculate total possible combinations
        total_combinations = self.alphabet_size ** id_length

        if num_partitions > total_combinations:
            raise ValueError(
                f"Number of partitions ({num_partitions}) cannot exceed total possible combinations ({total_combinations})"
            )

        # Calculate size of each partition
        partition_size = total_combinations // num_partitions

        # Generate partition boundaries
        boundaries = []
        for i in range(num_partitions):
            # Calculate the starting point of this partition
            start = i * partition_size
            
            # Convert to Nano ID string
            id_str = self._to_base(start, id_length)
            
            boundaries.append(id_str)
            
        return boundaries


def parse_arguments():
    parser = argparse.ArgumentParser(description="Partition Nano ID ranges")
    
    parser.add_argument("-s", "--splits", type=int, required=True,
                        help="Number of splits to create")
    parser.add_argument("-t", "--target", type=str, required=True,
                        help="Name of the table or index")
    parser.add_argument("-y", "--targettype", type=str, required=True, choices=["table", "index"],
                        help="Type of target (table or index)")
    parser.add_argument("-l", "--length", type=int, default=NanoidRangeSplitter.DEFAULT_LENGTH,
                        help=f"Length of the Nano ID (default: {NanoidRangeSplitter.DEFAULT_LENGTH})")
    parser.add_argument("-a", "--alphabet", type=str, default="standard",
                        help="Alphabet type (standard, no_underscore, alphanumeric, numbers, lowercase, uppercase) or custom alphabet string")
    
    return parser.parse_args()


def main():
    args = parse_arguments()
    
    # Determine the alphabet type
    try:
        alphabet_type = AlphabetType(args.alphabet)
        custom_alphabet = None
    except ValueError:
        # If not a valid enum value, treat as custom alphabet
        alphabet_type = None
        custom_alphabet = args.alphabet
    
    # Create the splitter
    splitter = NanoidRangeSplitter(
        alphabet_type=alphabet_type,
        custom_alphabet=custom_alphabet
    )
    
    # Get the partition boundaries
    try:
        boundaries = splitter.get_ranges(
            num_partitions=args.splits,
            id_length=args.length
        )
        
        # Display the output
        target_type = "TABLE" if args.targettype.upper() == "TABLE" else "INDEX"
        
        for boundary in boundaries:
            print(f"{target_type} {args.target} ('{boundary}')")
                
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()