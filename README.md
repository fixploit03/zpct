# ZPCT

`ZPCT` (ZIP Password Cracker Tool) adalah script Bash sederhana yang dirancang untuk mengcrack file ZIP.

## Fitur

- **Teknik Cracking**:
  
  - **Konvensional (Tanpa Hash)**
  - **Konvensional (Dengan Hash)**
  - **KPA (Known Plaintext Attack)**
    
- **Mode Serangan Canggih (untuk john dan hashcat)**:
  - Dictionary Attack
  - Brute Force Attack
  - Combinator Attack
  - Mask Attack
  - rince Attack
  - Hybrid Attack
  - Subsets Attack
  - Toggle Case Attack
    
 
- **Dukungan Enkripsi**:
  
  - ZipCrypto
  - AES (128/192/256-bit).
    
- **Output**: Hasil disimpan di `/opt/zpct/hasil_cracking/` dalam format `teks` dan `CSV`.
    
## Persyaratan

- **Sistem Operasi**: Kali Linux (script hanya kompatibel dengan Kali).
- **Hak Akse**s: Harus dijalankan sebagai root (`sudo`).
- **Koneksi Internet**: Diperlukan untuk instalasi awal.
- **Alat Pendukung**:
        `lsb_release`, `combinator`, `toggle-case`, `john`, `hashcat`, `zipinfo`, `7z`, `unzip`, `zip2hashcat`, `fcrackzip`, `bkcrack`.
- **Kopi**: Biar ga ngantuk saat cracking berjalan lama ^_^.
  
## Cara Instal

> Hanya dapat diinstal di sistem operasi Kali Linux.

Jalankan perintah berikut untuk menginstal ZPCT secara otomatis:

```
sudo /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/fixploit03/zpct/refs/heads/main/instal.sh)"
```

## Cara menjalankan 

Untuk menjalankan ZPCT ketikkan perintah dibawah ini:

```
zpct
```

## Catatan Penting 

- **Teknik Terbatas**: Teknik Konvensional (Tanpa Hash) dan teknik KPA (Known Plaintext Attack) hanya berfungsi pada file ZIP dengan enkripsi ZipCrypto. Untuk enkripsi AES, gunakan teknik dengan hash (`john` atau `hashcat`).
- **Teknik KPA (Known Plaintext Attack)**: Membutuhkan file plaintext yang sesuai dengan isi file ZIP.
- **Performa**: Kecepatan cracking tergantung pada kekuatan hardware (`CPU/GPU`) dan kompleksitas kata sandi.

  
## Credits

ZPCT dibangun dengan memanfaatkan alat-alat hebat berikut:

- [Fcrackzip](http://oldhome.schmorp.de/marc/fcrackzip.html)
- [John The Ripper](https://github.com/openwall/john)
- [Hashcat](https://github.com/hashcat/hashcat)
- [Bkcrack](https://github.com/kimci86/bkcrack)

Terima kasih kepada komunitas open-source yang telah mengembangkan alat-alat ini!

## Lisensi

Dilisensikan dibawah [Lisensi MIT]().

## Kontribusi

Ingin membantu? Silakan fork repo ini, tambahkan fitur, atau laporkan bug melalui issue atau pull request di GitHub!

## Dibuat dengan ❤️ dan ☕ oleh Rofi (Fixploit03). Selamat cracking! ^_^
