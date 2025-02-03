# ZPCT

![](https://github.com/fixploit03/zpct/blob/main/Screenshot_2025-02-02-14-25-54-409_tech.ula-edit.jpg)

ZPCT (ZIP Password Cracker Tool) adalah script berbasis Bash yang dirancang untuk mengcrack kata sandi file ZIP.

## Fitur

1. **Mudah digunakan** – Antarmuka berbasis terminal yang ramah pengguna.
2. **Mendukung berbagai jenis enkripsi file ZIP**:

    - ZipCrypto
    - AES-128
    - AES-192
    - AES-256

3. **Mendukung berbagai alat**:

    - Fcrackzip
    - John The Ripper
    - Hashcat
    - Bkcrack

4. **Mendukung berbagai teknik serangan**:

    1. **Konvensional (Tanpa file Hash)**:

       - Dictionary Attack
       - Brute Force Attack
         
    2. **Konvensional (Dengan file Hash)**:
   
       - Dictionary Attack
       - Brute Force Attack
       - Combinator Attack
       - Mask Attack
       - Prince Attack
       - Hybrid Attack
       - Subsets Attack
       - Toggle Case Attack
         
    3. **KPA (Known Plaintext Attack)**:
       
       - Brute Force Attack

5. Menyimpan hasil proses cracking untuk referensi lebih lanjut.
6. Error handling yang baik.

## Persyaratan

- Sistem operasi Kali Linux
- Koneksi internet
- Kopi (Biar ga ngantuk ^_^)
  
## Instal

> Pastikan Anda sudah berada dalam mode superuser (root) sebelum memulai proses instalasi.

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/fixploit03/zpct/refs/heads/main/instal.sh)"
```

> Hanya dapat diinstal di sistem operasi Kali Linux.

## Run

Untuk menjalankan ZPCT ketikkan perintah dibawah ini:

```
zpct
```

## Catatan

> Teknik konvensional (Tanpa file Hash) dan teknik KPA (Known Plaintext Attack) hanya bisa digunakan pada file ZIP yang memiliki enkripsi ZipCrypto.

## Lisensi

Dilisensikan dibawah [Lisensi MIT]().
