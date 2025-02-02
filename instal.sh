#!/bin/bash

# Fungsi untuk mengecek root
function cek_root(){
	if [[ $EUID -ne 0 ]]; then
		echo "[-] Script ini harus dijalankan sebagai rooi."
		exit 1
	fi
}

# Fungsi untuk mengonfirmasi
function konfirmasi(){
	while true; do
		read -r -p "[#] Apakah Anda ingin menginstal zpct [Y/n]: " nanya
		if [[ "${nanya}" == "y" || "${nanya}" == "Y" ]]; then
			break
		elif [[ "${nanya}" == "n" || "${nanya}" == "N" ]]; then
			echo "[*] Semoga harimu menyenangkan ^_^"
			exit 0
		else
			echo "[-] Masukkan tidak valid."
			continue
		fi
	done
}

# Fungsi untuk mengecek koneksi internet
function cek_koneksi_internet(){
	if ! ping -c 4 google.com; then
		echo "[-] Anda tidak memiliki koneksi internet."
		exit 1
	fi
}

gagal=()

# Fungsi untuk menginstal dependesi yang diperlukan
function instal_dependensi(){
	daftar_dependensi=(
		"john"
		"john-data"
		"john-dbgsym"
		"hashcat"
		"hashcat-data"
		"hashcat-utils"
		"hashcat-utils-dbgsym"
		"zip"
		"unzip"
		"p7zip-full"
		"gcc"
		"make"
		"lsb-release"
		"wget"
		"gzip"
		"git"
		"fcrackzip"
		"cmake"
                "g++"
		"mingw-w64"
	)

	apt-get update

	if [[ $? -ne 0 ]]; then
		echo "[-] Repositori Linux gagal diperbarui."
		gagal+=("gagal")
	fi

	for instal_dependensi in "${daftar_dependensi[@]}"; do
		apt-get install "${instal_dependensi}"
		if [[ $? -ne 0 ]]; then
			gagal+=("${instal_dependensi}")
		fi
	done
}

# Fungsi untuk menginstal alat-alat yang diperlukan
function instal_tools(){
	daftar_tools=(
		"fixploit03/zpct"
		"fixploit03/zip2hashcat"
		"fixploit03/combinator"
		"fixploit03/toggle-case"
		"fixploit03/princeprocessor/"
		"kimci86/bkcrack"
	)

	target=/usr/local/bin/

	cd /opt

	for instal_tools in "${daftar_tools[@]}"; do
		git clone "https://github.com/${instal_tools}"

		if [[ $? -ne 0 ]]; then
			gagal+=("${instal_tools}")
		fi

		if [[ "${instal_tools}" == "${daftar_tools[0]}" ]]; then
			cd zpct
			source=zpct
	 		chmod +x "${source}"
			cp "${source}" "${target}"
		elif [[ "${instal_tools}" == "${daftar_tools[1]}" ]]; then
			cd zip2hashcat
			make
			cp zip2hashcat "${target}"
			cd ..
		elif [[ "${instal_tools}" == "${daftar_tools[2]}" ]]; then
			cd combinator
			make
			cp combinator "${target}"
			cd ..
		elif [[ "${instal_tools}" == "${daftar_tools[3]}" ]]; then
			cd toggle-case
			make
			cp toggle-case "${target}"
			cd ..
		elif [[ "${instal_tools}" == "${daftar_tools[4]}" ]]; then
			cd princeprocessor/src
			make
			cp pp64.bin "${target}/princeprocessor"
			cd ../../
		elif [[ "${instal_tools}" == "${daftar_tools[5]}" ]]; then
			cd bkcrack
			cmake -S . -B build -DCMAKE_INSTALL_PREFIX=install
			cmake --build build --config Release
			cmake --build build --config Release --target install
			ln -s /opt/zpct/bkcrack/install/bkcrack "${target}"
			cd ../
		fi
	done
}

function download_rockyou(){
	url_rockyou="https://github.com/praetorian-inc/Hob0Rules/raw/refs/heads/master/wordlists/rockyou.txt.gz"
	folder_wordlist="wordlists"
	rockyou="rockyou.txt.gz"

	if [[ ! -d "${folder_wordlist}" ]]; then
		mkdir "${folder_wordlist}"
	fi

	cd "${folder_wordlist}"

	wget "${url_rockyou}"

	if [[ $? -ne 0 ]]; then
		echo "[-] File Wordlist 'rockyou.txt' gagal didownload."
		gagal+=("gagal")
	fi

	gzip -d "${rockyou}"

	if [[ $? -ne 0 ]]; then
		echo "[-] File Wordlist 'rockyou.txt' gagal diekstrak."
		gagal+=("gagal")
	fi

	cd ..
}

# Fungsi untuk menginstal zpct
function cek_status_instal_zpct(){

	if [[ "${#gagal[@]}" -eq 0 ]]; then
		echo "[+] zpct berhasil diinstal."
		echo "[+] Untuk menjalankannya ketikkan 'zpct'"
		exit 0
	else
		echo "[-] zpct gagal diinstal."
		exit 1
	fi
}

# run script
cek_root
konfirmasi
cek_koneksi_internet
instal_dependensi
instal_tools
download_rockyou
cek_status_instal_zpct

