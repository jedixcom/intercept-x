import re

# Example keystroke log
keystroke_log = """
2024-04-02 21:35:13: 
2024-04-02 21:35:18: HalloAdnan
JalHa
2024-04-02 21:35:52: lloMichael

2024-04-02 21:35:53: Hall
2024-04-02 21:36:18: oMichael

2024-04-02 21:36:25: Ditiseentest
HalloMan
k
2024-04-02 21:36:54: eystrokennadeenter
"""

# Splitting by lines and filtering out empty ones
lines = [line.strip() for line in keystroke_log.split("\n") if line.strip()]

# Removing timestamps and extra whitespace
cleaned_lines = [re.sub(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}: ", "", line) for line in lines]

# Joining the cleaned lines into a single string
cleaned_text = " ".join(cleaned_lines)

print(cleaned_text)