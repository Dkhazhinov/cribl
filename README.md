# Cribl Take home project

author: Dmitry Khazhinov

Known Issues:
---
https://github.com/Dkhazhinov/cribl/issues

CI - GitHub workflow
---
The pipeline (workflow) contains two jobs: `deployment` and `testing`. CI workflow triggered on every **push** 
and **pull request**

`testing` job depends on successful completion of `deployment` job

Setup and teardown of the deployment automated inside the `deployment` job.

Manually running a workflow
---
1. On GitHub, navigate to the main page of the repository.
2. Under your repository name, click **Actions**
3. In the left sidebar, click the workflow you want to run - `Data Distribution` workflow
4. Above the list of workflow runs, select `Run workflow`.
5. Use the Branch dropdown to select the workflow's branch (`master`). 
6. Click `Run workflow`

Artifacts
---
Artifacts from both jobs would be uploaded to `Artifacts` section under `Summary` for CI workflow run with name:
`my-artifact`. You can download artifacts by clicking on `my-artifact` link.

Downloaded folder will have a name `my-artifact` and contain several artifacts depending on the stage of the workflow: 
- Upon completion of `deployment` job:
  - `events_target_1.log`
  - `events_target_2.log`
    
- Upon completion of `testing` job:
  - `test_report.html` - file with test results.

Test Report
---
Interactive test report html file can be opened in any browser. You can see **Environment** details, **Summary** of all 
tests and upu can filter by `passed`, `failed` and other test status.

Each `failed` test will contain details about the test -> you can see by clicking on `(show details)` link.

Under `details` section you can see the test body as well as the relevant `Assertion Error Message` that should provide 
you with enough information to be able to create a bug report.

#### Assertion Error Example

Test - `test/test_events_log_data_distribution.py::TestLogDistribution::test_verify_combined_number_lines_match_input`:
```commandline
E       AssertionError: Number of lines in input file doesn't match combined number of lines
E         Expected number of lines: 1000000
E         Actual number of lines: 999999
E         Where number of lines for target_1 file: 497065 and target_2 file: 502934
E         Test input data: {'input': 'large_1M_events.log', 'target_1': 'events_target_1.log', 'target_2': 'events_target_2.log'}
E       assert 1000000 == 999999
E         -1000000
E         +999999
```
Test - `test/test_events_log_data_distribution.py::TestLogDistribution::test_verify_file_content_matches`
```commandline
E       AssertionError: Total of 3 event(s) were corrupter after data went through Splitter
E             
E         Following list of pairs (receiving_host_name, log_line) were corrupted:
E         [('target_1', 'This is event number vent number 347357\n'), ('target_1', 'T340334\n'), ('target_1', 'This is ehis is event number 359059\n')]
E             
E       assert 3 == 0
E         +3
E         -0
```

Running tests locally:
---
In order to run tests locally you need to install supported python version from **Support Documentation** section.
You can find instructions here: https://www.python.org/downloads/

Stable version `Python==3.8` is recommended

Clone the project repository:
```commandline
git clone https://github.com/Dkhazhinov/cribl.git
```

Once Python installed and project repo cloned you need to install dependencies.
From project root directory run following commands:
```commandline
python -m pip install --upgrade pip
pip install -r requirements.txt
```

###There are two ways of running tests locally:
- Running python script `deployment.py` that will perform automated deployment and tear down

`deployment.py` script supports `test` arguments that will run all tests automatically:
```commandline
python deployment_script.py -test
```

OR

To run the script from root directory:
```commandline
python deployment_script.py
```
Once deployment completed successfully run pytest command to collect and run all tests:
```commandline
pytest -v --html=./outputs/test_report.html --self-contained-html
```

In either case temporary directory `/outputs/` will be created and all artifacts will be copied into it.

To see all supported arguments for `deploymnet.py` script run:
```commandline
python deployment.py -help
```

Support Documentation
---
All dependencies automatically downloaded and installed inside the pipeline/workflow.

Python version supported
```
3.6+
```
Package support
```
pytest v 4.6+
pytest-html v1.20+
```
