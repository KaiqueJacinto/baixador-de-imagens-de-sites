from selenium import webdriver
import hashlib
import time
import urllib.request
import requests
import shutil
import random
import os
import sys

def baixa_imagem(link,nome_arquivo):
    '''Baixa imagens, ele tenta de duas formas diferentes e caso nao seja possivel baixar
        ele notifica o erro!'''
    try:
        urllib.request.urlretrieve(link, f"temp/{nome_arquivo}.jpg")
    except:
        try:
            with open('temp/{nome_arquivo}.jpg', 'wb') as imagem:
                resposta = requests.get(link, stream=True)
                if not resposta.ok:
                    print("Ocorreu um erro, status:" , resposta.status_code)
                else:
                    for dado in resposta.iter_content(1024):
                        if not dado:
                            break
                        imagem.write(dado)
        except:
            print('Não foi possivel baixar a imagem')

def gera_hash(caminho):
    '''Gerador de hash do arquivo, no nosso caso gera hash das imagens!'''
    hash_arquivo = hashlib.sha256()
    hash_arquivo.update(open(caminho, 'rb').read())
    return hash_arquivo.hexdigest()

def tira_repitidos(lista1,lista2,filtro):
    '''Tira repetidos além de aplicar o filtro caso ele seja definido'''
    if filtro != '':
        lista = lista1.copy()
        for i in lista2:
            if not(i in lista1) and filtro in i:
                lista.append(i)
        return lista
    else:
        lista = lista1.copy()
        for i in lista2:
            if not(i in lista1):
                lista.append(i)
        return lista

def atualiza_dados(lista_hash,filtro):
    '''Atualiza a lista de hashs baixadas'''
    try:
        with open('hash.txt','r') as teste:
            lista = teste.read().split(';')[:-1:]
    except:
        lista = []
        open('hash.txt','a')
    lista = tira_repitidos(lista,lista_hash,filtro)
    with open('hash.txt','wt') as teste:
        for i in lista:
            teste.write(i+';')

def cria_diretorio(caminho):
    '''Cria diretorio na pasta onde o arquivo .py esta sendo executado'''
    if not(os.path.isdir(caminho)):
        os.mkdir(caminho)

def main(filtro,lista_li,onde_salvar_imagens,TEMPO_ESPERA):
    lista = lista_li.copy()
    lista_links_imagens_baixadas = [] # Lista de links de imagens baixadas
    lista_de_hashs = [] # Lista de hashs das imagens
    num_lista = 0 # Numero do link que sera acessado
    total_imagens_achadas = 0 # Total de imagens achadas nos sites (NORMALMENTE ESSE NUMERO É MAIOR DO QUE O NUMERO DE IMAGENS BAIXADAS, ISSO OCORRE VISTO QUE NEM TODAS AS IMAGENS SÃO BAIXADAS, POR SEREM REPETIDAS OU POSSIVEIS ERROS NO DOWNLOAD)
    cria_diretorio(onde_salvar_imagens) # Cria a pasta caso nao exista
    driver = webdriver.Firefox()
    driver.get(lista[num_lista])
    while (len(lista) > num_lista):
        try:
            driver.execute_script(F'window.location.href = "{lista[num_lista]}"')
            time.sleep(TEMPO_ESPERA)
            SCROLL_PAUSE_TIME = TEMPO_ESPERA/2
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)
                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            time.sleep(TEMPO_ESPERA*1.5)
            teste = driver.execute_script('''let lista = document.getElementsByTagName('a')
                                            let lista_final = []
                                            for(let num=0;num<lista.length;num++){
                                                if(lista[num].href != ''){
                                                    lista_final.push(lista[num].href)
                                                }
                                            }
                                            
                                            return lista_final''')
            links_imgs = driver.execute_script('''let lista1 = document.getElementsByTagName('img')
                                            let lista_imgs = []
                                            for(let num=0;num<lista1.length;num++){
                                                if(lista1[num].currentSrc != ''){
                                                    lista_imgs.push(lista1[num].src)
                                                    lista1[num].hidden = true
                                                }
                                            } return lista_imgs''')
            total_imagens_achadas +=len(links_imgs)
            lista = tira_repitidos(lista,teste,filtro)
            for link_img in links_imgs:
                if not(link_img in lista_links_imagens_baixadas):
                    nome_arquivo = f'tempAux-{random.randint(1000000000000000000000,999999999999999999999999999999)}'
                    baixa_imagem(link_img,nome_arquivo)
                    lista_links_imagens_baixadas.append(link_img)
                    hash_imagem = gera_hash(f'temp/{nome_arquivo}.jpg')
                    print(f'LINKS VERIFICADOS [{str(num_lista+1)}/{len(lista)}] || IMAGENS BAIXADAS {len(lista_de_hashs)} || IMAGENS ACHADAS {total_imagens_achadas}',end='\r')
                    
                    if not(hash_imagem in lista_de_hashs):
                        shutil.move(f'temp/{nome_arquivo}.jpg', f'{onde_salvar_imagens}/{hash_imagem}.jpg')
                        lista_de_hashs.append(hash_imagem)
                        shutil.rmtree(f'temp/{nome_arquivo}.jpg', ignore_errors=True)
                    else:
                        os.remove(f'temp/{nome_arquivo}.jpg')
                        shutil.rmtree(f'temp/{nome_arquivo}.jpg', ignore_errors=True)
            atualiza_dados(lista_de_hashs,filtro)
            
            num_lista+=1
        except:
            num_lista+=1

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filtro,link_inicial,pasta_inicial,TEMPO_ESPERA = '','','imagens',2
        parametros = []
        for i, arg in enumerate(sys.argv):
            parametros.append(arg)
        for num in range(len(parametros)):
            if parametros[num] == '-F' or parametros[num] == '--filtro':
                filtro = parametros[num+1]
            elif parametros[num] == '-U' or parametros[num] == '--url':
                link_inicial = parametros[num+1]
            elif parametros[num] == '-P' or parametros[num] == '--path':
                pasta_inicial = parametros[num+1]
            elif parametros[num] == '-T' or parametros[num] == '--tempo':
                TEMPO_ESPERA = parametros[num+1]
        main(filtro,[link_inicial,],pasta_inicial,int(TEMPO_ESPERA))
    else:
        filtro = input('Filtro de url: ') # Se alguma palavra for colocada aqui so vai acessar links que possua essa palavra.
        lista_links=[input('URL inicial: '),] # Lista de links que seram acessados
        onde_salvar_imagens = input('Nome da pasta onde sera salvo as imagens: ') # Pasta onde serão salvas as imagens, ela sera criada dentro do diretorio de execução do .py
        TEMPO_ESPERA = 2 # Tempo de espera entre execução (DEPENDE DA SUA INTERNET)
        main(filtro,lista_links,onde_salvar_imagens,TEMPO_ESPERA)