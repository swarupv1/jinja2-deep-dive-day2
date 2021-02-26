#!/usr/bin/env python3

from pybatfish.client.commands import bf_session, bf_set_network
from pybatfish.question import bfq
from pybatfish.question.question import load_questions
from pybatfish.datamodel.flow import HeaderConstraints, PathConstraints
import click
import os
import code
import pandas as pd

os.environ["PYTHONINSPECT"] = "TRUE"


@click.command()
@click.option(
    "--snapshot_path",
    "-p",
    type=click.Path(),
    required=True,
    help="Snapshot path.",
)
@click.option("--snapshot", "-s", required=False, help="Snapshot name.")
@click.option("--network", "-n", required=False, help="Network name.")
@click.option(
    "--bf_host",
    "-a",
    required=False,
    default="127.0.0.1",
    show_default=True,
    help="Batfish host.",
)
def main(network, snapshot_path, snapshot, bf_host):
    """ Batfish Snapshot Importer """
    bf_session.host = bf_host

    load_questions()

    if not snapshot:
        snapshot = os.path.basename(f"{snapshot_path}_snapshot")
    if not network:
        network = os.path.basename(f"{snapshot_path}_network")

    bf_set_network(network)
    bf_session.init_snapshot(snapshot_path, name=snapshot, overwrite=True)

    code.interact(local=dict(globals(), **locals()))


def update_pd_display():
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 15)
    pd.set_option("display.width", 300)
    pd.set_option("display.max_colwidth", 1)


if __name__ == "__main__":
    #update_pd_display()
    main()