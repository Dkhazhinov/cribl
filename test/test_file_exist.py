import os
import pytest

class TestFileExist:

    @pytest.mark.parametrize("file_name", [
        "events_target_1.log",
        "events_target_2.log"
    ])
    def test_verify_file_exist(self, file_name):
        assert os.path.isfile(f"{os.getcwd()}/outputs/{file_name}")