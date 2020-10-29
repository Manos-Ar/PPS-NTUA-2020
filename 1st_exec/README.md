# SSH File Sharing

### Local -> Scirouter (Without Proxy)
From the local machine, this command:
- If the directory on the remote machine does not exists:
  - It creates the directory and transfers all its contents.
- If the directory on the remote machine exists:
  - It transfers all its contents in the existing directory.

```
rsync -vr --rsh "ssh parlab07@orion.cslab.ece.ntua.gr ssh" src/ parlab07@scirouter.cslab.ece.ntua.gr:/home/parallel/parlab07/a1/src
```

### Scirouter -> Local (Without Proxy)
From the local machine, this command:
- If the directory on the local machine does not exists:
  - It creates the directory and transfers all its contents.
- If the directory on the local machine exists:
  - It transfers all its contents in the existing directory.

```
rsync -vr --rsh "ssh parlab07@orion.cslab.ece.ntua.gr ssh" parlab07@scirouter.cslab.ece.ntua.gr:/home/parallel/parlab07/a1/src .
```
