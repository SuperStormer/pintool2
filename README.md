# Pintool

This tool can be useful for solving some reversing challenges in CTFs events. Implements the technique described here:

-   http://shell-storm.org/blog/A-binary-analysis-count-me-if-you-can/

Original: https://github.com/wagiro/pintool

### Configuration

Download pin from [the Intel website](https://www.intel.com/content/www/us/en/developer/articles/tool/pin-a-binary-instrumentation-tool-downloads.html), extract the archive, and run the following:

```sh
cd source/tools/ManualExamples
make obj-intel64/inscount0.so TARGET=intel64
make obj-ia32/inscount0.so TARGET=ia32
```

You should configure your pin path inside of `pintool/pin.py` if it is different from the default:

```py
PIN = Path("/opt/pin/pin").expanduser()
INSCOUNT32 = Path("/opt/pin/source/tools/ManualExamples/obj-ia32/inscount0.so").expanduser()
INSCOUNT64 = Path("/opt/pin/source/tools/ManualExamples/obj-intel64/inscount0.so").expanduser()
```

### Help

```
$ pintool
usage: pintool [-h] [-d] [-l LEN] [-c CHARSET] [-b CHARACTERS] [-a {32,64}] [-i INIT_PASS] [-s SYMBOL] [-e EXPRESSION] [-r] [-u] [-g]
                   filename [additional_args ...]

Program for playing with Pin

positional arguments:
  filename
  additional_args

options:
  -h, --help            show this help message and exit
  -d, --detect          Detect the password length. For example -d -l 40, with 40 characters
  -l LEN                Length of password
  -c CHARSET, --charset CHARSET
                        Charset definition for brute force (default, default2, lower, upper, digit, hex, punct, print)
  -b CHARACTERS, --chars CHARACTERS, --characters CHARACTERS
                        Add characters for the charset. For example, -b _-
  -a {32,64}, --arch {32,64}
                        Program architecture
  -i INIT_PASS, --init INIT_PASS, --init-pass INIT_PASS
                        Initial password characters. For example, -i CTF{
  -s SYMBOL, --symbol SYMBOL
                        Symbol used as password placeholder
  -e EXPRESSION, --expression EXPRESSION
                        Difference between instructions that are successful or not. For example: -e '== -12', -e '=> 900', -e '<= 17' or -e '!=
                        32'
  -r, --reverse         Reverse order, bruteforcing starting from the last character
  -u, --unordered, --non-ascending
                        Target program doesn't check chars in ascending order
  -g, --argv            Pass argument via command-line arguments instead of stdin.
```

### Examples

**Baleful - picoCTF 2014**

```sh
$ pintool --arch 32 -l 30 -e '== -12' examples/baleful
p----------------------------- = 763799 difference -12 instructions
pa---------------------------- = 763787 difference -12 instructions
pac--------------------------- = 763775 difference -12 instructions
pack-------------------------- = 763763 difference -12 instructions
packe------------------------- = 763751 difference -12 instructions
packer------------------------ = 763739 difference -12 instructions
packers----------------------- = 763727 difference -12 instructions
packers_---------------------- = 763715 difference -12 instructions
packers_a--------------------- = 763703 difference -12 instructions
packers_an-------------------- = 763691 difference -12 instructions
packers_and------------------- = 763679 difference -12 instructions
packers_and_------------------ = 763667 difference -12 instructions
packers_and_v----------------- = 763655 difference -12 instructions
packers_and_vm---------------- = 763643 difference -12 instructions
packers_and_vms--------------- = 763631 difference -12 instructions
packers_and_vms_-------------- = 763619 difference -12 instructions
packers_and_vms_a------------- = 763607 difference -12 instructions
packers_and_vms_an------------ = 763595 difference -12 instructions
packers_and_vms_and----------- = 763583 difference -12 instructions
packers_and_vms_and_---------- = 763571 difference -12 instructions
packers_and_vms_and_x--------- = 763559 difference -12 instructions
packers_and_vms_and_xo-------- = 763547 difference -12 instructions
packers_and_vms_and_xor------- = 763535 difference -12 instructions
packers_and_vms_and_xors------ = 763523 difference -12 instructions
packers_and_vms_and_xors_----- = 763511 difference -12 instructions
packers_and_vms_and_xors_o---- = 763499 difference -12 instructions
packers_and_vms_and_xors_oh--- = 763487 difference -12 instructions
packers_and_vms_and_xors_oh_-- = 763475 difference -12 instructions
packers_and_vms_and_xors_oh_m- = 763463 difference -12 instructions
packers_and_vms_and_xors_oh_my = 763463 difference -12 instructions
packers_and_vms_and_xors_oh_my
```

**Reverse 400 - Hack You 2014**

```sh
$ pintool --arch 32 -l 37 -c hex -i CTF{ -b }_ -e '>= 900' examples/reverse400
CTF{c________________________________ = 1057174 difference 1300 instructions
CTF{c9_______________________________ = 1058474 difference 1300 instructions
CTF{c9f______________________________ = 1059774 difference 1300 instructions
CTF{c9fd_____________________________ = 1061074 difference 1300 instructions
CTF{c9fd9____________________________ = 1062374 difference 1300 instructions
CTF{c9fd99___________________________ = 1063674 difference 1300 instructions
CTF{c9fd99d__________________________ = 1064974 difference 1300 instructions
CTF{c9fd99de_________________________ = 1066274 difference 1300 instructions
CTF{c9fd99de8________________________ = 1067574 difference 1300 instructions
CTF{c9fd99de8e_______________________ = 1068874 difference 1300 instructions
CTF{c9fd99de8eb______________________ = 1070174 difference 1300 instructions
CTF{c9fd99de8eb0_____________________ = 1071474 difference 1300 instructions
CTF{c9fd99de8eb08____________________ = 1072774 difference 1300 instructions
CTF{c9fd99de8eb082___________________ = 1074074 difference 1300 instructions
CTF{c9fd99de8eb082c__________________ = 1075374 difference 1300 instructions
CTF{c9fd99de8eb082c6_________________ = 1076674 difference 1300 instructions
CTF{c9fd99de8eb082c66________________ = 1077974 difference 1300 instructions
CTF{c9fd99de8eb082c66c_______________ = 1079274 difference 1300 instructions
CTF{c9fd99de8eb082c66c4______________ = 1080574 difference 1300 instructions
CTF{c9fd99de8eb082c66c4c_____________ = 1081874 difference 1300 instructions
CTF{c9fd99de8eb082c66c4ce____________ = 1083174 difference 1300 instructions
CTF{c9fd99de8eb082c66c4ce4___________ = 1084474 difference 1300 instructions
CTF{c9fd99de8eb082c66c4ce40__________ = 1085774 difference 1300 instructions
CTF{c9fd99de8eb082c66c4ce403_________ = 1087074 difference 1300 instructions
CTF{c9fd99de8eb082c66c4ce4039________ = 1088374 difference 1300 instructions
CTF{c9fd99de8eb082c66c4ce4039f19c____ = 1093574 difference 1300 instructions
CTF{c9fd99de8eb082c66c4ce4039f19c4___ = 1094874 difference 1300 instructions
CTF{c9fd99de8eb082c66c4ce4039f19c4f__ = 1096174 difference 1300 instructions
CTF{c9fd99de8eb082c66c4ce4039f19c4fc_ = 1097474 difference 1300 instructions
CTF{c9fd99de8eb082c66c4ce4039f19c4fc} = 1098391 difference 917 instructions
CTF{c9fd99de8eb082c66c4ce4039f19c4fc}
```

**wyvern 500 - CSAW CTF 2015**

```sh
$ pintool -l 28 -e '> 200' examples/wyvern
d--------------------------- = 1505212 difference 10332 instructions
dr-------------------------- = 1515830 difference 10618 instructions
dr4------------------------- = 1521965 difference 6135 instructions
dr4g------------------------ = 1533160 difference 11195 instructions
dr4g0----------------------- = 1539867 difference 6707 instructions
dr4g0n---------------------- = 1546952 difference 7085 instructions
dr4g0n_--------------------- = 1554227 difference 7275 instructions
dr4g0n_o-------------------- = 1566566 difference 12339 instructions
dr4g0n_or------------------- = 1574413 difference 7847 instructions
dr4g0n_or_------------------ = 1582638 difference 8225 instructions
dr4g0n_or_p----------------- = 1591053 difference 8415 instructions
dr4g0n_or_p4---------------- = 1599752 difference 8699 instructions
dr4g0n_or_p4t--------------- = 1608735 difference 8983 instructions
dr4g0n_or_p4tr-------------- = 1618098 difference 9363 instructions
dr4g0n_or_p4tri------------- = 1627651 difference 9553 instructions
dr4g0n_or_p4tric------------ = 1642776 difference 15125 instructions
dr4g0n_or_p4tric1----------- = 1652899 difference 10123 instructions
dr4g0n_or_p4tric1a---------- = 1663001 difference 10102 instructions
dr4g0n_or_p4tric1an--------- = 1673709 difference 10708 instructions
dr4g0n_or_p4tric1an_-------- = 1684701 difference 10992 instructions
dr4g0n_or_p4tric1an_i------- = 1695977 difference 11276 instructions
dr4g0n_or_p4tric1an_it------ = 1707626 difference 11649 instructions
dr4g0n_or_p4tric1an_it5----- = 1719474 difference 11848 instructions
dr4g0n_or_p4tric1an_it5_---- = 1731606 difference 12132 instructions
dr4g0n_or_p4tric1an_it5_L--- = 1744022 difference 12416 instructions
dr4g0n_or_p4tric1an_it5_LL-- = 1756811 difference 12789 instructions
dr4g0n_or_p4tric1an_it5_LLV- = 1769799 difference 12988 instructions
dr4g0n_or_p4tric1an_it5_LLVM = 1785242 difference 15443 instructions
dr4g0n_or_p4tric1an_it5_LLVM
```
