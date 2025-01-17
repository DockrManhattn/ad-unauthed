import os
import shutil
import subprocess

def get_current_user():
    return os.getlogin()

def create_directory():
    user = get_current_user()
    dir_path = f"/home/{user}/.local/bin"
    os.makedirs(dir_path, exist_ok=True)
    print(f"Directory created at: {dir_path}")

def clone_repository():
    # Define the repository URLs and their respective directories
    repos = [
        ("https://github.com/DockrManhattn/kerbusers.git", "kerbusers"),
        ("https://github.com/ropnop/windapsearch.git", "windapsearch"),
    ]

    # Loop through each repo, check if the directory exists, and clone it
    for repo_url, repo_dir in repos:
        if os.path.exists(repo_dir):
            print(f"Directory '{repo_dir}' already exists. Removing it.")
            shutil.rmtree(repo_dir)

        subprocess.run(["git", "clone", repo_url], check=True)
        print(f"Repository cloned successfully: {repo_url}")

    # After cloning, copy windapsearch.py to /home/{user}/.local/bin
    windapsearch_file = os.path.join("windapsearch", "windapsearch.py")
    user_dir = f"/home/{get_current_user()}/.local/bin"
    shutil.copy(windapsearch_file, user_dir)
    print(f"Copied windapsearch.py to {user_dir}")

def run_setup_in_kerbusers():
    os.chdir("kerbusers")
    subprocess.run(["python3", "setup.py"], check=True)
    print("Setup script inside 'kerbusers' executed successfully.")

def install_package(package):
    try:
        if package == 'pipx':
            subprocess.run(["pip3", "install", "--break-system-packages", "pipx"], check=True)
            print(f"Package {package} installed successfully.")
        elif package == 'python-ldap':
            # Install python-ldap using pip3 with --break-system-packages flag
            subprocess.run(["pip3", "install", "--break-system-packages", "python-ldap"], check=True)
            print(f"Package {package} installed successfully via pip.")
        else:
            subprocess.run(["pip3", "install", "--break-system-packages", package], check=True)
            print(f"Package {package} installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package}. Error: {e}")

def install_required_packages():
    packages = [
        'impacket',
        'ldap3',
        'bloodhound',
        'requests',
        'pywerview',
        'pipx',
    ]
    for package in packages:
        install_package(package)

def copy_ad_unauthed():
    # Define the absolute path for ad-unauthed.py in the starting directory
    ad_unauthed_source = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ad-unauthed.py")
    user_dir = f"/home/{get_current_user()}/.local/bin"

    # Ensure the destination directory exists
    os.makedirs(user_dir, exist_ok=True)

    # Copy the ad-unauthed.py file
    shutil.copy(ad_unauthed_source, user_dir)
    print(f"Copied ad-unauthed.py to {user_dir}")
    
def add_to_path():
    path_to_add = '/home/kali/.local/bin'

    # Check the user's current shell and modify the appropriate configuration file
    current_shell = os.environ.get('SHELL', '')

    if 'zsh' in current_shell:
        config_file = os.path.expanduser('~/.zshrc')
        shell_file = '.zshrc'
    elif 'bash' in current_shell:
        config_file = os.path.expanduser('~/.bashrc')
        shell_file = '.bashrc'
    else:
        print(f"Unsupported shell: {current_shell}. PATH not updated.")
        return

    # Append the export statement and alias to the appropriate file
    with open(config_file, 'a') as file:
        file.write(f'\nexport PATH="$PATH:{path_to_add}"\n')
        file.write(f'alias ad-unauthed="python3 /home/{get_current_user()}/.local/bin/ad-unauthed.py"\n')
    print(f"Added to PATH and alias in {config_file}.")

    # Print the reminder message and the source command in colored format
    print(f"\033[0mBe sure to source your {shell_file} file.")  # White text
    print(f"\033[1;32m    source /home/{get_current_user()}/{shell_file}\033[0m")  # Indented green text

if __name__ == "__main__":
    create_directory()
    clone_repository()
    run_setup_in_kerbusers()
    install_required_packages()
    copy_ad_unauthed()
    add_to_path()
