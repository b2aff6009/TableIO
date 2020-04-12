# TableIO
![tests](https://github.com/b2aff6009/TableIO/workflows/tests/badge.svg?branch=master)

## Settings
- type: "csv"/"xls"/"google" #defines the type of the underlying table
- parse: true/false #sets if the given table should be parsed or not
- parseDirection: "row"/"column" #defines if the table should be parsed column or row wise
- offsetX: <Int> #defines an x-offset for parsing
- offsetY: <Int> #defines an y-offset for parsing
- permission: "read"/"write"/"" #defines if the permissions of the parser ("" allows read and write)
