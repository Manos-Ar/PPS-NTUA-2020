# SSH File Sharing

### Local -> Scirouter (Without Proxy)
From the local machine, this command:
- If the directory on the remote machine does not exists:
  - It creates the directory and transfers all its contents.
- If the directory on the remote machine exists:
  - It transfers all its contents in the existing directory.

From the `src` directory on local to transfer the `src` directory on remote:
```
rsync -vr --delete --rsh "ssh parlab07@orion.cslab.ece.ntua.gr ssh" . parlab07@scirouter.cslab.ece.ntua.gr:/home/parallel/parlab07/a3/z1
```

### Scirouter -> Local (Without Proxy)
From the local machine, this command:
- If the directory on the local machine does not exists:
  - It creates the directory and transfers all its contents.
- If the directory on the local machine exists:
  - It transfers all its contents in the existing directory.

From the `3rd_exec` directory on local to transfer the `3rd_exec` directory on remote:
```
rsync -vr --rsh "ssh parlab07@orion.cslab.ece.ntua.gr ssh" parlab07@scirouter.cslab.ece.ntua.gr:/home/parallel/parlab07/a3/src/z1/ .
```

### Rsync Options

```
--delete = to delete everything old to the remote directory
```
### Compile All
```
qsub -q parlab make_on_queue.sh
```

### Run All
```
qsub -q serial -l nodes=sandman:ppn=64 run_on_queue.sh
```
