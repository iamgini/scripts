## Port Checker 

A simple script to verify the prereq ports are opened between nodes.

## Sample CSV

`Source,Destination,Port`

```csv
$ cat port-checker-data.csv
localhost,192.168.57.145,80
192.168.57.140,192.168.57.145,443

```

Note: Remember to add a new line at the end of file.

## Prerequisite

- Target nodes (source and destination) are able to access from the localhost over SSH without password.
- The `remote_user` has sudo access on target nodes without password.

