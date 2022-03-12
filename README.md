# llch-logger

This library is provided to allow standard python logging to output log data as json objects.
With JSON we can make our logs more readable by machines and we can stop writing custom parsers for syslog type records.

It also outputs the log to the console.

## Installation

```sh
python3 -m pip install llch-logger
```

## Usage

```sh
usage: python -m llch_logger [-h] [-m MESSAGE] [-I | -W | -E | -D | -A | -R] [--config CONFIG]

Sends logging messages [llch_logger 0.1.1] By default, it sends an information message.

optional arguments:
  -h, --help            show this help message and exit
  -m MESSAGE, --message MESSAGE
                        Message to be sent. By default, it is of type information.
  -I, --info            INFO message.
  -W, --warn            WARN message.
  -E, --error           ERROR message.
  -D, --debug           DEBUG message.
  -A, --audit           AUDIT message.
  -R, --raw             RAW message
  --config CONFIG       Location of the configuration file. Default: ./config.ini
```

```sh
python3 -m llch_logger -m "INFORMATION message to be saved"
python3 -m llch_logger -A -m "AUDITOR message to be saved"
python3 -m llch_logger -R -m "RAW message to be saved"
```

## Usage within python

```python
from llch_logger import Logger

logger = Logger()
logger.set_execution_metadata({"metadata1": "metadata1", "metadata2": 22,  "metadata3": "", "metadata4": None})
logger.info("INFORMATION message to be sent")
logger.audit("AUDITOR message to be sent")
```

### config.ini

```ini
[log]
log_level=DEBUG
log_folder=../log
write_to_stdout = true
```

## Results

```json
{
  "message": "Sending a message",
  "eventId": "xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx",
  "eventDate": "xxxx-xx-xxTxx:xx:xx.xxxxx-xx:00",
  "correlationId": "xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx",
  "header": {
    "source": { "version": "0.1.1", "appName": "unittest.suite" },
    "host": { "name": "xxxxxxxxxx", "ip": "xxx.xxx.xx.xx" }
  },
  "payload": {
    "message": "Sending a message",
    "additionalFields": {
      "metadata1": "metadata1",
      "metadata2": 22,
      "metadata3": "",
      "metadata4": null
    }
  },
  "type": "INFO"
}
```
