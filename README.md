# ZPCT

`ZPCT` (ZIP Password Cracker Tool) adalah script berbasis Bash yang dirancang untuk mengcrack kata sandi file ZIP.

## Persyaratan

- Sistem operasi Kali Linux
- Koneksi internet
- Kopi (Biar ga ngantuk ^_^)
  
## Cara Instal

> Hanya dapat diinstal di sistem operasi Kali Linux.

```
sudo /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/fixploit03/zpct/refs/heads/main/instal.sh)"
```

## Cara menjalankan 

Untuk menjalankan ZPCT ketikkan perintah dibawah ini:

```
zpct --help
```

Output 

```
root@localhost:~# zpct --help

ZPCT 2.1 - https://github.com/fixploit03/zpct/
Copyright (c) 2025 - Rofi (Fixploit03)

Penggunaan: zpct [OPSI]

Opsi:

--run           : Opsi untuk menjalankan script.
--update        : Opsi untuk memperbarui script.
--cracked-file  : Opsi untuk menampilkan seluruh file ZIP yang berhasil dicrack.
--uninstall     : Opsi untuk menguninstal script.
--help          : Opsi untuk menampilkan menu bantuan.
```

## Catatan Penting 

> Teknik konvensional (Tanpa file Hash) dan teknik KPA (Known Plaintext Attack) hanya bisa digunakan pada file ZIP yang memiliki enkripsi ZipCrypto.

## Credits

- [Fcrackzip](http://oldhome.schmorp.de/marc/fcrackzip.html)
- [John The Ripper](https://www.openwall.com/john/)
- [Hashcat](https://hashcat.net/hashcat/)
- [Bkcrack](https://github.com/kimci86/bkcrack)

## Lisensi

Dilisensikan dibawah [Lisensi MIT]().
