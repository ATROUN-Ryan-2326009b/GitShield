SIGNATURES = {
    "command_execution": {
        "severity": 25,
        "patterns": [
            "os.system(",
            "subprocess.Popen(",
            "subprocess.call(",
            "subprocess.run(",
            "exec(",
            "eval("
        ]
    },
    "network_activity": {
        "severity": 15,
        "patterns": [
            "requests.get(",
            "requests.post(",
            "socket.socket(",
            "urllib.request.urlopen(",
            "curl ",
            "wget "
        ]
    },
    "credential_access": {
        "severity": 20,
        "patterns": [
            "os.environ.get(",
            "os.getenv(",
            ".env",
            "AWS_SECRET_ACCESS_KEY",
            "GITHUB_TOKEN",
            "API_KEY",
            "SECRET_KEY",
            "PRIVATE_KEY"
        ]
    },
    "destructive_action": {
        "severity": 45,
        "patterns": [
            "rm -rf",
            "shutil.rmtree(",
            "os.remove(",
            "os.unlink(",
            "Path.unlink(",
            "del /f"
        ]
    },
    "obfuscation": {
        "severity": 35,
        "patterns": [
            "base64.b64decode(",
            "marshal.loads(",
            "__import__("
        ]
    },
    "persistence": {
        "severity": 35,
        "patterns": [
            "crontab",
            "systemctl enable",
            "schtasks",
            "reg add"
        ]
    }
}