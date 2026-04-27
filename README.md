# 🛡️ GitShield

**GitShield** is an advanced CLI tool that analyzes GitHub repositories for potential security threats **before you run the code**.

It performs static analysis on source code, detects suspicious patterns, and provides a **risk score and verdict** in a clean, modern terminal interface.

---

<p align="center">
  <img src="./logo.png" width="260"/>
</p>

<h1 align="center">🛡️ GitShield</h1>

<p align="center">
  Advanced GitHub Security Scanner<br>
  <b>by frizz</b>
</p>

---

## 🚀 Features

* 🔍 Scan any public GitHub repository **without cloning**
* 🧠 Detect suspicious behaviors (command execution, obfuscation, etc.)
* 📊 Intelligent risk scoring system
* ⚠️ Threat classification (Low / Suspicious / High risk)
* 🎨 Modern CLI interface (Rich)
* 🧹 Temporary scan (no files stored on your machine)

---

## 🧠 How it works

GitShield performs a **safe static analysis**:

1. Downloads the repository as a ZIP
2. Extracts it in a temporary folder
3. Scans files for suspicious patterns
4. Calculates a global risk score
5. Displays a detailed report
6. Deletes everything automatically

---

## 📦 Installation

### 🐧 Linux / macOS

```bash
git clone https://github.com/ATROUN-Ryan-2326009b/GitShield.git
cd GitShield
chmod +x install.sh
./install.sh
```

---

### 🪟 Windows

```bat
git clone https://github.com/ATROUN-Ryan-2326009b/GitShield.git
cd GitShield
install.bat
```

---

## ▶️ Usage

```bash
gitshield
```

or:

```bash
GitShield
```

Then enter a GitHub repository URL:

```text
https://github.com/pallets/flask
```

---

## 📊 Example Output

```text
Repository: https://github.com/pallets/flask
Branch scanned: main

Total files analyzed: 28
Suspicious files: 6
Threatening files: 2

Security risk score: 17%
Verdict: Low risk
```

---

## ⚠️ Disclaimer

GitShield **does NOT guarantee that a repository is safe**.

It uses static analysis to detect obvious suspicious patterns.
Advanced malware or obfuscated code may bypass detection.

👉 Always review code manually before running it.

---

## 🧩 Detection Categories

GitShield detects patterns such as:

* Command execution (`os.system`, `subprocess`)
* Network activity (`requests`, `socket`)
* Credential access (`env`, API keys)
* Destructive actions (file deletion)
* Obfuscation (`base64`, `marshal`)
* Persistence mechanisms (cron, systemctl)

---

## 🎯 Roadmap

* 🌐 Web interface (dashboard)
* 📄 PDF export reports
* 🧠 AI-assisted analysis
* 🔒 Dependency vulnerability scanning
* 📊 Scan history

---

## 👨‍💻 Author

**frizz**

---

