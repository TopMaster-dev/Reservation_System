import subprocess
from settings import load_settings

# Make set_tag available for import
set_tag = load_settings('settings.json')

def main():
    scripts = [
        "python page.py",
        # "python page1.py",
        # "python page2.py",
        # "python page3.py",
        # "python page4.py"
    ]

    processes = []
    if(set_tag):
        # Start all scripts
        for cmd in scripts:
            p = subprocess.Popen(cmd, shell=True)
            processes.append(p)

        # Wait for all scripts to finish
        for p in processes:
            p.wait()

        print("✅ All scripts finished.")

if __name__ == "__main__":
    main()