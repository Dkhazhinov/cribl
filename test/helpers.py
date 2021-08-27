import os
import re


def combine_files(file_one: str, file_two: str):
    """
    Method will combine two files by reading them line by line which helps with memory allocation - we don't load both
    files into memory only 1 line at the time.
    :param file_one: string representing path to first file
    :param file_two: string representing path to second file
    :return: Method returns path to file that is created by combining two files from arguments
    """
    combined_file_name = "combined_events.log"
    combined_file_path = f"{os.getcwd()}/outputs/{combined_file_name}"

    with open(file_one, 'r') as first_file, open(file_two, 'r') as second_file, open(combined_file_path, 'w') as output:
        # load 1 line from the file and write it to combined file
        for line in first_file:
            output.write(line)
        for line in second_file:
            output.write(line)

    # return path to newly added file that contains combined data
    return combined_file_path


def sort_file(file_to_sort: str):
    """
    Method will sort data inside of the file and will write sorted data to the same file
    :param file_to_sort: string representing path to file that needs to be sorted
    :return: N/A
    memory that is allocated to store data in temp_list doesn't need to be released. Python cleans up after te method
    is node and all local variables removed
    """
    temp_list = []
    with open(file_to_sort, "r") as to_sort:
        for line in to_sort:
            # extract numerical value from the string so we can sort using it
            number = int(re.search(r"\d+", line).group())
            # append a tuple that contains original line from the file and extracted int
            temp_list.append((line, number))

    # sort temp list by second (int) value inside of a tuple
    temp_list = sorted(temp_list, key=lambda s: s[1])

    # write sorted data back to a file
    with open(file_to_sort, "w") as to_write:
        for element in temp_list:
            # only writes original string from the unsorted file
            to_write.write(element[0])


def get_file_name_from_string(line: str, file_path: str):
    """
    :param line: String from log file that needs to be matched to a file name
    :param file_path: String to contains path to a file
    :return: Returns True if line was found in a file and False if line wasn't found
    """
    with open(file_path, 'r') as file:
        for file_line in file:
            if line == file_line:
                return True
    return False

