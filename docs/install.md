# Installation

## Using a container (Docker, Podman..)

Pull the image (adapt the version number with the latest release).

```bash
podman pull ghcr.io/wivik/pyp-boy:v0.4.2
```

Run the container, using a volume for the /pypboy/data directory inside the container (because it stores your save file).

```bash
podman run --rm -v <somepath>:/pypboy/data -p 5000:5000 ghcr.io/wivik/pyp-boy:v0.4.2
```

Open your browser to http://localhost:5000 and enjoy.

## Using source code

Clone the repository.

Install requirements :

```bash
pip install --user requirements.txt
```

Run flask

```bash
python -m flask run
```

Open your browser to http://localhost:5000