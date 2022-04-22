import os
from functools import partial
from pathlib import Path
import subprocess as sp
import lazycli
import pathlib
import tarfile

import collist

here = pathlib.Path().absolute()

script = lazycli.script()


class compose:
    __slots__ = "funcs", "first"

    def __init__(self, *funcs):
        self.first = funcs[-1]
        self.funcs = reversed(funcs[:-1])

    def __call__(self, *args, **kwargs):
        data = self.first(*args, **kwargs)
        for func in self.funcs:
            data = func(data)
        return data


def extract_setupfile(path: pathlib.Path = here):
    path = path.absolute()
    os.chdir(path)
    try:
        sp.run(["poetry", "build"], check=True)
        archive_name = sorted((path / "dist").glob("*.tar.gz"))[-1]
        with tarfile.open(archive_name) as archive:
            for filename in archive.getnames():
                if filename.endswith("/setup.py"):
                    break
            archive.extract(filename)

        extracted = pathlib.Path(filename)
        extracted.rename(path / "setup.py")
        extracted.parent.rmdir()
    finally:
        os.chdir(here)


def install_editable(repo, pip="pip"):
    sp.run(["git", "clone", "--recurse-submodules", repo], check=True)
    if repo.endswith(".git"):
        repo = repo[:-4]

    localrepo = pathlib.Path(repo.split("/")[-1])
    pyprojectfile = localrepo / "pyproject.toml"
    temp = pathlib.Path(str(pyprojectfile) + ".old")
    if pyprojectfile.exists():
        try:
            extract_setupfile(localrepo)
            pyprojectfile.rename(temp)
        except sp.CalledProcessError:
            pass

    sp.run([pip, "install", "-e", str(localrepo)], check=True)

    if temp.exists():
        temp.rename(pyprojectfile)


def install_remote(repo, pip="pip"):
    sp.run([pip, "install", "--upgrade", "git+" + repo], check=True)


def get_git_remote(path: Path):
    origin = Path().absolute()
    os.chdir(str(path))
    try:
        return sp.run(
            ["git", "config", "--get", "remote.origin.url"],
            check=True,
            stdout=sp.PIPE,
            universal_newlines=True,
        ).stdout.strip()
    except sp.CalledProcessError:
        return ""
    finally:
        os.chdir(str(origin))


def get_all_remotes():
    return set(get_git_remote(p) for p in Path().glob("*") if p.is_dir())


def classify_repos(repos):
    local_repos = get_all_remotes()
    local = local_repos.intersection(repos)
    remote = set(r for r in repos if r not in local_repos)
    return local, remote


select = compose(set, partial(map, int), str.split, input)


def get_repos(repofile: Path):
    with repofile.open() as fh:
        return fh.read().splitlines()


@script.subcommand
def install(repofile: Path, venv: Path = None):
    """Take the path of a file with an address of git repositories on each
    line. Gives the option to install directly from the repo or to clone the
    repo and install as editable.

    optionally, supply the name for a virtual environment that will be created
    where the packages will be installed.

    """
    if venv and not venv.exists():
        sp.run(["python", "-m", "venv", str(venv)], check=True)
    pip = str(venv / "bin" / "pip") if venv else "pip"
    sp.run([pip, "install", "--upgrade", "pip"])
    repos = get_repos(repofile)
    print(collist.collist({i: n for i, n in enumerate(repos)}))
    editable = select("which packages would you like to install for local editing? ")
    _, download = classify_repos(repos)
    for i, repo in enumerate(repos):
        if i in editable and repo in download:
            install_editable(repo, pip)
        else:
            install_remote(repo, pip)


@script.subcommand
def update(repofile: Path, venv: Path = None):
    """Take the path of a file with an address of git repositories on each
    line. This file should contain repos previously installed with `devinstall
    install`. This will update any files that are not installed locally.

    optionally, supply the name for a virtual environment where things are
    installed.
    """
    repos = get_repos(repofile)
    local, remote = classify_repos(repos)
    pip = str(venv / "bin" / "pip") if venv else "pip"
    sp.run([pip, "install", "--upgrade", "pip"])
    for repo in remote:
        install_remote(repo, pip)


if __name__ == "__main__":
    script.run()
