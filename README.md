# test-proxy


check proxy type and version (Support http, https, socks4 and socks5).

```
 python3 --file proxy.txt --check-version --timeout 10
```

check proxy if can access web who using cloudflare protection.

note: check proxy_live.txt before use this.
```
 python3 proxy_test.py --file proxy_live.txt --cf --pattern https://www.cloudflare.com --target https://rapiddns.io/ --timeout 10
```
