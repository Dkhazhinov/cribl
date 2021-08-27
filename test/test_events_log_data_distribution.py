import pytest
from helpers import *
from itertools import zip_longest


class TestLogDistribution:

    @pytest.mark.parametrize("file_name", [
        "events_target_1.log",
        "events_target_2.log"
    ])
    def test_verify_file_exist(self, file_name: str):
        """
        Test verifies that output event log file exist after input data was split
        :param file_name: string that contains name of the events log file
        """
        file_path = f"{os.getcwd()}/outputs"

        # verify that file exists
        assert os.path.isfile(f"{file_path}/{file_name}"), (
            f"File {file_name} is not found"
        )

    @pytest.mark.parametrize("file_names", [
        {
            "input": "large_1M_events.log",
            "target_1": "events_target_1.log",
            "target_2": "events_target_2.log"
        }
    ])
    def test_verify_output_files_size_match_input_file(self, file_names: dict):
        """
        Test verifies that size of two combined events log files matches size of input log file.
        :param file_names: dict with file names
        """
        # Get file size in bytes
        main_file = os.stat(f"{os.getcwd()}/agent/inputs/{file_names.get('input')}").st_size
        events_one = os.stat(f"{os.getcwd()}/outputs/{file_names.get('target_1')}").st_size
        events_two = os.stat(f"{os.getcwd()}/outputs/{file_names.get('target_2')}").st_size

        # Verify that input log file size matches size of combined output log files
        combined_size = sum([events_one, events_two])
        assert main_file == combined_size, (
            f"Input file size doesn't match combined output files size"
            f"\nExpected input file size: {main_file} bytes"
            f"\nActual combined file size: {combined_size} bytes"
            f"\nWhere file size in bytes for target_1: {events_one} and target_2: {events_two}"
            f"\nTest input data:\n{file_names}"
        )

    @pytest.mark.parametrize("file_names", [
        {
            "input": "large_1M_events.log",
            "target_1": "events_target_1.log",
            "target_2": "events_target_2.log"
        }
    ])
    def test_verify_combined_number_lines_match_input(self, file_names: dict):
        """
        Test verifies that total combined count of lines in both output event log files matches number
        of lines in the input log file
        :param file_names: dict with file names
        """
        # Path to input log file and output events log files
        input_path = f"{os.getcwd()}/agent/inputs/{file_names.get('input')}"
        events_one_path = f"{os.getcwd()}/outputs/{file_names.get('target_1')}"
        events_two_path = f"{os.getcwd()}/outputs/{file_names.get('target_2')}"

        # Open log files in 'read' mode (opened files would be automatically closed after the test)
        with open(input_path, "r") as input_file, open(events_one_path, "r") as events_one, open(events_two_path, "r") as events_two:
            input_lines_count, events_one_count, events_two_count = 0, 0, 0
            # Iterate through all files line by line
            for line, line_one, line_two in zip_longest(input_file, events_one, events_two):
                # Increment counts when line from file exist
                if line:
                    input_lines_count += 1
                if line_one:
                    events_one_count += 1
                if line_two:
                    events_two_count += 1

        # Verify that number of lines matches
        sum_lines = sum([events_one_count, events_two_count])
        assert input_lines_count == sum_lines, (
            f"Number of lines in input file doesn't match combined number of lines"
            f"\nExpected number of lines: {input_lines_count}"
            f"\nActual number of lines: {sum_lines}"
            f"\nWhere number of lines for target_1 file: {events_one_count} and target_2 file: {events_two_count}"
            f"\nTest input data: {file_names}"
        )

    @pytest.mark.ddev
    @pytest.mark.parametrize("file_names", [
        {
            "input": "large_1M_events.log",
            "target_1": "events_target_1.log",
            "target_2": "events_target_2.log"
        }
    ])
    def test_verify_file_content_matches(self, file_names: dict):
        # Path to input log file and output events log files
        input_path = f"{os.getcwd()}/agent/inputs/{file_names.get('input')}"
        events_one_path = f"{os.getcwd()}/outputs/{file_names.get('target_1')}"
        events_two_path = f"{os.getcwd()}/outputs/{file_names.get('target_2')}"

        # combine two output log filed into one sorted file
        combined_file_path = combine_files(events_one_path, events_two_path)
        sort_file(combined_file_path)

        with open(input_path, 'r') as input_file, open(combined_file_path, 'r') as sorted_results:
            # read data from files
            input_list = input_file.readlines()
            out_list = sorted_results.readlines()

            # compare two sets with data from files
            set_difference = set(out_list) - set(input_list)
            corrupted_data = list(set_difference)

            # map line of data to a host
            # in case of any data was corrupted after splitter process
            if len(corrupted_data) != 0:
                mapped_to_file = []
                for element in corrupted_data:
                    # we need to match line of data with file that it came from
                    for file in [events_one_path, events_two_path]:
                        # call method that will return True if line matched the file
                        file_found = get_file_name_from_string(element, file)
                        if file_found:
                            # translate file name to host name
                            for file_name in file_names.keys():
                                if file_name in file:
                                    host_name = file_name
                            mapped_to_file.append((host_name, element))
                            # exit loop if file was identified
                            break

            # verify that data was split without loss
            assert len(corrupted_data) == 0, (
                f"Total of {len(corrupted_data)} event(s) were corrupter after data went through Splitter\n"
                f"\nFollowing list of pairs (receiving_host_name, log_line) were corrupted:\n"
                f"{mapped_to_file}\n"
            )

