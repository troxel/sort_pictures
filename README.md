# Synopsis

usage: sort_pictures.py [-h] [-r] [-c] [-s] [-t] [-v] [-ym] [-ymd]
                        dir_src dir_dest

Sort jpgs

positional arguments:
  dir_src           source directory
  dir_dest          destination directory

optional arguments:
  -h, --help        show this help message and exit
  -r, --recursive   search dir_src recursively
  -c, --copy        copy files instead of move
  -s, --silent      don't display parsing details.
  -t, --test        run a test. files will not be moved/copied instead you
                    will just a list of would happen
  -v, --verbose     Verbose
  -ym, --yyyymm     Layout YYYY/MM
  -ymd, --yyyymmdd  Layout YYYY/MM_DD

