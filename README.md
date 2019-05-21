#### loghub_exporter
阿里云LogHub Prometheus Exporter


##### Using

```
➜  loghub_exporter git:(master) ✗ python loghub_exporter.py --help
Usage: loghub_exporter.py [OPTIONS]

Options:
  -e, --endpoints TEXT      endpoints `,`分割.默认:cn-beijing.log.aliyuncs.com,us-
                            west-1.log.aliyuncs.com
  -k, --access_key_id TEXT  阿里云access_key_id
  -a, --access_key TEXT     阿里云access_key
  -p, --port TEXT           端口,默认:8001
  --help                    Show this message and exit.
```