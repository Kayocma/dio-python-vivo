curso = "pYthOn"

print(curso.upper()) # torna todas as letras maiúsculas
print(curso.lower()) # torna todas as letras minúsculas
print(curso.title()) # torna a primeira letra de cada palavra maiúscula
print(curso.swapcase()) # inverte o caso de cada letra


curso2 = "     Python     "

print(curso2.strip()) # remove espaços em branco do início e do fim da string
print(curso2.lstrip()) # remove espaços em branco do início da string
print(curso2.rstrip()) # remove espaços em branco do fim da string


curso3 = "Python"

print(curso3.center(20)) # centraliza a string em um campo de 20 caracteres
print(curso3.ljust(20)) # alinha a string à esquerda em um campo de 20 caracteres
print(curso3.rjust(20)) # alinha a string à direita em um campo de 20 caracteres
print(curso3.center(10, "*")) # centraliza a string em um campo de 10 caracteres preenchido com asteriscos


nome = "Kayo Cézar Mendonça de Andrade"

print(nome.split()) # divide a string em uma lista de substrings

print (nome[0]) # imprime a primeira letra da string
print (nome[-1]) # imprime a última letra da string
print (nome[:4]) # imprime as quatro primeiras letras da string
print (nome[5:]) # imprime a string a partir do quinto caractere
print (nome[5:10]) # imprime a string do quinto ao décimo caractere
print (nome[::2]) # imprime a string pulando de dois em dois caracteres
print (nome[::-1]) # imprime a string invertida
print (nome[:]) # imprime a string completa


mensagem = "Olá, meu nome é {nome} e faço o curso de {curso}."

print(mensagem.format(nome="Kayo", curso="Python")) # formata a string substituindo as chaves pelos valores passados como argumento

print(f"Olá, meu nome é {nome} e faço o curso de {curso3}.") # formata a string substituindo as chaves pelos valores das variáveis

mensagem2 = f"""
Olá, meu nome é {nome} e faço o curso de {curso3}.
"""

print(mensagem2) # formata a string substituindo as chaves pelos valores das variáveis


PI = 3.14159                                                     
print(f"Valor de PI: {PI:.2f}")    