import subprocess

scripts = [
    "python page.py",
    "python page1.py",
    "python page2.py",
    "python page3.py",
    "python page4.py"
]

processes = []

# Start all scripts
for cmd in scripts:
    p = subprocess.Popen(cmd, shell=True)
    processes.append(p)

# Wait for all scripts to finish
for p in processes:
    p.wait()

print("✅ All scripts finished.")