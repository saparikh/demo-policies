# Batfish Enterprise policy examples

This repository contains example policies for a Batfish Enterprise demonstration. Configurations for the demo network can be found at https://github.com/saparikh/demo-network.

Together these 2 repositories are used to demonstrate, how you can:
- Define and upload policies for your network to a Batfish Enteprise service
- Upload production configurations to a Batfish Enterprise service for analysis
- Test changes to configurations with Batfish Enterprise, before deploying them to production.

## High-level demo workflow
Policies are created in this repository and uploaded to the Batfish Enterprise service.
Production configurations are in the main branch of the `demo-network` repository, which is setup to push new changes to the Batfish Enterprise service:
- Anytime a new production snapshot is committed to the main branch
- Anytime a branch is created to test changes to production configurations

## Structure of this repository
The policies are defined in YAML in the `batfish/policies` directory of the repository

The script `setup_bfe.py` in `scripts/` reads these policies and uploads them to the Batfish Enterprise service. The script is triggered by a GH action, which runs anytime a commit is made to the main branch.
- The script will re-initialize the Batfish Enterprise service and push updated policies.
