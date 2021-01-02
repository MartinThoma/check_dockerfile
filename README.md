# check_dockerfile

`check_dockerfile` is a static Dockerfile security vulnerability scannner (SAST).

## Installation

```
$ git clone https://github.com/MartinThoma/check_dockerfile.git && cd check_dockerfile
$ pip install -e .
```

## Usage

```
$ check_dockerfile --help
Usage: check_dockerfile [OPTIONS] DOCKERFILE

  Check a dockerfile for issues.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.
```

Running it:

```
$ check_dockerfile tests/examples/mritd/Dockerfile.rssbot
Use a trusted base image: alpine:3.12 ✔️
All checks are ok
```
