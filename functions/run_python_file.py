import os
import subprocess

from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not full_path.startswith(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    if not full_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        command = ["python3", full_path] + args
        completed_process = subprocess.run(
            command, text=True, timeout=30, cwd=working_directory, capture_output=True
        )
        if (completed_process.stdout == "") and (completed_process.stderr == ""):
            string_output = "No output produced"
        else:
            string_output = f"STDOUT: {completed_process.stdout} \n STDERR: {completed_process.stderr}"
        if completed_process.returncode != 0:
            string_output += f"Process exited with code {completed_process.returncode}"
        return string_output
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file. ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The location of the Python file should be executed. ",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="A list with arguments to be passed to the Python function if needed. "
            )
        },
    ),
)

