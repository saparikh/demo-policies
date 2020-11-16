# required imports
from pybfe.client.session import Session
import yaml
from pathlib import Path
import argparse


def upload_bf_policies(bf, policy_dir):
    # find and upload network policies to Batfish Enterprise
    for policy in Path(policy_dir).iterdir():
        if policy.is_file():
            with open(policy) as fp:
                assertions = yaml.safe_load(fp)
                for assertion in assertions['assertion']:
                    bf._experimental_create_policy(assertion)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--network', default="demonet",
                        help='Network name')
    parser.add_argument('-a', '--aggregates',
                        help='Aggregates for the network')
    parser.add_argument('-p', '--policies', default = "./batfish/policies",
                        help='Directory with Batfish Enterprise policies. Default value is "./batfish/policies"')
    parser.add_argument('-sn', '--server_name', required=True,
                        help='Hostname or IP address of Batfish Enterprise server')
    parser.add_argument('-sp', '--server_port', default = 443,
                        help='TCP port the Batfish Enterprise server is listening to')
    parser.add_argument('-r', action='store_true', dest='re_init',
                        help='Reset Batfish Enterprise by deleting network')
    parser.add_argument('-nr', action='store_false', dest='re_init',
                        help='Do not reset Batfish Enterprise by deleting network')
    options = parser.parse_args()

    POLICY_DIR = options.policies

    if not Path(POLICY_DIR).is_dir():
        print(f"Supplied path to policies - {POLICY_DIR} is invalid")
        exit()
    else:
        if not Path(POLICY_DIR).is_absolute():
            POLICY_DIR = Path(POLICY_DIR).absolute()

    host = options.server_name
    port = options.server_port
    network = options.network
    bf = Session(host=host, port=port)  # establish session
    if options.re_init:
        try:
            bf.delete_network(network)
        except:
            pass
    bf.set_network(network)

    if options.aggregates is not None:
        if not Path(options.aggregates).is_absolute():
            aggregates = Path(options.aggregates).absolute()
            if not Path(aggregates).exists():
                print(f"Supplied aggregates file {aggregates} does not exist")
            else:
                with open(aggregates) as fp:
                    _aggs = yaml.safe_load(fp)
                bf.put_network_aggregates(_aggs)

    upload_bf_policies(bf, POLICY_DIR)