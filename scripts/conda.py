import subprocess


def conda_search(package):
    result = subprocess.run(
        ["conda", "search", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return result.returncode == 0


def generate_environment_yml(requirements_path, output_path):
    with open(requirements_path, "r") as f:
        packages = f.readlines()

    conda_packages = []
    pip_packages = []
    for package in packages:
        package_name = package.split("==")[0].strip()
        if conda_search(package_name):
            conda_packages.append(package.strip())
        else:
            pip_packages.append(package.strip())

    with open(output_path, "w") as f:
        f.write("name: myenv\n")
        f.write("channels:\n  - defaults\n  - conda-forge\n")
        f.write("dependencies:\n")
        for package in conda_packages:
            f.write(f"  - {package}\n")
        if pip_packages:
            f.write("  - pip\n  - pip:\n")
            for package in pip_packages:
                f.write(f"    - {package}\n")


# Usage
generate_environment_yml("requirements.txt", "environment.yml")
