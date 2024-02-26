# updates the version number in the __about__.py file
import subprocess


def update_version(version_type):
    with open("src/api/__about__.py", "r") as f:
        version = f.read().split("=")[1].replace('"', "").strip()
        patch_version = version.split(".")[2]
        minor_version = version.split(".")[1]
        major_version = version.split(".")[0]
        if version_type == "major":
            major_version = str(int(major_version) + 1)
            minor_version = "0"
            patch_version = "0"
        elif version_type == "minor":
            minor_version = str(int(minor_version) + 1)
            patch_version = "0"
        elif version_type == "patch":
            patch_version = str(int(patch_version) + 1)
        else:
            raise ValueError("Invalid version type. Please use major, minor, or patch.")
        with open("src/api/__about__.py", "w") as f:
            new_version = f"{major_version}.{minor_version}.{patch_version}"
            f.write(f'__version__ = "{new_version}"\n')
            return f"v{new_version}"


# passes the command line argument to the function
if __name__ == "__main__":
    import sys

    new_version = update_version(sys.argv[1])
    message = input(f"Version updated to {new_version}. Enter commit message: \n")
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", message.strip()])
    subprocess.run(["git", "push"])
    subprocess.run(["git", "tag", "-a", new_version, "-m", new_version])
    subprocess.run(["git", "push", "origin", new_version])
