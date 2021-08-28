import os
import sys

# list of container names
containers = [
    "cribl_target_1",
    "cribl_target_2",
    "cribl_splitter",
    "cribl_agent"
]

# temp_directory name
temp_directory = "outputs"


def run_deployment():
    # create temporary directory
    os.system(f"mkdir {temp_directory}")

    # start up docker containers
    os.system("docker-compose -f 'docker-compose.yml' up -d --build")

    # copy events file from target_1 and target_2 containers
    os.system(f"docker cp cribl_target_1_1:/usr/src/events.log ./{temp_directory}/events_target_1.log")
    os.system(f"docker cp cribl_target_2_1:/usr/src/events.log ./{temp_directory}/events_target_2.log")

    # tear down docker containers
    os.system("docker-compose -f 'docker-compose.yml' down")

    # remove docker images
    for container in containers:
        os.system(f"docker rmi {container} --force")


def run_tests():
    run_deployment()
    os.system(f"pytest -v --html=./{temp_directory}/test_report.html --self-contained-html")
    # remove file that was created by testing framework
    os.system(f"rm ./{temp_directory}/combined_events.log")


# parse command arguments
if len(sys.argv) == 1:
    run_deployment()
# deployment script only supports one argument
elif 3 > len(sys.argv) > 1:
    if sys.argv[1] == "-test":
        run_tests()
    elif sys.argv[1] == "-help":
        supported_arguments = (
            "\nWhen no arguments provided script will run full deployment\n"
            "\n-test - collect and run all tests after deployment\n"
            "-help - see all available arguments\n"
        )
        print(supported_arguments)

