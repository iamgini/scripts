## Port Checker 

A simple script to verify the required ports are opened between nodes before the deployment of multi-component/multi-node software stacks.

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
- The `nc` utility is available on both source and destination nodes.

