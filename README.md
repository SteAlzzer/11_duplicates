# Anti-Duplicator

Script helps to find identical files in folder.
Just give to it a folder and find out, how many files have a copy on your computer.

## How it works:
Use command line:
`python duplicates.py path_to_folder`.
As output:
```
[!] Найдены одинаковые файлы lang.csh в каталогах:
 C:\cygwin\etc\defaults\etc\profile.d
 C:\cygwin\etc\profile.d
```

## Just FYI:
Two files are identical if they have __same name__ and __same size__ in bytes.

## TODO:
- [ ] - Add comparison with checksums
- [ ] - Add search for files with identical checksums, but not names