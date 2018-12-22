#!/usr/bin/env python
# *-* coding: utf-8 *-*
import re
import time
import urllib2
import requests
import pyping
from BeautifulSoup import BeautifulSoup


class GoogleEngine:

    def __init__(self, key='777c64eaf7b22ead16668198b16266e1'):
        self.request_headers = {
            "Accept-Language": "en-US,en;q=0.5",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "https://www.google.com",
            "Connection": "keep-alive"
        }

        self.url = "http://www.google.com/search"
        self.hl = "en"
        # self.q = "????"
        self.start = 1  # numero da pagina
        self.num = "100"  # qtd de resultados por paginas
        # self.sa = "N"
        # self.filter = "0"
        self.key = key
        self.request = 'http://2captcha.com/in.php'
        self.response = 'http://2captcha.com/res.php'
        self.proxies = {}

        self.getProxy()

    # resolve captcha
    def solve(self, googlekey, site):


        payload = {'key': self.key, 'method': 'userrecaptcha', 'googlekey': googlekey, 'pageurl': site}
        req = requests.get(self.request, params=payload, proxies=self.proxies)
        req = req.content.split('|')

        if req[0] == 'OK':
            idRequest = req[1]
            payload = {'key': self.key, 'action': 'get', 'id': idRequest}
            wait = True
            i = 0
            while wait:
                try:
                    time.sleep(15)
                    res = requests.get(self.response, params=payload, proxies=self.proxies, timeout=1)
                    res = res.content.split('|')
                    if res[0] == 'OK':
                        wait = False
                        return res[1]
                    else:
                        if i > 15:
                            return True
                        i = i + 1
                        time.sleep(15)
                        print str(i) + 'ª Tentativa - Waiting Solve Captcha'

                except (requests.exceptions.ConnectionError), e:
                    print '- Timeout'
                    time.sleep(2)


        return False

    def search(self, query):

        results = []
        total = 0

        #dominios = ['com', 'com.br', 'pt', 'it', 'es'] #PODE ADICIONAR VARIOS DOMINIOS DO GOOGLE
        dominios = ['com.br']

        for q in query:
            q = q.replace('\n', '').replace('\r', '')
            for dominio in dominios:
                print '\nSearch [' + q + '] in www.google.' + dominio
                q = urllib2.quote(q)
                url_search = "http://www.google." + dominio + "/search?hl=" + self.hl + "&q=" + q + "&start=" + str(
                    self.start) + "&num=" + self.num + "&sa=N&filter=0"

                response = requests.get(url_search, headers=self.request_headers, proxies=self.proxies)

                while True:

                    print "\n\t\t\tPagina: " + str(self.start) + "\n"

                    # se tiver recaptcha, resolve

                    if response.url.find("google.com/sorry") >= 0:
                        print "Captcha para resolver"

                        # explicacao: pq nao usei urllib2? R: problemas no redirecionamento e mais linhas de codigos

                        soup = BeautifulSoup(response.text)
                        googlekey = soup.find(attrs={"id": "recaptcha"})['data-sitekey']
                        solveCaptcha = self.solve(googlekey, response.url)

                        if type(solveCaptcha) == (str):

                            try:
                                response = requests.get(response.url + "&g-recaptcha-response=" + solveCaptcha,
                                                    headers=self.request_headers)

                            except (requests.exceptions.SSLError, requests.exceptions.ConnectionError), e:
                                print '- SSL error'
                                pass
                        else:
                            break



                        print "Captcha resolvido com sucesso"

                    # captura codigo html da pagina
                    soup = BeautifulSoup(response.text)
                    # print response.url

                    p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'

                    i = 1
                    # captura os links dos resultados
                    links = soup.findAll("div", {"class": "r"})
                    for link in links:
                        link = link.findChild().attrs[0][1]
                        fullurl = link
                        m = re.search(p, link)
                        link = m.group('host')
                        print '# [google.' + dominio + '] Verificando  ' + str(i) + ' / ' + str(
                            len(links)) + ' : ' + fullurl
                        # if link not in results:
                        if fullurl not in results:
                            results.append(fullurl)
                        i += 1
                        total += i

                    print "Hosts: " + str(i)

                    self.start += 1

                    # avanca para proxima pagina
                    try:
                        linknext = str(response.url[:22]) + soup.find(attrs={"id": "pnnext"})["href"]
                        response = requests.get(linknext, headers=self.request_headers, proxies=self.proxies)
                    except:
                        break

        return results

    def getProxy(self):
        #r = requests.get('https://proxy.l337.tech/txt')
        listproxy = open('proxies.txt', 'r')
        listproxy = listproxy.readlines()
        proxies = {}
        for proxy in listproxy:
            proxy = proxy.replace('\n','').split(' ')[0]
            proxy = proxy.split(':')
            if(len(proxy) == 2):
                proxy = {proxy[0] : proxy[1]}
                proxies.update(proxy)

        self.proxies = proxies