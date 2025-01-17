# ad-unauthed
This repo hosts the script and setup file ad-unauthed.

# Installation
```bash
python3 setup.py
```

# Usage
```bash
ad-unauthed $IP
```

# Example
```bash

┌─[kali@parrot]─[~/hybrid]
└──╼ $export IP='10.10.173.37'
┌─[kali@parrot]─[~/hybrid]
└──╼ $ad-unauthed $IP
{🌀🌵[+]🌵🌀}Running lookupsid.py
{🌀🌵[+]🌵🌀}Running ldapsearch queries
{🌀🌵[+]🌵🌀}Running nxc user enumeration
{🌀🌵[+]🌵🌀}Running rpcclient
{🌀🌵[+]🌵🌀}Running enum4linux
{🌀🌵[+]🌵🌀}Do you want to run kerbusers? (Y/N):
y

    __             __               __
   / /_____  _____/ /_  _______  __/ /____
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/

Version: v1.0.3 (9dad6e1) - 01/16/25 - Ronnie Flathers @ropnop

2025/01/16 22:02:54 >  Using KDC(s):
2025/01/16 22:02:54 >  	10.10.173.37:88

2025/01/16 22:02:55 >  [+] VALID USERNAME:	 administrator@hybrid.vl
2025/01/16 22:02:56 >  [+] VALID USERNAME:	 ADMINISTRATOR@hybrid.vl
2025/01/16 22:02:56 >  [+] VALID USERNAME:	 Administrator@hybrid.vl
2025/01/16 22:03:23 >  [+] VALID USERNAME:	 pamela.smith@hybrid.vl
2025/01/16 22:06:39 >  [+] VALID USERNAME:	 emily.white@hybrid.vl
2025/01/16 22:06:44 >  [+] VALID USERNAME:	 olivia.smith@hybrid.vl
2025/01/16 22:07:21 >  [+] VALID USERNAME:	 josh.mitchell@hybrid.vl
2025/01/16 22:11:25 >  [+] VALID USERNAME:	 edward.miller@hybrid.vl
2025/01/16 22:14:26 >  [+] VALID USERNAME:	 peter.turner@hybrid.vl
2025/01/16 22:27:30 >  [+] VALID USERNAME:	 kathleen.walker@hybrid.vl
2025/01/16 22:46:34 >  [+] VALID USERNAME:	 ricky.myers@hybrid.vl
2025/01/16 22:53:51 >  Done! Tested 963050 usernames (11 valid) in 3056.946 seconds
{🌀🌵[+]🌵🌀}Renamed kerb-users-01.txt to AD-Unauthed-10.10.173.37/AD-Unauthed-kerbrute-users-10.10.173.37.txt
{🌀🌵[+]🌵🌀}Do you want to further enumerate with a specific wordlist? (Y/N):
y
{🌀🌵[+]🌵🌀}Select a wordlist:
1. jjsmith
2. jjs
3. johnjs
4. john.smith
5. johnsmith
6. johns
7. john
8. jsmith
9. smithjj
10. smithj
11. smith
12. john.smith-at-example.com
13. service-accounts
14. test-accounts
Enter the number or the name of the wordlist: 14

__             __               __
/ /_____  _____/ /_  _______  __/ /____
/ //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
/ ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/

Version: v1.0.3 (9dad6e1) - 01/16/25 - Ronnie Flathers @ropnop

2025/01/16 22:54:29 >  Using KDC(s):
2025/01/16 22:54:29 >  	10.10.173.37:88

2025/01/16 22:54:30 >  Done! Tested 689 usernames (0 valid) in 0.977 seconds
{🌀🌵[+]🌵🌀}Kerbrute enumeration completed. Results saved to AD-Unauthed-10.10.173.37/AD-Unauthed-kerbrute-test-accounts-10.10.173.37.txt
```
