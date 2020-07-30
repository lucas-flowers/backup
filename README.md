
# Introduction

I use this super basic script to perform equally basic periodic backups of a
hard drive.

# Installation

Choose a location to place `backup.py`. For example, I cloned this repo
to `/opt/backup/`.

# Usage

Use `cron` to schedule running `backup.py` at an appropriate frequency. For
example, on the device I use this for, I have a file called `backup` in the
`/etc/cron.d/` directory with the following contents:

```
@monthly <USER> /opt/backup/backup.py <SOURCE> <DESTINATION>
```

