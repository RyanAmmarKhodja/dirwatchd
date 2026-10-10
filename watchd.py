import os
import sys
import json
import time
import hashlib
import getpass
from datetime import datetime

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def hash_file(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None

def scan_directory(directory):
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            h = hash_file(filepath)
            if h:
                file_hashes[filepath] = h
    return file_hashes

def log_change(log_path, file_path):
    user = getpass.getuser()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{user}]: [{timestamp}]: [{file_path}]\n"
    
    print(log_entry.strip())
    with open(log_path, "a") as f:
        f.write(log_entry)

def main():
    config = load_config()
    target_dir = config["watch_directory"]
    log_file = config["log_file"]
    baseline_file = config["baseline_file"]
    interval = config["check_interval_seconds"]

    # Initialize or load baseline
    if not os.path.exists(baseline_file):
        print(f"Creating baseline for {target_dir}...")
        baseline = scan_directory(target_dir)
        with open(baseline_file, "w") as f:
            json.dump(baseline, f, indent=4)
    else:
        with open(baseline_file, "r") as f:
            baseline = json.load(f)

    print(f"Monitoring {target_dir} for changes...")
    
    while True:
        time.sleep(interval)
        current_state = scan_directory(target_dir)
        
        # Check for modified or new files
        for filepath, current_hash in current_state.items():
            if filepath not in baseline:
                log_change(log_file, f"CREATED: {filepath}")
                baseline[filepath] = current_hash
            elif baseline[filepath] != current_hash:
                log_change(log_file, f"MODIFIED: {filepath}")
                baseline[filepath] = current_hash
                
        # Check for deleted files
        deleted_files = set(baseline.keys()) - set(current_state.keys())
        for filepath in deleted_files:
            log_change(log_file, f"DELETED: {filepath}")
            del baseline[filepath]
            
        # Update baseline file
        with open(baseline_file, "w") as f:
            json.dump(baseline, f, indent=4)

if __name__ == "__main__":
    main()