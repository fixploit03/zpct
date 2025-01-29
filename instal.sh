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
	)

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
		"hashstation/zip2hashcat"
		"fixploit03/combinator"
		"fixploit03/toggle-case"
		"hashcat/princeprocessor/"
	)

	target=/usr/local/bin/

	for instal_tools in "${daftar_tools[@]}"; do
		git clone "https://github.com/${instal_tools}"

		if [[ $? -ne 0 ]]; then
			gagal+=("${instal_tools}")
		fi

		if [[ "${instal_tools}" == "${daftar_tools[0]}" ]]; then
			cd zip2hashcat
			make
			cp zip2hashcat "${target}"
			cd ..
		elif [[ "${instal_tools}" == "${daftar_tools[1]}" ]]; then
			cd combinator
			make
			cp combinator "${target}"
			cd ..
		elif [[ "${instal_tools}" == "${daftar_tools[2]}" ]]; then
			cd toggle-case
			make
			cp toggle-case "${target}"
			cd ..
		elif [[ "${instal_tools}" == "${daftar_tools[3]}" ]]; then
			cd princeprocessor/src
			make
			cp pp64.bin "${target}/princeprocessor"
			cd ../../
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
		exit 1
	fi

	gzip -d "${rockyou}"

	if [[ $? -ne 0 ]]; then
		echo "[-] File Wordlist 'rockyou.txt' gagal diekstrak."
		exit 1
	fi

	cd ..
}

# Fungsi untuk menginstal zpct
function instal_zpct(){

	target=/usr/local/bin

	source=zpct

 	chmod +x "${source}"
	cp "${source}" "${target}"

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
instal_zpct

