# Parallel-NTUA-2020
This repository contains the exercises and their solutions for the Parallel Systems NTUA course of 2020-2021.  

# SSH Connections
## Local -> Orion -> Scirouter (With Proxy)
### Local -> Orion
Connect:
```
ssh parlab07@orion.cslab.ece.ntua.gr
```

### Orion -> Scirouter
```
ssh parlab07@scirouter.cslab.ece.ntua.gr
```

## Local -> Scirouter (Without Proxy)
### With ssh command
A way to connect directly from local machine to Scirouter, using:
- `-A`: to enable agent forwarding
- `-t`: to force a pseudo-tty to be allocated

```
ssh -A -t parlab07@orion.cslab.ece.ntua.gr ssh -A -t parlab07@scirouter.cslab.ece.ntua.gr
```

To add an alias in your `.bashrc` or `.zshrc` add at the end:
```
alias ssh-scirouter="ssh -A -t parlab07@orion.cslab.ece.ntua.gr ssh -A -t parlab07@scirouter.cslab.ece.ntua.gr"
```

# SSH File Sharing
## Local -> Orion -> Scirouter (With Proxy)
### Local -> Orion
On the Local Machine:
```
scp -r file_to_copy.c parlab07@orion.cslab.ece.ntua.gr:/home/parallel/parlab07
```

### Orion -> Scirouter
On the Orion Machine:
```
scp -r /home/parallel/parlab07/file_to_copy.c parlab07@scirouter.cslab.ece.ntua.gr:/home/parallel/parlab07
```
## Scirouter -> Orion -> Local (With Proxy)
### Scirouter -> Orion
On the Scirouter Machine:
```
scp -r /home/parallel/parlab07/file_to_copy.c parlab07@orion.cslab.ece.ntua.gr:/home/parallel/parlab07
```

### Orion -> Local
On the Local Machine:
```
scp -r parlab07@orion.cslab.ece.ntua.gr:/home/parallel/parlab07/file_to_copy.c .
```

## Local -> Scirouter (Without Proxy)
A way to share **files** directly from local machine to Scirouter, using:
```
rsync -v --rsh "ssh parlab07@orion.cslab.ece.ntua.gr ssh" file_to_copy.c parlab07@scirouter.cslab.ece.ntua.gr:/home/parallel/parlab07/
```
A way to share **directories** directly from local machine to Scirouter, using:
```
rsync -vr --rsh "ssh parlab07@orion.cslab.ece.ntua.gr ssh" dir_to_copy parlab07@scirouter.cslab.ece.ntua.gr:/home/parallel/parlab07/
```

## Scirouter -> Local (Without Proxy)
A way to share **files** directly from Scirouter to local machine, using:
```
rsync -v --rsh "ssh parlab07@orion.cslab.ece.ntua.gr ssh" parlab07@scirouter.cslab.ece.ntua.gr:/home/parallel/parlab07/file_to_copy.c .
```
A way to share **directories** directly from Scirouter to local machine, using:
```
rsync -vr --rsh "ssh parlab07@orion.cslab.ece.ntua.gr ssh" parlab07@scirouter.cslab.ece.ntua.gr:/home/parallel/parlab07/dir_to_copy .
```


# Torque Commands

## Submit for Compiling
On parlab:
```
qsub -q parlab make_on_queue.sh
```

## Submit for Running
On parlab:
```
qsub -q parlab run_on_queue.sh
```
On sandman:
```
qsub -q serial -l nodes=sandman:ppn=64 run_on_queue.sh
```

## View all jobs
```
showq
```

## Get info for the queue
```
queue –d parlab
```

## Get info from running job
```
qstat -f 26160.localhost
```

## Delete a job from the queue
```
qdel 26160
```
