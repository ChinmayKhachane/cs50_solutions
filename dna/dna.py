import csv
import sys


def main():

    if len(sys.argv) != 3:
        print("Incorrect usage of argument")
        sys.exit(1)

    data_file = open(sys.argv[1])
    dna_file = open(sys.argv[2])
    dna = dna_file.read()
    dna_file.close()
    data = csv.DictReader(data_file)

    str = data.fieldnames[1:]

    count = {}
    for i in str:
        count[i] = longest_match(dna, i)

    for row in data:
        if all(count[i] == int(row[i]) for i in count):
            print(row["name"])
            return
    print("No match")
    data_file.close()

def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run



main()
