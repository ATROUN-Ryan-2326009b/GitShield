SIGNATURES = {
    "command_execution": {
        "severity": 25,
        "patterns": [
            r"\bos\.system\s*\(",
            r"\bsubprocess\.(Popen|call|run)\s*\(",
            r"\beval\s*\(",
            r"\bexec\s*\("
        ]
    },
    "network_activity": {
        "severity": 15,
        "patterns": [
            r"\brequests\.(get|post)\s*\(",
            r"\burllib\.request\.urlopen\s*\(",
            r"\bsocket\.socket\s*\("
        ]
    },
    "credential_access": {
        "severity": 20,
        "patterns": [
            r"(AWS_SECRET_ACCESS_KEY|GITHUB_TOKEN|PRIVATE_KEY|API_KEY)",
            r"(password|passwd|token|secret)\s*=\s*[\"'][^\"']{8,}[\"']"
        ]
    },
    "destructive_action": {
        "severity": 35,
        "patterns": [
            r"\bshutil\.rmtree\s*\(",
            r"\bos\.remove\s*\(",
            r"\bos\.unlink\s*\(",
            r"rm\s+-rf\s+/"
        ]
    },
    "obfuscation": {
        "severity": 30,
        "patterns": [
            r"\bbase64\.b64decode\s*\(",
            r"\bmarshal\.loads\s*\(",
            r"\bcompile\s*\(",
            r"__import__\s*\("
        ]
    },
    "persistence": {
        "severity": 35,
        "patterns": [
            r"systemctl\s+enable",
            r"crontab\s+-e",
            r"schtasks\s+/create",
            r"reg\s+add"
        ]
    }
}