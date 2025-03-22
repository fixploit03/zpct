import sys
import os
import subprocess
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLineEdit, QTextEdit, QLabel, QComboBox, QMessageBox, 
                             QFileDialog, QInputDialog)
from PyQt5.QtCore import QThread, pyqtSignal, Qt

class CrackThread(QThread):
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                self.output_signal.emit(output.strip())
        stderr = process.stderr.read()
        if stderr:
            self.output_signal.emit(stderr.strip())
        self.finished_signal.emit(process.returncode)

class ZPCTGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZPCT v2.5 - ZIP Password Cracker")
        self.setGeometry(100, 100, 900, 700)
        self.zip_file = ""
        self.encryption = ""
        self.method = ""
        self.is_multi_file = False
        self.hash_file = ""
        self.init_ui()
        self.check_system()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Banner
        self.banner = QLabel("ZPCT v2.5\nBy Rofi (Fixploit03)\nhttps://github.com/fixploit03/zpct")
        self.banner.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.banner)

        # ZIP File Input
        self.zip_layout = QHBoxLayout()
        self.zip_label = QLabel("Enter ZIP file name:")
        self.zip_input = QLineEdit()
        self.zip_browse = QPushButton("Browse")
        self.zip_browse.clicked.connect(self.browse_zip)
        self.zip_validate = QPushButton("Validate")
        self.zip_validate.clicked.connect(self.validate_zip)
        self.zip_layout.addWidget(self.zip_label)
        self.zip_layout.addWidget(self.zip_input)
        self.zip_layout.addWidget(self.zip_browse)
        self.zip_layout.addWidget(self.zip_validate)
        self.layout.addLayout(self.zip_layout)

        # Technique Selection
        self.tech_label = QLabel("Select cracking technique:")
        self.tech_combo = QComboBox()
        self.tech_combo.addItems(["1. Conventional (Without Hash)", "2. Conventional (With Hash)", "3. KPA (Known Plaintext Attack)"])
        self.layout.addWidget(self.tech_label)
        self.layout.addWidget(self.tech_combo)

        # Tool and Hash Extraction (for Technique 2)
        self.tool_layout = QHBoxLayout()
        self.tool_label = QLabel("Select tool (Technique 2):")
        self.tool_combo = QComboBox()
        self.tool_combo.addItems(["1. John The Ripper", "2. Hashcat"])
        self.tool_combo.setEnabled(False)
        self.hash_label = QLabel("Hash extraction method:")
        self.hash_combo = QComboBox()
        self.hash_combo.addItems(["1. Extract from one file", "2. Extract default (all files)"])
        self.hash_combo.setEnabled(False)
        self.tool_layout.addWidget(self.tool_label)
        self.tool_layout.addWidget(self.tool_combo)
        self.tool_layout.addWidget(self.hash_label)
        self.tool_layout.addWidget(self.hash_combo)
        self.tech_combo.currentIndexChanged.connect(self.toggle_technique_options)
        self.layout.addLayout(self.tool_layout)

        # Output Area
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.layout.addWidget(self.output)

        # Start Button
        self.start_button = QPushButton("Start Cracking")
        self.start_button.clicked.connect(self.start_cracking)
        self.start_button.setEnabled(False)
        self.layout.addWidget(self.start_button)

    def check_system(self):
        self.output.append("[INFO] Checking system requirements...")
        if os.geteuid() != 0:
            QMessageBox.critical(self, "Error", "This script must be run as root.")
            sys.exit(1)
        
        try:
            os_release = subprocess.check_output("lsb_release -i", shell=True, text=True).strip()
            if "Kali" not in os_release:
                QMessageBox.critical(self, "Error", "This script can only run on Kali Linux.")
                sys.exit(1)
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", "Failed to check operating system.")
            sys.exit(1)

        required_tools = ["lsb_release", "combinator", "toggle-case", "john", "hashcat", "zipinfo", "7z", "unzip", "zip2hashcat", "fcrackzip", "bkcrack"]
        missing = [tool for tool in required_tools if subprocess.call(f"command -v {tool}", shell=True) != 0]
        if missing:
            QMessageBox.critical(self, "Error", f"The following tools are not installed: {', '.join(missing)}")
            sys.exit(1)
        self.output.append("[INFO] System check passed.")

    def browse_zip(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select ZIP File", "", "ZIP Files (*.zip)")
        if file_name:
            self.zip_input.setText(file_name)

    def validate_zip(self):
        self.zip_file = self.zip_input.text().strip()
        if not self.zip_file:
            self.output.append("[ERROR] ZIP file name cannot be empty.")
            return
        if not os.path.isfile(self.zip_file):
            self.output.append("[ERROR] ZIP file not found.")
            return
        if not self.zip_file.endswith(".zip"):
            self.output.append("[ERROR] File is not a ZIP file.")
            return

        self.output.append("[INFO] Checking ZIP file...")
        result = subprocess.check_output(f"zipinfo -v '{self.zip_file}'", shell=True, text=True, stderr=subprocess.STDOUT)
        if "cannot find zipfile directory" in result.lower():
            self.output.append("[ERROR] Invalid or corrupted ZIP file.")
            return
        if "encrypted" not in result.lower():
            self.output.append("[ERROR] ZIP file is not encrypted.")
            return

        # Check number of files
        self.is_multi_file = len(subprocess.check_output(f"zipinfo '{self.zip_file}'", shell=True, text=True).splitlines()) > 3

        # Check compression method
        methods = subprocess.check_output(f"7z l -slt '{self.zip_file}' | grep -i 'method'", shell=True, text=True).splitlines()
        deflate = any("Deflate" in m for m in methods)
        store = any("Store" in m for m in methods)
        self.method = "Mixed" if deflate and store else "Compressed" if deflate else "Uncompressed"

        # Check encryption
        enc_result = subprocess.check_output(f"7z l -slt '{self.zip_file}' | grep -i 'method'", shell=True, text=True)
        if "ZipCrypto" in enc_result:
            self.encryption = "ZipCrypto"
        elif "AES-128" in enc_result:
            self.encryption = "AES-128"
        elif "AES-192" in enc_result:
            self.encryption = "AES-192"
        elif "AES-256" in enc_result:
            self.encryption = "AES-256"

        status = "Multi-File" if self.is_multi_file else ""
        self.output.append(f"[INFO] ZIP file found. Encryption: {self.encryption} ({self.method} {status})")
        self.start_button.setEnabled(True)

    def toggle_technique_options(self):
        tech = self.tech_combo.currentIndex() + 1
        self.tool_combo.setEnabled(tech == 2)
        self.hash_combo.setEnabled(tech == 2)
        if tech in [1, 3] and self.encryption != "ZipCrypto":
            self.output.append("[ERROR] Technique 1 and 3 are only available for ZipCrypto encryption.")
            self.start_button.setEnabled(False)
        else:
            self.start_button.setEnabled(True)

    def start_cracking(self):
        if not self.zip_file:
            self.output.append("[ERROR] Please validate a ZIP file first.")
            return

        technique = self.tech_combo.currentIndex() + 1
        self.output.append(f"[INFO] Starting cracking with technique {technique}...")

        if technique == 1:
            self.crack_conventional_no_hash()
        elif technique == 2:
            self.crack_conventional_with_hash()
        elif technique == 3:
            self.crack_kpa()

    def crack_conventional_no_hash(self):
        tech, ok = QInputDialog.getItem(self, "Select Technique", "Choose cracking technique:", 
                                        ["1. Dictionary Attack", "2. Brute Force Attack"], 0, False)
        if not ok:
            return
        tech = int(tech[0])

        if tech == 1:
            wordlist, _ = QFileDialog.getOpenFileName(self, "Select Wordlist", "", "Text Files (*.txt)")
            if not wordlist or not os.path.isfile(wordlist):
                self.output.append("[ERROR] Invalid or no wordlist selected.")
                return
            command = f"fcrackzip -v -u -D -p '{wordlist}' '{self.zip_file}'"
        else:
            min_len, _ = QInputDialog.getInt(self, "Brute Force", "Minimum password length:", 1, 1)
            max_len, _ = QInputDialog.getInt(self, "Brute Force", "Maximum password length:", 6, min_len)
            command = f"fcrackzip -v -u -b -c aA1! -l {min_len}-{max_len} '{self.zip_file}'"

        self.run_crack(command, "Fcrackzip", "Dictionary Attack" if tech == 1 else "Brute Force Attack")

    def crack_conventional_with_hash(self):
        os.makedirs("/opt/zpct/file_hash", exist_ok=True)
        hash_method = self.hash_combo.currentIndex() + 1
        self.hash_file = f"/opt/zpct/file_hash/hash_{os.path.basename(self.zip_file)}.txt"

        if hash_method == 1:
            files = subprocess.check_output(f"unzip -l '{self.zip_file}'", shell=True, text=True).splitlines()[3:-2]
            file_list = [f.split()[-1] for f in files]
            inner_file, ok = QInputDialog.getItem(self, "Select File", "Choose a file inside ZIP:", file_list, 0, False)
            if not ok:
                return
            command = f"zip2hashcat -o '{inner_file}' '{self.zip_file}' > '{self.hash_file}'"
        else:
            command = f"zip2hashcat '{self.zip_file}' > '{self.hash_file}'"

        subprocess.run(command, shell=True)
        if not os.path.isfile(self.hash_file) or not ( "$pkzip" in open(self.hash_file).read() or "$zip2" in open(self.hash_file).read()):
            self.output.append("[ERROR] Failed to extract hash.")
            return
        self.output.append(f"[INFO] Hash extracted to: {self.hash_file}")

        tool = self.tool_combo.currentIndex() + 1
        if tool == 1:
            self.run_john()
        else:
            self.run_hashcat()

    def run_john(self):
        tech, ok = QInputDialog.getItem(self, "Select Technique", "Choose cracking technique:", 
                                        ["1. Dictionary Attack", "2. Brute Force Attack", "3. Combinator Attack", 
                                         "4. Mask Attack", "5. Prince Attack", "6. Hybrid Attack", 
                                         "7. Subsets Attack", "8. Toggle Case Attack"], 0, False)
        if not ok:
            return
        tech = int(tech[0])
        format = "PKZIP" if "$pkzip" in open(self.hash_file).read() else "ZIP"

        if tech == 1:
            wordlist = self.get_wordlist()
            command = f"john --wordlist='{wordlist}' --format={format} --pot=pot.txt --verbosity=6 --progress-every=1 '{self.hash_file}'"
        elif tech == 2:
            min_len, max_len = self.get_length()
            command = f"john --incremental --min-length={min_len} --max-length={max_len} --format={format} --pot=pot.txt --verbosity=6 --progress-every=1 '{self.hash_file}'"
        elif tech == 3:
            wl1, wl2 = self.get_two_wordlists()
            command = f"combinator '{wl1}' '{wl2}' | john --stdin --format={format} --pot=pot.txt --verbosity=6 --progress-every=1 '{self.hash_file}'"
        elif tech == 4:
            mask = self.get_mask()
            command = f"john --mask='{mask}' --format={format} --pot=pot.txt --verbosity=6 --progress-every=1 '{self.hash_file}'"
        elif tech == 5:
            wordlist = self.get_wordlist()
            command = f"john --prince='{wordlist}' --format={format} --pot=pot.txt --verbosity=6 --progress-every=1 '{self.hash_file}'"
        elif tech == 6:
            wordlist = self.get_wordlist()
            mask = self.get_mask()
            command = f"john --wordlist='{wordlist}' --mask='?w{mask}' --format={format} --pot=pot.txt --verbosity=6 --progress-every=1 '{self.hash_file}'"
        elif tech == 7:
            min_len, max_len = self.get_length()
            charset, _ = QInputDialog.getText(self, "Subsets Attack", "Enter character set (e.g., aA1$):")
            command = f"john --subsets='{charset}' --min-length={min_len} --max-length={max_len} --format={format} --pot=pot.txt --verbosity=6 --progress-every=1 '{self.hash_file}'"
        elif tech == 8:
            wordlist = self.get_wordlist()
            command = f"toggle-case '{wordlist}' | john --stdin --format={format} --pot=pot.txt --verbosity=6 --progress-every=1 '{self.hash_file}'"

        self.run_crack(command, "John The Ripper", ["Dictionary Attack", "Brute Force Attack", "Combinator Attack", 
                                                    "Mask Attack", "Prince Attack", "Hybrid Attack", 
                                                    "Subsets Attack", "Toggle Case Attack"][tech-1])

    def run_hashcat(self):
        mode = {"ZipCrypto": "17200" if not self.is_multi_file else "17220" if self.method == "Compressed" else "17225",
                "AES-128": "13600", "AES-192": "13600", "AES-256": "13600"}[self.encryption]
        
        tech, ok = QInputDialog.getItem(self, "Select Technique", "Choose cracking technique:", 
                                        ["1. Dictionary Attack", "2. Brute Force Attack", "3. Combinator Attack", 
                                         "4. Mask Attack", "5. Prince Attack", "6. Hybrid Attack", 
                                         "7. Subsets Attack", "8. Toggle Case Attack"], 0, False)
        if not ok:
            return
        tech = int(tech[0])

        if tech == 1:
            wordlist = self.get_wordlist()
            command = f"hashcat -a 0 -m {mode} '{self.hash_file}' '{wordlist}' --status --status-timer=1 --potfile-path pot.txt"
        elif tech == 2:
            min_len, max_len = self.get_length()
            mask = "?a" * max_len
            command = f"hashcat -a 3 -m {mode} '{self.hash_file}' '{mask}' --increment --increment-min={min_len} --increment-max={max_len} --status --status-timer=1 --potfile-path pot.txt"
        elif tech == 3:
            wl1, wl2 = self.get_two_wordlists()
            command = f"hashcat -a 1 -m {mode} '{self.hash_file}' '{wl1}' '{wl2}' --status --status-timer=1 --potfile-path pot.txt"
        elif tech == 4:
            mask = self.get_mask()
            command = f"hashcat -a 3 -m {mode} '{self.hash_file}' '{mask}' --status --status-timer=1 --potfile-path pot.txt"
        elif tech == 5:
            wordlist = self.get_wordlist()
            command = f"princeprocessor < '{wordlist}' | hashcat -a 0 -m {mode} '{self.hash_file}' --status --status-timer=1 --potfile-path pot.txt"
        elif tech == 6:
            wordlist = self.get_wordlist()
            mask = self.get_mask()
            command = f"hashcat -a 6 -m {mode} '{self.hash_file}' '{wordlist}' '{mask}' --status --status-timer=1 --potfile-path pot.txt"
        elif tech == 7:
            min_len, max_len = self.get_length()
            charset, _ = QInputDialog.getText(self, "Subsets Attack", "Enter character set (e.g., aA1$):")
            mask = "?1" * max_len
            command = f"hashcat -a 3 -m {mode} '{self.hash_file}' -1 '{charset}' '{mask}' --status --status-timer=1 --potfile-path pot.txt"
        elif tech == 8:
            wordlist = self.get_wordlist()
            command = f"toggle-case '{wordlist}' | hashcat -a 0 -m {mode} '{self.hash_file}' --status --status-timer=1 --potfile-path pot.txt"

        self.run_crack(command, "Hashcat", ["Dictionary Attack", "Brute Force Attack", "Combinator Attack", 
                                            "Mask Attack", "Prince Attack", "Hybrid Attack", 
                                            "Subsets Attack", "Toggle Case Attack"][tech-1])

    def crack_kpa(self):
        files = subprocess.check_output(f"bkcrack -L '{self.zip_file}'", shell=True, text=True).splitlines()[2:]
        store_files = [f.split()[2] for f in files if "Store" in f]
        if not store_files:
            self.output.append("[ERROR] No files with Store compression found.")
            return
        inner_file, ok = QInputDialog.getItem(self, "Select File", "Choose a file with Store compression:", store_files, 0, False)
        if not ok:
            return

        plain_file, _ = QFileDialog.getOpenFileName(self, "Select Known Plaintext File", "", "Text Files (*.txt)")
        if not plain_file or not os.path.isfile(plain_file):
            self.output.append("[ERROR] Invalid or no plaintext file selected.")
            return

        command = f"bkcrack -C '{self.zip_file}' -c '{inner_file}' -p '{plain_file}'"
        self.run_crack(command, "Bkcrack", "KPA", is_kpa=True)

    def get_wordlist(self):
        wordlist, _ = QFileDialog.getOpenFileName(self, "Select Wordlist", "", "Text Files (*.txt)")
        if not wordlist or not os.path.isfile(wordlist):
            self.output.append("[ERROR] Invalid or no wordlist selected.")
            raise ValueError
        return wordlist

    def get_two_wordlists(self):
        wl1 = self.get_wordlist()
        wl2 = self.get_wordlist()
        return wl1, wl2

    def get_length(self):
        min_len, _ = QInputDialog.getInt(self, "Password Length", "Minimum password length:", 1, 1)
        max_len, _ = QInputDialog.getInt(self, "Password Length", "Maximum password length:", 6, min_len)
        return min_len, max_len

    def get_mask(self):
        mask, _ = QInputDialog.getText(self, "Mask Attack", "Enter mask pattern (?l?u?d?s?a):")
        if not re.match(r"^(\?l|\?u|\?d|\?s|\?a)+$", mask):
            self.output.append("[ERROR] Invalid mask pattern.")
            raise ValueError
        return mask

    def run_crack(self, command, tool, technique, is_kpa=False):
        self.output.append(f"[INFO] Starting {tool} with {technique}...")
        self.crack_thread = CrackThread(command)
        self.crack_thread.output_signal.connect(self.update_output)
        self.crack_thread.finished_signal.connect(lambda code: self.process_result(code, tool, technique, is_kpa))
        self.crack_thread.start()

    def update_output(self, text):
        self.output.append(text)

    def process_result(self, return_code, tool, technique, is_kpa=False):
        os.makedirs("/opt/zpct/hasil_cracking", exist_ok=True)
        result_file = f"/opt/zpct/hasil_cracking/{os.path.basename(self.zip_file)}.txt"
        csv_file = "/opt/zpct/hasil_cracking/cracked.csv"
        start_time = subprocess.check_output("date +'%d-%m-%Y/ %H:%M:%S'", shell=True, text=True).strip()
        end_time = subprocess.check_output("date +'%d-%m-%Y/ %H:%M:%S'", shell=True, text=True).strip()

        if os.path.isfile("pot.txt"):
            with open("pot.txt") as f:
                content = f.read()
            if is_kpa and "Found a solution" in content:
                password = " ".join(content.splitlines()[-1].split()[:3])
                self.output.append(f"[SUCCESS] Encryption keys found: {password}")
                min_len, max_len = self.get_length()
                command = f"bkcrack -k {password} -b ?p -l {min_len}..{max_len} | tee pot2.txt"
                subprocess.run(command, shell=True)
                with open("pot2.txt") as f2:
                    if "password:" in f2.read():
                        password = f2.read().split()[-1]
                        self.save_result(password, tool, technique, result_file, csv_file, start_time, end_time)
                    else:
                        self.output.append("[ERROR] Password not found.")
                os.remove("pot2.txt")
            elif tool == "Fcrackzip" and "PASSWORD FOUND" in content.upper():
                password = content.split()[-1]
                self.save_result(password, tool, technique, result_file, csv_file, start_time, end_time)
            elif ":" in content:
                password = content.split(":")[1].strip()
                self.save_result(password, tool, technique, result_file, csv_file, start_time, end_time)
            else:
                self.output.append("[ERROR] Password not found.")
            os.remove("pot.txt")
        else:
            self.output.append("[ERROR] Cracking failed.")
        self.output.append(f"[INFO] Finished at: {end_time}")

    def save_result(self, password, tool, technique, result_file, csv_file, start_time, end_time):
        self.output.append(f"[SUCCESS] Password found: {password}")
        with open(result_file, "w") as f:
            f.write(f"[+] File ZIP: {os.path.realpath(self.zip_file)}\n[+] Password: {password}\n")
        self.output.append(f"[INFO] Result saved to: {result_file}")
        
        if not os.path.isfile(csv_file):
            with open(csv_file, "w") as f:
                f.write("File ZIP, Password, Tool Used, Technique Used, Start Time, End Time\n")
        with open(csv_file, "a") as f:
            f.write(f"{os.path.realpath(self.zip_file)}, {password}, {tool}, {technique}, {start_time}, {end_time}\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZPCTGui()
    window.show()
    sys.exit(app.exec_())
