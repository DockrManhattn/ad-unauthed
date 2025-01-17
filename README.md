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

```bash
┌─[kali@parrot]─[~/hybrid]
└──╼ $ls -lahR AD-Unauthed-10.10.173.37/
AD-Unauthed-10.10.173.37/:
total 24K
drwxr-xr-x 1 kali kali  868 Jan 16 22:54 .
drwxr-xr-x 1 kali kali   48 Jan 16 22:53 ..
-rw-r--r-- 1 kali kali 1.2K Jan 16 22:02 AD-Unauthed-enum4linux-10.10.173.37.txt
-rw-r--r-- 1 kali kali  492 Jan 16 22:54 AD-Unauthed-kerbrute-test-accounts-10.10.173.37.txt
-rw-r--r-- 1 kali kali 1.4K Jan 16 22:53 AD-Unauthed-kerbrute-users-10.10.173.37.txt
-rw-r--r-- 1 kali kali  346 Jan 16 22:02 AD-Unauthed-ldapsearch-base-10.10.173.37.txt
-rw-r--r-- 1 kali kali    0 Jan 16 22:02 AD-Unauthed-ldapsearch-description-10.10.173.37.txt
-rw-r--r-- 1 kali kali    0 Jan 16 22:02 AD-Unauthed-ldapsearch-sam-10.10.173.37.txt
-rw-r--r-- 1 kali kali    0 Jan 16 22:02 AD-Unauthed-lookupsid-10.10.173.37.txt
-rw-r--r-- 1 kali kali  165 Jan 16 22:02 AD-Unauthed-nxc-ldap-10.10.173.37.txt
-rw-r--r-- 1 kali kali    0 Jan 16 22:02 AD-Unauthed-nxc-smb-10.10.173.37.txt
-rw-r--r-- 1 kali kali   35 Jan 16 22:02 AD-Unauthed-rpcclient-querydispinfo-10.10.173.37.txt
```
