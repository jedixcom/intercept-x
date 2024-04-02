import subprocess

def run_powershell_command(command):
    subprocess.run(['powershell', '-Command', command], shell=True)

# Example usage
powershell_command = 'Start-Process pwsh -Verb RunAs'
run_powershell_command(powershell_command)
