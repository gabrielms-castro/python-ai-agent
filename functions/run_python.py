import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    try:
        sub = subprocess.run(
            ["python3", abs_file_path],
            timeout=30,
            capture_output=True,
            cwd=abs_working_directory,
            text=True
        )
        stdout = sub.stdout.strip()
        stderr = sub.stderr.strip()
        
        output_lines = []
        if stdout:
            output_lines.append(f"STDOUT:\n{stdout}")
        if stderr:
            output_lines.append(f"STDERR:\n{stderr}")
        
        if sub.returncode != 0:
            return f"Process exited with code {sub.returncode}.\nError: {sub.stderr.strip()}"
        
        if not sub.stdout.strip() and not sub.stderr.strip():
            return "No output produced."
        
        return "\n".join(output_lines)
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
run_python_file("calculator", "main.py")