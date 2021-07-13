# PRTR transfers FastAPI


<p align="center">
  <img src=https://github.com/jodhernandezbe/PRTR_transfers_FastAPI/blob/master/static/img/logo.svg width="50%">
</p>

## Overview

### Data source

The API contains and deploys summary information for 3 Pollutant Release and Transfer Register (PRTR) systems. The 3 PRTR systems are the [National Pollutant Release Inventory (NPRI)](https://www.canada.ca/en/services/environment/pollution-waste-management/national-pollutant-release-inventory.html), the [National Pollutant Inventory (NPI)](http://www.npi.gov.au/), and the [Toxics Release Inventory (TRI)](https://www.epa.gov/toxics-release-inventory-tri-program). The PRTR_transfers_summary database (see the [SQLite database](https://github.com/jodhernandezbe/PRTR_transfers_FastAPI/blob/master/output/PRTR_transfers_summary.db)) provides the summary  information for the data from the the PRTR_transfers database obtained by the data engineering procedure presented in the public GitHub repository [PRTR_transfers](https://github.com/jodhernandezbe/PRTR_transfers).

### Enhanced entity-relationship diagram (EERD) for the PRTR_transfers_summary database

The EERD model in the following figure represents the PRTR_transfers_summary database schema created based on the records from the PRTR_transfers database (see [link](https://github.com/jodhernandezbe/PRTR_transfers/blob/master/data_engineering/load/PRTR_transfers_EER_Diagram.svg)).

<p align="center">
  <img src=https://github.com/jodhernandezbe/PRTR_transfers_FastAPI/blob/master/output/PRTR_transfers_summary_EERD.svg width="90%">
</p>

## Remote deployment

This API was deployed at Heroku

https://prtr-transfers-summary.herokuapp.com/

<ul>
  <li>You can run queries in https://prtr-transfers-summary.herokuapp.com/docs/</li>
  <li>You can see the generic industry sectors list in https://prtr-transfers-summary.herokuapp.com/sectors/</li>
  <li>You can see the generic substances list in https://prtr-transfers-summary.herokuapp.com/substances/</li>
  <li>You can see the generic transfer classes list in https://prtr-transfers-summary.herokuapp.com/transfer_classes/</li>
</ul>
