dirwatchd is a lightweight Linux daemon that monitors specified directories for file changes, creations, and deletions using SHA-256 integrity hashing and logs events with system metadata.

Features

    Integrity Monitoring: Detects modified, added, or deleted files using SHA-256 hashes.

    Audit Logging: Records timestamps, system users, and file actions to an output log.

    Systemd Ready: Includes a unit file to run seamlessly as a background service.

    Configurable: Managed via a simple JSON configuration file.
