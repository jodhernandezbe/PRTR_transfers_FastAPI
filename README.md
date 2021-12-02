# PRTR transfers FastAPI


<p align="center">
  <img src=https://github.com/jodhernandezbe/PRTR_transfers_FastAPI/blob/local/static/img/logo.svg width="50%">
</p>

# Overview

## Data source

The API contains and deploys summary information for three Pollutant Release and Transfer Register (PRTR) systems. The three PRTR systems are the [National Pollutant Release Inventory (NPRI)](https://www.canada.ca/en/services/environment/pollution-waste-management/national-pollutant-release-inventory.html), the [National Pollutant Inventory (NPI)](http://www.npi.gov.au/), and the [Toxics Release Inventory (TRI)](https://www.epa.gov/toxics-release-inventory-tri-program). The PRTR_transfers_summary database (see the [SQLite database](https://github.com/jodhernandezbe/PRTR_transfers_FastAPI/blob/master/output/PRTR_transfers_summary.db)) provides the summary  information for the data from the the PRTR_transfers database obtained by the data engineering procedure presented in the public GitHub repository [PRTR_transfers](https://github.com/jodhernandezbe/PRTR_transfers).

## Enhanced entity-relationship diagram (EERD) for the PRTR_transfers_summary database

The EERD model in the following figure represents the PRTR_transfers_summary database schema created based on the records from the PRTR_transfers database (see [link](https://github.com/jodhernandezbe/PRTR_transfers/blob/master/data_engineering/load/PRTR_transfers_EER_Diagram.svg)).

<p align="center">
  <img src=https://github.com/jodhernandezbe/PRTR_transfers_FastAPI/blob/local/output/PRTR_transfers_summary_EERD.svg width="90%">
</p>

# Requirments

## Developers

### Creating conda environment

A conda environment can be created by executing the following command:

      
    conda env create -n PRTR_FastAPI -f environment.yml

The above command is written assuming that you are in the folder containing the .yml file, i.e. the root folder PRTR_transfers_FastAPI. 

### Ovoiding ModuleNotFoundError and ImportError

If you are working as a Python developer, you should avoid both ```ModuleNotFoundError``` and ```ImportError``` (see the following [link](https://towardsdatascience.com/how-to-fix-modulenotfounderror-and-importerror-248ce5b69b1c)). Thus, follow the steps below to solve the above mentioned problems:

<ol>
  <li>
    Run the following command in order to obtain the PRTR_transfers_FastAPI project location and then saving its path into the variable PACKAGE
    
    PACKAGE=$(locate -br '^PRTR_transfers_FastAPI$')
  </li>
  <li>
    Check the PACKAGE value by running the following command
    
    echo $PACKAGE
   </li>
   <li>
    Run the following command to add the PRTR_transfers_FastAPI project to the system paths
     
    export PYTHONPATH="${PYTHONPATH}:$PACKAGE"
   </li>
</ol>

If you prefer to save the path to the PRTR_transfers_FastAPI project folder as a permanent environment variable, follow these steps:

<ol>
   <li>
    Open the .bashrc file with the text editor of your preference (e.g., Visual Studio Code)
        
    code ~/.bashrc
   </li>
   <li>
    Scroll to the bottom of the file and add the following lines
       
    export PACKAGE=$(locate -br '^PRTR_transfers_FastAPI$')
    export PYTHONPATH="${PYTHONPATH}:$PACKAGE"
   </li>
   <li>
    Save the file with the changes
   </li>
   <li>
    You can open another terminal to verify that the variable has been successfully saved by running the following command
    
    echo $PYTHONPATH
   </li>
</ol>

<hr/>

# Remote deployment

This was deployed at Heroku where you can also test it from the docs endpoint

WebSite: https://prtr-transfers-summary.herokuapp.com/

API documentation: https://prtr-transfers-summary.herokuapp.com/v1/api_documentation

<hr/>

# Local deployment

Run the following command for local deployment
```
python run.py
```
Go to http://127.0.0.1:8000
