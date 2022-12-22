# baixador-de-imagens-de-sites
Baixador de imagens de sites com filtro que permite baixar so de sites com frase especifica, ele também procura os links do site e baixa as imagens que tiverem neles.

INSTALAÇÃO

# baixador-de-imagens-de-sites

Baixador de imagens de sites com filtro que permite baixar so de sites com frase especifica, ele também procura os links do site e baixa as imagens que tiverem neles.


## INSTALAÇÃO

```groovy
virtualenv {NOME_VENV}
Script\activate
````
```groovy
pip install -r requirements.txt
```

## Screenshot
![image](https://user-images.githubusercontent.com/79776257/209223200-2b322ef3-67c3-4033-bbee-3a8a81f138b9.png)



## Uso/Exemplos

```groovy
-U ou --url --> url do site
-F ou --filtro --> palavra que deve ter no link
-P ou --path --> pasta dentro que vao ser salvas as imagens
-T ou --tempo --> defini o tempo de espera para rolagem da pagina e ir para o proximo link
```

```python
python main.py -U https://www.google.com/search?q=pessoas
python main.py -U https://www.google.com/search?q=pessoas -F google
python main.py -U https://www.google.com/search?q=pessoas -F google -P imagens_pessoas
python main.py -U https://www.google.com/search?q=pessoas -F google -P imagens_pessoas -T 4
```

