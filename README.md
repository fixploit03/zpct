# ZPCT

![](https://github.com/fixploit03/zpct/blob/main/img/zpct.jpg)

`ZPCT` (ZIP Password Cracker Tool) adalah script berbasis Bash yang dirancang untuk mengcrack kata sandi file ZIP.

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
  
## Cara Instal

> Hanya dapat diinstal di sistem operasi Kali Linux.

```
sudo /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/fixploit03/zpct/refs/heads/main/instal.sh)"
```

## Cara menjalankan 

Untuk menjalankan ZPCT ketikkan perintah dibawah ini:

```
zpct
```

ikuti instruksi yang ditampilkan di menu. 

## Hasil Proses Cracking 

Untuk file ZIP yang berhasil dicrack, hasilnya disimpan dalam file `.txt`. Sementara itu, semua file ZIP yang pernah dicrack disimpan dalam file `cracked.csv`. Kedua file tersebut berada di folder `/opt/zpct/hasil_cracking`.

Berikut adalah contoh isi dari masing-masing file:

![](https://github.com/fixploit03/zpct/blob/main/img/cracked_txt.png)

<p align="center">
    [ Sample File TXT ]
</p>

![](https://github.com/fixploit03/zpct/blob/main/img/cracked.png)

<p align="center">
    [ Sample File CSV ]
</p>


## Catatan Penting 

> Teknik konvensional (Tanpa file Hash) dan teknik KPA (Known Plaintext Attack) hanya bisa digunakan pada file ZIP yang memiliki enkripsi ZipCrypto.

## Credits

- [Fcrackzip](http://oldhome.schmorp.de/marc/fcrackzip.html)
- [John The Ripper](https://www.openwall.com/john/)
- [Hashcat](https://hashcat.net/hashcat/)
- [Bkcrack](https://github.com/kimci86/bkcrack)

## Lisensi

Dilisensikan dibawah [Lisensi MIT]().
