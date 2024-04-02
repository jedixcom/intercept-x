import elevate
import subprocess

# Elevate privileges
elevate.elevate()

# Your PowerShell command
powershell_command = 'Set-MpPreference -DisableRealtimeMonitoring $true'
powershell_command = 'Set-MpPreference -DisableBehaviorMonitoring $true'
powershell_command = 'Set-MpPreference -DisableBlockAtFirstSeen $true'
powershell_command = 'Set-MpPreference -DisableIOAVProtection $true'
powershell_command = 'Set-MpPreference -PUAProtection 0'
powershell_command = 'Set-MpPreference -SubmitSamplesConsent 0'
powershell_command = 'Set-MpPreference -MAPSReporting 0'
powershell_command = 'Set-MpPreference -SignatureDisableUpdateOnStartupWithoutEngine 0'


# PowerShell commands to check status
powershell_commands = [
    'Get-MpPreference -DisableRealtimeMonitoring',
    'Get-MpPreference -DisableBehaviorMonitoring',
    'Get-MpPreference -DisableBlockAtFirstSeen',
    'Get-MpPreference -DisableIOAVProtection',
    'Get-MpPreference -PUAProtection',
    'Get-MpPreference -SubmitSamplesConsent',
    'Get-MpPreference -MAPSReporting',
    'Get-MpPreference -SignatureDisableUpdateOnStartupWithoutEngine'
]


# Execute the PowerShell commands and print the output
for command in powershell_commands:
    print(f"Command: {command}")
    subprocess.run(['powershell', '-Command', command], shell=True)
    print("-" * 50)  # Separating lines for clarity
