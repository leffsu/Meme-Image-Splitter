Meme Image Splitter
=====

How do I use Meme Image Splitter?
-------------------



```Bash
Usage: splitter.py [options]

Options:
  -h, --help            show this help message and exit
  -p PATH, --path=PATH  path to file
  -i INITIAL_NAME, --initial_name=INITIAL_NAME
                        initial name
  -t TARGET_NAME, --target_name=TARGET_NAME
                        target name
  -o ORIENTATION, --orientation=ORIENTATION
                        orientation
```
PATH, INITIAL_NAME, TARGET_NAME are mandatory.

ORIENTATION is optional. By default it will cut vertically.

```Bash
python splitter.py -p pathToFile -i initialName -t targetName
```

For example:
```Bash
python splitter.py -p '/Users/leff/original.png' -i lev -t vel
python splitter.py -p '/Users/leff/original.png' -i lev -t vel -o h
```

Dependencies
-------------

 * Pillow

Getting Help
------------
To report a specific problem or feature request, open a new issue on Github. For questions, suggestions, or
anything else, email me at leff@leff.su or ping me on Telegram t.me/leffsu.

Author
------
Lev Nazarov - @leffsu on GitHub, @leffsu on Telegram

License
-------
Apache 2.0