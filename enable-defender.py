import subprocess

def enable_windows_defender():
    powershell_script = 'enable_defender.ps1'
    # Execute the PowerShell script using PowerShell
    try:
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", powershell_script], check=True)
        print("Windows Defender is enabled.")
    except subprocess.CalledProcessError as e:
        print(f"Error enabling Windows Defender: {e}")

if __name__ == "__main__":
    enable_windows_defender()

