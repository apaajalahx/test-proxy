import requests
import argparse

def save(filename, proxy):
    z = open(filename, 'a')
    z.write(proxy + "\n")
    z.close()

def checkProxyTypeAndVersion(proxy, pattern, timeout):
    try:
        
        test_get = requests.get('https://httpbin.org/status/200', proxies=proxy, timeout=timeout)
        if test_get.status_code == 200:
            return pattern
    except:
        return False

def check(proxy, timeout):
    patterns = ['https','http', 'socks4', 'socks5']
    for pattern in patterns:
        Proxies = {
            'http' : pattern + '://' + proxy,
            'https' : pattern + '://' + proxy
        }
        if checkProxyTypeAndVersion(Proxies, pattern, timeout):
            print('Proxy {} Live With Pattern {}'.format(proxy, pattern))
            save('proxy_live.txt', "{}://{}".format(pattern, proxy))
            break
        else:
            print('DIE : Proxy {}, Pattern {}'.format(proxy, pattern))

def main(proxy, target_web = 'https://rapiddns.io/', pattern='https://www.cloudflare.com', timeout=10):
    try:
        HEADERS = {
            'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0',
            'Cookie' : '_ga=GA1.2.425455903.1647080836; _gid=GA1.2.1443908755.1647080836; __gads=ID=ceb718d01be4a46e-221ca57df0d000bc:T=1647080836:RT=1647080836:S=ALNI_MbAv0xZB9uU11EPdqHHjfEYY9vgyw'
        }
        Proxies = {
            'http' : proxy,
            'https' : proxy
        }
        get = requests.get(target_web, headers=HEADERS, proxies=Proxies, timeout=timeout)
        if pattern not in get.text:
            print('Proxy Support to access rapiddns : {}'.format(proxy))
            save('proxy-cf.txt', proxy)
        else:
            print('Proxy Not support to access rapiddns : {}'.format(proxy))
    except ConnectionError:
        print('Proxy Connection Error : {}'.format(proxy))
    except TimeoutError:
        print('Proxy Timeout Error : {}'.format(proxy))
    except Exception as e:
        print('Error : {}'.format(proxy))
    except:
        print('Proxy Unknow Error : {}'.format(proxy))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test Proxy, dah gitu aja")
    parser.add_argument('--file', help="Filename list proxy", required=True)
    parser.add_argument('--check-version', help="Check Version of proxy", action="store_true")
    parser.add_argument('--cf', help="Check if proxy to web/site without get cloudflare", action="store_true")
    parser.add_argument('--pattern', help="Pattern for check if target has cloudflare anti DDos, (not support regex)")
    parser.add_argument('--target', help="Web Target for check cf, ex: https://rapiddns.io/ (input must like example)")
    parser.add_argument('--timeout', help="set timeout")
    args = parser.parse_args()
    timeout = 10
    if args.timeout:
        if args.timeout != '':
            timeout = int(args.timeout)
    if args.check_version:
        io = open(args.file, 'r').read().splitlines()
        for i in io:
            check(i, timeout)
    elif args.cf:
        io = open(args.file, 'r').read().splitlines()
        pattern = 'https://www.cloudflare.com'
        target = 'https://rapiddns.io/'
        if args.pattern:
            if args.pattern != '':
                pattern = args.pattern
        if args.target:
            if args.target != '':
                target = args.target
        for i in io:
            main(i, target_web=target, pattern=pattern, timeout=timeout)
    else:
        parser.print_help()
