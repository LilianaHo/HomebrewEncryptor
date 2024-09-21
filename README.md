# HomebrewEncryptor
A terminal-based program that compresses and encrypts .txt data

## Linux
### Requirements
1. python3. To install type the following in the terminal:
```sh
sudo apt install python3
```

### Instructions
1. Make sure you have installed python3
2. Download the files on this github. Prepare a file to encrypt as well as a password file. Both of which must be textfiles of a single line.
4. Open terminal on the downloaded folder
5. To encrypt type in terminal: 
```sh
python3 ./encryptor.py [file_to_encrypt.txt] [password_file.txt] [file_to_decrypt.bin]
```
5. To decrypt type in terminal: 
```sh
python3 ./decryptor.py [file_to_decrypt.bin] [password_file.txt] [output_name.txt]
```
