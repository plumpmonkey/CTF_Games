# ROT13 Demo

## Run the Server
```python3 server.py```

## Connect to using telnet or nc.

```
$ nc 127.0.0.1 8000
Gb erprvir gur synt, erfcbaq jvgu EBG13 rapbqrq grkg fnlvat 'Fraq Synt'
hello
Gb erprvir gur synt, erfcbaq jvgu EBG13 rapbqrq grkg fnlvat 'Fraq Synt'
Fraq Synt
Synt{Jryy_Qbar_Lbh_Fcrnx_EBG13}
```
## Decoded
```
$ echo "Gb erprvir gur synt, erfcbaq jvgu EBG13 rapbqrq grkg fnlvat 'Fraq Synt'" | rot13
To receive the flag, respond with ROT13 encoded text saying 'Send Flag'
$ echo "Send Flag" | rot13
Fraq Synt
$ echo "Synt{Jryy_Qbar_Lbh_Fcrnx_EBG13}" | rot13
Flag{Well_Done_You_Speak_ROT13}
```
