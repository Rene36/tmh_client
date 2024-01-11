# The Mobility House Coding Challenge
This README explains all steps required on client-side to query an existing PostgreSQL database based on a configuration and then plot the output.

- [Setting Up The Environment](#environment)
- [Configuration File](#configuration)
- [Example Code](#example_code)

## Setting Up The Environment <a name="environment"></a>
Check out [tmh_server](https://github.com/Rene36/tmh_server) for instructions on how to start a new virtual machine with Terraform and to initialize it with Ansible. Otherwise run the following commands to install everything needed to create a new Python virtual environment:
1. `sudo apt update && sudo apt upgrade -y`
2. `sudo apt install python3-venv python3-pip -y`
3. `python3 -m venv name_of_venv`
4. `. name_of_venv/bin/activate`
5. `pip install wheel && pip install --upgrade pip`
6. `pip install git+https://github.com/Rene36/tmh_client`

## Configuration File <a name="configuration"></a>
The configuration is a JSON file obying the following structure. The `level` parameter can either be a list of multiple numbers or a single value:
```
{
    "user": "user_name",
    "password": "user_password",
    "db_name": "db_name",
    "table_name": "curtailments",
    "start_curtailment": "2022-01-01",
    "end_curtailment": "2022-12-31",
    "plant_id": "E2187801EA0100BAGBA00068967600001",
    "level": [0, 30]
}
```

## Example Code <a name="example_code"></a>
Either use an external configuration file or directly add it as a dictionary. See below examples (1.) and (2.):
```
# stdlib
import os

# third party
from tmh_client import plotter
from tmh_client.postgresql import PostgreSQL
from tmh_client.process_data import ProcessData


def main():
    # (1.) Using an external configuration file
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    config_path: str = os.path.join(os.getcwd(), "configs")
    psql: PostgreSQL = PostgreSQL(config_path=config_path,
                                  config_name="query.json")
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # (2.) Using a dictionary for configuration
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    config: dict = {"user": "user_name",
                    "password": "user_password",
                    "db_name": "db_name",
                    "table_name": "curtailments",
                    "start_curtailment": "2022-01-01",
                    "end_curtailment": "2022-12-31",
                    "plant_id": "E2187801EA0100BAGBA00068967600001",
                    "level": [0, 30]}
    psql: PostgreSQL = PostgreSQL(config_path="",
                                  config_name="")
    psql.config = config
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    df = psql.connect_and_extract()

    process_data: ProcessData = ProcessData(df)
    process_data.clean()

    plotter.plot_data(df=process_data.get_data(),
                      config=psql.config)


if __name__ == "__main__":
    main()
```
