#!/usr/bin/env python

import ipdb
import argparse
import sh
import time

EUAT_PORT=5439


def run_slave_cmd(name, cmd):
    bastion = "bastion.{}.fc-unstable.co.uk".format(name)
    baked = sh.ssh.bake("-tt", bastion)
    members = baked("consul members")
    sample_slave = [x for x in members.stdout.splitlines() if 'slave' in x][0].split(' ')[0]
    return baked("ssh", "-tt", sample_slave, cmd)


def open_tunnel(name, port):
    bastion = "bastion.{}.fc-unstable.co.uk".format(name)
    opts = "-o ExitOnForwardFailure=yes -f -A -L {}:postgres-postgres.service.consul:5432 {} sleep 10".format(
        port, bastion
    )
    return sh.ssh("-o", "ExitOnForwardFailure=yes", "-A", "-L",
                  "{}:postgres-postgres.service.consul:5432".format(port),
                  bastion,
                  _bg=True)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Open a tunnel and start pgcli')

    parser.add_argument('name', help="Name of the euat")
    parser.add_argument('-c', '--cmd',
                        help="Extra command to run")

    return parser.parse_args()


def pgcli(args):
    ssh_proc = open_tunnel(args.name, EUAT_PORT)

    time.sleep(10)
    pg_proc = sh.pgcli("-h", "localhost",
                       "-p", EUAT_PORT,
                       "-U", "payments_reconciler",
                       "payments_reconciler")

    print(pg_proc.std_out)
    print(pg_proc.std_err)


if __name__ == '__main__':
    args = parse_arguments()
    print(run_slave_cmd("andrea-2", args.cmd))
