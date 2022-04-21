# Adguard Rewrite URL Management

A simple python script to take a list of ip addresses and mac addresses and add them to Adguard URL rewrites.

## Usage

The JSON file required should be in the following format:

``` json
{
    "device_name": {
        "ip_address": "10.1.1.1",
        "mac_address": "aa:bb:cc:dd:ee:ff"
    },
    "device_name": {
        "ip_address": "10.1.1.1",
        "mac_address": "aa:bb:cc:dd:ee:ff"
    }
}
```

The device section can be repeated as many times as required.

The following parameters are required by the script:

| Argument               | Description                                                                     |
|------------------------|---------------------------------------------------------------------------------|
| `-a/--adguard-servers` | List of Adguard servers seperated by comma with http(s):// and port if required |
| `-d/--domain`          | The DNS domain to use                                                           |
| `-u/--user`            | The Adguard username                                                            |
| `-p/--password`        | The Adguard password                                                            |
| `-f/--file`            | The JSON file containing the ip addresses and mac addresses                     |
