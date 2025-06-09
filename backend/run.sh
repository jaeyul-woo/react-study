#!/bin/bash

# Common variables
WORKING_DIRECTORY=`pwd`

# Python related vairables
PYTHON_VENV_DIRECTORY="${WORKING_DIRECTORY}/.venv"
PYTHON_ACTIVATE_DIRECTORY="${PYTHON_VENV_DIRECTORY}/bin/activate"
PYTHON_REQUIREMENTS_DIRECTORY="${WORKING_DIRECTORY}/requirements.txt"

print_help() {
    echo ""
    echo "Welcome to Chronos for CDS"
    echo ""
    echo "Usage: ./build.sh <command> [-h | --help] [-c | --clean]"
    echo ""
    echo "These are list of commands"
    echo "   help       : print help message"
    echo "   clean      : clean python environment"
    echo ""
    echo "e.g."
    echo "./run.sh -h   <- Print help"
    echo "./run.sh -c   <- Clean python"
    echo ""
}

remove_pycache() {
    # Remove all __pycache__ directories
    find . -type d -name "__pycache__" -exec rm -r {} +
}
remove_venv() {
    if [ -d "${PYTHON_VENV_DIRECTORY}" ]; then
        rm -r ${PYTHON_VENV_DIRECTORY}
    fi
}
activate_python_env() {
    source ${PYTHON_ACTIVATE_DIRECTORY}
}
init_venv() {
    if [ ! -d "${PYTHON_VENV_DIRECTORY}" ]; then
        python3 -m venv ${PYTHON_VENV_DIRECTORY}
        pip install --upgrade pip
        pip install -r ${PYTHON_REQUIREMENTS_DIRECTORY}
    fi
    activate_python_env
}
clean_env() {
    remove_pycache
    remove_venv
    init_venv
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case ${1} in
        -h|--help)      print_help; exit 0;;
        -c|--clean)     clean_env;  exit 0;;
        --) shift;;
        *)  COMMAND="${1}";;
    esac
    shift
done

case ${COMMAND} in
    help)
        print_help; exit 0;;
    clean)
        clean_env;  exit 0;;
    # *)
    #     echo "Unknown command '${COMMAND}'";
    #     exit 1;;
esac

export FLASK_APP=app.py
flask run
