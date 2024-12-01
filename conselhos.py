import requests
from deep_translator import GoogleTranslator
import json

def buscar_conselhos(quantidade):
    
    url = "https://api.adviceslip.com/advice"
    conselhos = []
    for _ in range(quantidade):
        response = requests.get(url)
        data = response.json()
        conselho = data['slip']['advice']
        conselho_id = data['slip']['id']
        conselhos.append((conselho, conselho_id))
    return conselhos

def salvar_conselhos(conselhos):
    
    with open('conselhos.json', 'w') as arquivo:
        json.dump(conselhos, arquivo, indent=4)

def carregar_conselhos():
    
    try:
        with open('conselhos.json', 'r') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []

def traduzir_conselho(texto, idioma_destino='pt'):
    
    translator = GoogleTranslator(source='auto', target=idioma_destino)
    traducao = translator.translate(texto)
    return traducao

def menu():
    
    while True:
        print("\nBem-vindo aos conselhos do Seu Zé!")
        print("1. Ouvir novos conselhos")
        print("2. Ver conselhos salvos")
        print("3. Traduzir conselho")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            quantidade = int(input("Quantos conselhos você deseja? "))
            conselhos = buscar_conselhos(quantidade)
            salvar_conselhos(conselhos)
            print("Conselhos foram registrados com sucesso!")

        elif opcao == '2':
            conselhos = carregar_conselhos()
            if conselhos:
                for i, (conselho, conselho_id) in enumerate(conselhos):
                    print(f"{i+1}. Conselho {conselho_id}: {conselho}")
            else:
                print("Nenhum há conselho salvo.")

        elif opcao == '3':
            conselhos = carregar_conselhos()
            if conselhos:
                print("Escolha o conselho a ser traduzido:")
                for i, (conselho, conselho_id) in enumerate(conselhos):
                    print(f"{i+1}. Conselho {conselho_id}: {conselho}")
                opcao_traducao = int(input("Digite o número do conselho: ")) - 1
                texto_a_traduzir = conselhos[opcao_traducao][0]
                traducao = traduzir_conselho(texto_a_traduzir)
                print("Tradução:", traducao)
            else:
                print("Nenhum conselho salvo para tradução.")

        elif opcao == '4':
            break

if __name__ == "__main__":
    menu()