#code adapted from stem.torproject.org/tutorials/to_russia_with_love.html

import io
import pycurl
import certifi

import stem
import stem.process

PORT = 9150

def connect(url):

    output = io.BytesIO()

    con = pycurl.Curl()
    con.setopt(pycurl.CAINFO, certifi.where())
    con.setopt(pycurl.URL, url)
    con.setopt(pycurl.PROXY, 'localhost')
    con.setopt(pycurl.PROXYPORT, PORT)
    con.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)
    con.setopt(pycurl.WRITEFUNCTION, output.write)

    try:
        con.perform()
        return output.getvalue()
    except pycurl.error as err:
        return 'Cannot reach %s (%s)' % (url,err)

def message_handler(line):
    print(line)

print('Starting:\n')

tor = stem.process.launch_tor_with_config(
    config = {
        'SocksPort': str(PORT),
        #'UseBridges': '1',
        #'Bridge': '79.136.160.201:44729'
        #'Bridge' : '79.136.160.201:44729 66AC975BF7CB429D057AE07FC0312C57D61BAEC1'
        #'Bridge': '212.144.102.196:30009 80E446A40424933350EAC3DA4A3E3844964E9DBE'
        #109.218.75.215:45602 89F669CE7B9174430DB5C40667F836D90231C7D3
        #'Bridge': '5.45.180.246:443'# 09938051EC4F4B4099DDAEE24ADA9243A24EFC07'
    },
    init_msg_handler = message_handler,
    tor_cmd = "C:\Tor-win32-0.3.3.7\Tor\Tor.exe"
)

print('Connected from:\n')
print(connect('https://www.atagar.com/echo.php'))

tor.kill()
