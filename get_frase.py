import json
import urllib.request as ureq
import urllib.parse
import random
import sys
import re
from bs4 import BeautifulSoup
from http.cookiejar import CookieJar


#Diretório onde está o arquivo MyNotes.txt dentro do diretório raiz do lol
ARQ_NOTAS = 'C:\Riot Games\League of Legends\MyNotes.txt'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; rv:97.0) Gecko/20100101 Firefox/97.0'


    
    
#remove cochetes, parenteses e todo texto dentro de ambos
#remove caracteres não-ascii e que não estão na lista de exceções
def str2chat_str(str_n_ascii):
    excecoes = (
        231,    #ç ---> 231
        225,    #á ---> 225
        233,    #é ---> 233
        237,    #í ---> 237
        243,    #ó ---> 243
        250,    #ú ---> 250
        224,    #à ---> 224
        236,    #ì ---> 236
        227,    #ã ---> 227
        226,    #â ---> 226
        234,    #ê ---> 234
        244,    #ô ---> 244
        252,    #ü ---> 252
    
    )
    #substitui todos os parenteses e o conteudo dentro deles por nada
    _str = re.sub("[\[].*?[\]]", "", str_n_ascii)
    _str = re.sub("[\(].*?[\)]", "", _str)
    
    
    #só concatena se o caractere for ascii ou estiver na lista de exceções
    ret_str = "".join(ch if (ord(ch) > 31 and ord(ch) < 126) or (ord(ch) in excecoes) else '' for ch in _str ) 
    

    return ret_str


# O parametro disso aqui vai ser o indice do site mais tarde
def zip_zap(site):
    req = ureq.Request('https://www.geradordefrasesaleatorias.com/feeds/posts/default?alt=json-in-script&start-index=' + str(random.randint(1,3436)) + '&max-results=1&callback=random_posts')
    #user agent comum
    req.add_header('User-Agent', USER_AGENT)
    #isso só vai dar erro se der pau na conexão 
    ret = ureq.urlopen(req)
    
    #separa json do js
    str_ret = (ret.read())[29:-2]
    json_ret = json.loads(str_ret)

    


    #Converte a frase para utf-8, atualmente ela é uma string unicode do python
    str_utf8 = json_ret["feed"]["entry"][0]["title"]["$t"].encode('utf8')

    
    return str_utf8
    
# O parametro disso é a categoria na wikipedia
def wikipedia(categoria):

    

    
    #TODO:: se ainda sim a categoria tirada da ultima linha do arquivo for nula ou <1 , joga exceção
    
    
        
    reqData = urllib.parse.urlencode({
    
	"wpcategory": categoria,
	"wpEditToken": "+\\",
	"title": "Especial:Aleatória+na+Categoria",
	"redirectparams": ""

    })
    
    reqData = reqData.encode()
    
    req = ureq.Request('https://pt.wikipedia.org/wiki/Especial:Aleat%C3%B3ria_na_Categoria', headers={
        
        'Host': 'pt.wikipedia.org',
        'User-Agent': USER_AGENT,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://pt.wikipedia.org/wiki/Especial:Aleat%C3%B3ria_na_Categoria',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://pt.wikipedia.org',
        'Connection': 'keep-alive'

    },
    data=reqData
  
    
    )
    
    
    
    #jarra de cookies para evitar loop infinito de redirecionamento 302
    jarra = CookieJar()
    opener = ureq.build_opener(ureq.HTTPCookieProcessor(jarra))
    ret = opener.open(req)
    
    
        
    
    if (ret.status != 200): return
    
    #Se cair na pagina de seleção de categorias, requisita outra pagina aleatoria
    while "?title=Categoria" in ret.url:
    
        ret = ureq.urlopen(req)
        if (ret.status != 200): return
            
        
    html = ret.read() 
    
    
    
    sopa = BeautifulSoup(html, 'html.parser')
    ps = sopa.find_all("div",{"class":"mw-parser-output"})[0]
    p = ps.p
    
    frase = ""
    
    
    for texto in p.stripped_strings:
        frase += " " + texto
        
        
    if len(frase) < 100:
        wikipedia(categoria) 
        
   
    frase = str2chat_str(frase)
    
    
    #TODO:: Isso aqui é feio DEMAIS. Mudar mais tarde.
    frase = frase.replace(" . ", ". ").replace(" , ",", ").replace("  ", " ")
    
    
    if (frase[-2:] == " ."):
        frase = frase[0:len(frase)-2] + "."
        
    frase = frase.strip()
    
    
    
   
    
    
    
    
    return frase.encode("utf8")
    
    

def insultos_shakespeare():
    #http://www.pangloss.com/seidel/Shaker/index.html?
    
    #TODO:: TRADUTOR
    
    return "".encode("utf8")
    
############################
#Associa o valor do argumento do programa com a determinada função para gerar a frase
#O retorno de cada função é sempre uma string utf-8
geradores = (
    zip_zap,
    wikipedia,
    insultos_shakespeare,
    
)
    
def main():
    
    
    
    
    
    
    
    
    
    gerar_frase = geradores[ int(sys.argv[1][0]) ]
    arg_2=""
    if len(sys.argv) > 2:
        arg_2 = sys.argv[2]
    
    else:
        #arg2 não definido. a ultima linha do arquivo de notas do lol será a categoria.
        arq_notas = open(ARQ_NOTAS,encoding='utf-8')
        arg_2 = arq_notas.readlines()[-1].strip()
        
        arq_notas.close()
        
    
   
    try:
 
        #envia a string direto pra saida, sem respeitar a pagina de codificacao de caracteres do console
        sys.stdout.buffer.write(gerar_frase(arg_2))
    except Exception as err:
        #escreve crashlog.
        arq = open('crashlog.txt','w')
        arq.write(str(err))
        arq.close()
        
        
    return 0;
if __name__ == '__main__':
    main()