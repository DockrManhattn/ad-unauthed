import subprocess
import sys
import re
import threading
import os
import argparse

YELLOW = "\033[33m"
DARK_WHITE = "\033[2;37m"
BLUE = "\033[34m"
RESET = "\033[0m"

def print_informational(message):
    informational_msg = f"{YELLOW}{{🌀🌵[+]🌵🌀}}{RESET}"
    print(f"{informational_msg}{DARK_WHITE}{message}{RESET}")

def print_error(message):
    error_msg = f"{YELLOW}{{🔥💀💥[+]💥💀🔥}}{RESET}"
    print(f"{error_msg} {DARK_WHITE}{message}{RESET}")

def assign_ip_address_and_domain():
    parser = argparse.ArgumentParser(description="AD Enumeration Script")
    parser.add_argument("ip_address", help="The IP address of the target")
    parser.add_argument("-d", "--domain", help="The domain name (optional)")

    args = parser.parse_args()

    ip_address = args.ip_address
    domain = args.domain

    return ip_address, domain

def create_output_directory(ip_address):
    directory_name = f"ad-unauhed-{ip_address}"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    return directory_name

def run_nxc_ldap_command(ip_address, output_dir):
    command = f"nxc ldap {ip_address}"
    filename = os.path.join(output_dir, f"ad-unauhed-nxc-ldap-{ip_address}.txt")
    output = run_command_and_get_output(command)
    save_output_to_file(output, filename)
    return output

def run_lookupsid_command(ip_address, output_dir):
    command = f"lookupsid.py anonymous@{ip_address} -no-pass"
    print(f"\033[90mRunning command:\033[0m {command}")
    filename = os.path.join(output_dir, f"ad-unauhed-lookupsid-{ip_address}.txt")
    output = run_command_and_get_output(command)
    save_output_to_file(output, filename)
    extract_usernames(output, ip_address, output_dir)

def run_command_and_get_output(command):
    completed_process = subprocess.run(command, shell=True, capture_output=True, text=True)
    return completed_process.stdout

def save_output_to_file(output, filename):
    with open(filename, 'w') as file:
        file.write(output)

def extract_usernames(output, ip_address, output_dir):
    user_pattern = re.compile(r'\d+: \S+\\(\S+) \(SidTypeUser\)')
    matches = user_pattern.findall(output)
    if matches:
        usernames = '\n'.join(matches)
        usernames_filename = os.path.join(output_dir, f"ad-unauhed-Users-{ip_address}.txt")
        with open(usernames_filename, 'w') as file:
            file.write(usernames)

def extract_details_from_nxc_output(output):
    hostname_pattern = re.compile(r'name:([\w.]+)')
    domain_pattern = re.compile(r'domain:([\w.]+)')
    hostname_match = hostname_pattern.search(output)
    domain_match = domain_pattern.search(output)
    if hostname_match and domain_match:
        hostname = hostname_match.group(1)
        domain = domain_match.group(1)
        return hostname, domain
    else:
        return None, None

def extract_distinguished_name(nxc_output):
    _, domain = extract_details_from_nxc_output(nxc_output)
    if domain:
        parts = domain.split('.')
        dn_parts = [f"DC={part}" for part in parts]
        distinguished_name = ','.join(dn_parts)
        return distinguished_name
    else:
        return None

def run_ldap_search_queries(ip_address, distinguished_name, output_dir):
    base_query_command = f"ldapsearch -x -H ldap://{ip_address} -D '' -w '' -b '{distinguished_name}'"
    sam_query_command = f"{base_query_command} | grep sAMAccountName | awk -F: '{{ print $2 }}' | awk '{{ gsub(/ /,\" \"); print }}'"
    description_query_command = f"{base_query_command} | grep description"

    print(f"\033[90mRunning command:\033[0m {base_query_command}")
    print(f"\033[90mRunning command:\033[0m {sam_query_command}")
    print(f"\033[90mRunning command:\033[0m {description_query_command}")

    run_and_save_query_result(base_query_command, os.path.join(output_dir, f"ad-unauhed-ldapsearch-base-{ip_address}.txt"))
    run_and_save_query_result(sam_query_command, os.path.join(output_dir, f"ad-unauhed-ldapsearch-sam-{ip_address}.txt"))
    run_and_save_query_result(description_query_command, os.path.join(output_dir, f"ad-unauhed-ldapsearch-description-{ip_address}.txt"))

def run_and_save_query_result(command, filename):
    output = run_command_and_get_output(command)
    save_output_to_file(output, filename)

def run_rpcclient_command(ip_address, output_dir):
    command = f"rpcclient -W '' -c querydispinfo -U''%'' {ip_address}"
    print(f"\033[90mRunning command:\033[0m {command}")
    output = run_command_and_get_output(command)
    save_output_to_file(output, os.path.join(output_dir, f"ad-unauhed-rpcclient-querydispinfo-{ip_address}.txt"))

def run_nxc_user_enum(ip_address, output_dir):
    command = f"nxc smb {ip_address} -u anonymous -p '' --rid-brute 10000"
    print(f"\033[90mRunning command:\033[0m {command}")
    output = run_command_and_get_output(command)
    filtered_output = filter_sidtype_user(output)
    
    filename = os.path.join(output_dir, f"ad-unauhed-nxc-smb-{ip_address}.txt")
    with open(filename, 'w') as file:
        file.write(filtered_output)

    extract_and_append_users(filtered_output, ip_address, output_dir)

def filter_sidtype_user(output):
    lines = output.split('\n')
    filtered_lines = [line for line in lines if '(SidTypeUser)' in line]
    return '\n'.join(filtered_lines)

def extract_and_append_users(output, ip_address, output_dir):
    user_pattern = re.compile(r'\S+\\(\S+) \(SidTypeUser\)')
    matches = user_pattern.findall(output)
    if matches:
        unique_users = set(matches)
        filename = os.path.join(output_dir, f"ad-unauhed-Users-{ip_address}.txt")
        if os.path.exists(filename):
            with open(filename, "r") as users_file:
                existing_users = set(line.strip() for line in users_file)
        else:
            existing_users = set()
        with open(filename, "a") as users_file:
            for user in unique_users:
                if user.strip() not in existing_users:
                    users_file.write(user.strip() + '\n')

def run_enum4linux_command(ip_address, output_dir):
    command = f"enum4linux -A {ip_address} -u '' -p ''"
    print(f"\033[90mRunning command:\033[0m {command}")
    output = run_command_and_get_output(command)
    save_output_to_file(output, os.path.join(output_dir, f"ad-unauhed-enum4linux-{ip_address}.txt"))

def run_kerbrute_with_wordlist(domain, ip_address, output_dir):
    wordlists = [
        "jjsmith",
        "jjs",
        "johnjs",
        "john.smith",
        "johnsmith",
        "johns",
        "john",
        "jsmith",
        "smithjj",
        "smithj",
        "smith",
        "john.smith-at-example.com",
        "service-accounts",
        "test-accounts"
    ]

    print_informational("Do you want to further enumerate with a specific wordlist? (Y/N): ")
    response = input().strip().lower()

    if response not in ['y', 'yes']:
        sys.exit()  # Exit the program immediately

    print_informational("Select a wordlist:")
    for idx, wordlist in enumerate(wordlists, start=1):
        print(f"{idx}. {wordlist}")

    choice = input("Enter the number or the name of the wordlist: ").strip().lower()

    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(wordlists):
            selected_wordlist_name = wordlists[choice - 1]
            selected_wordlist = f"{selected_wordlist_name}.txt"
        else:
            print_error("Invalid choice. Exiting.")
            return
    elif choice in wordlists:
        selected_wordlist = f"{choice}.txt"
    else:
        print_error("Invalid choice. Exiting.")
        return
    wordlist_path = os.path.expanduser(f"~/.local/bin/wordlists/{selected_wordlist}")
    output_filename = os.path.join(output_dir, f"ad-unauhed-kerbrute-{selected_wordlist_name}-{ip_address}.txt")

    command = [
        "kerbrute",
        "userenum",
        "-d", domain,
        "--dc", ip_address,
        wordlist_path,
        "-t", "100"
    ]

    command_str = ' '.join(command)
    print(f"\033[90mRunning command:\033[0m {command_str}")
    
    with open(output_filename, "w") as output_file:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in process.stdout:
            print(line.strip())
            output_file.write(line)
        process.wait()

    print_informational(f"Kerbrute enumeration completed. Results saved to {output_filename}")

def main():
    ip_address, domain = assign_ip_address_and_domain()  # Get both IP and domain (if provided)

    output_dir = create_output_directory(ip_address)
    
    print_informational("Running lookupsid.py")
    run_lookupsid_command(ip_address, output_dir)
    
    nxc_thread = threading.Thread(target=run_nxc_ldap_command, args=(ip_address, output_dir))
    nxc_thread.start()
    nxc_thread.join()

    with open(os.path.join(output_dir, f"ad-unauhed-nxc-ldap-{ip_address}.txt")) as nxc_file:
        nxc_output = nxc_file.read()
    
    hostname, domain_from_nxc = extract_details_from_nxc_output(nxc_output)
    if domain is None:
        domain = domain_from_nxc
    
    if hostname and domain:
        distinguished_name = extract_distinguished_name(nxc_output)
        if distinguished_name:
            print_informational("Running ldapsearch queries")
            ldap_search_thread = threading.Thread(target=run_ldap_search_queries, args=(ip_address, distinguished_name, output_dir))
            ldap_search_thread.start()
        else:
            print_error("Failed to extract distinguished name.")
    else:
        print_error("Failed to extract hostname and domain from nxc output.")
    
    print_informational("Running nxc user enumeration")
    nxc_user_enum_thread = threading.Thread(target=run_nxc_user_enum, args=(ip_address, output_dir))
    nxc_user_enum_thread.start()
    
    print_informational("Running rpcclient")
    rpcclient_thread = threading.Thread(target=run_rpcclient_command, args=(ip_address, output_dir))
    rpcclient_thread.start()
    
    print_informational("Running enum4linux")
    enum4linux_thread = threading.Thread(target=run_enum4linux_command, args=(ip_address, output_dir))
    enum4linux_thread.start()

    ldap_search_thread.join()
    rpcclient_thread.join()
    nxc_user_enum_thread.join()
    enum4linux_thread.join()

    print_informational("Do you want to run kerbusers? (Y/N): ")
    response = input().strip().lower()
    if response in ['y', 'yes']:
        kerbusers_path = os.path.expanduser("~/.local/bin/kerbusers.py")
        kerbcommand = f"python3 {kerbusers_path} -d {domain} -dc-ip {ip_address}"
        print(f"\033[90mRunning command:\033[0m {kerbcommand}")

        subprocess.run(kerbcommand, shell=True)

        old_filename = "kerb-users-01.txt"
        new_filename = os.path.join(output_dir, f"ad-unauhed-kerbrute-users-{ip_address}.txt")
        if os.path.exists(old_filename):
            os.rename(old_filename, new_filename)
        else:
            print_error(f"{new_filename} not found.")

        run_kerbrute_with_wordlist(domain, ip_address, output_dir)
    else:
        print_informational("Skipping kerbusers enumeration.")

    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("")
