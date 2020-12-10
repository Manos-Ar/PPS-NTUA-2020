# SSH File Sharing

### Local -> Scirouter (Without Proxy)
From the local machine, this command:
- If the directory on the remote machine does not exists:
  - It creates the directory and transfers all its contents.
- If the directory on the remote machine exists:
  - It transfers all its contents in the existing directory.

From the `2nd_exec` directory on local to transfer the `2nd_exec` directory on remote:
```
rsync -vr --delete --rsh "ssh parlab07@orion.cslab.ece.ntua.gr ssh" . parlab07@scirouter.cslab.ece.ntua.gr:/home/parallel/parlab07/a2/
```

### Scirouter -> Local (Without Proxy)
From the local machine, this command:
- If the directory on the local machine does not exists:
  - It creates the directory and transfers all its contents.
- If the directory on the local machine exists:
  - It transfers all its contents in the existing directory.

From the `2nd_exec` directory on local to transfer the `2nd_exec` directory on remote:
```
rsync -vr --rsh "ssh parlab07@orion.cslab.ece.ntua.gr ssh" parlab07@scirouter.cslab.ece.ntua.gr:/home/parallel/parlab07/a2/ .
```

### Rsync Options

```
--delete = to delete everything old to the remote directory
```
### MPI compile and run
```
mpicc -O3 -Wall test_mpi.c
```
```
mpirun -n 4 ./test_mpi.out
```

### Compile All
```
qsub -q parlab make_on_queue.sh
```

### Run All
```
qsub -q parlab run_on_queue.sh
```
