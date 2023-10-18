import subprocess
import sys

# Some code here

pid = subprocess.Popen([sys.executable, "detect.py"]) # Call subprocess
pid2 = subprocess.Popen([sys.executable, "detect2.py"]) # Call subprocess
print(pid,pid2)