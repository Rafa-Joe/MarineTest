from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import csv
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://data.marine.copernicus.eu/viewer/expert?view=viewer&crs=epsg%3A4326&t=1606201200000&z=&center=26.667941517076972%2C2.9568943839625508&zoom=9.892117678674271&layers=H4sIANdlvGcAAxXNywrCMBBA0X_ZddWk3Uh3FUQLLRYfiyIyhGSogaSRJD6i_O.a5b2bc.6AEYl8raCETbNbVQ22p_ZY9_tqj922R8Y4soItpCUb0DqFg3F4uya0CdmcLQtFA3a8nVnMWV5wvggk8CkieXyQcVLHBBm861HRC8qcZaAnDQ3.b_OGgxSGoIz_ThmEmKaA4IxW1ag64aOWhgJ8Lz.uiTVRrQAAAA--&basemap=dark&objv2=H4sIANdlvGcAA1WNwQrCMBBE.2XPsdjShJCjBz3qXUKJdqs5NAnpFiySf3erIPQ6b2be9Q2_BwNdVCBgQEdzxgkM57QkZHL8ZUwfGEekvID5w0v0gRjdY8y9D46_27ZSUtZaCtVUWrVyr2wRkHJMmMmvlY01uHH96k5QimVNdum5dnjjp8MtvsBQnpEffDgPw4TEjp3Wom5ssR87nR3pwgAAAA--")
time.sleep(10)

#caminho onde está o csv com as coordenadas
caminho_csv = "C:\\Users\\AGAPYS\\Desktop\\Job\\testeMarine\\dadosMarine.csv"

#clicar no botão para abrir a janela de login
iconeSubset = driver.find_element(By.XPATH, "//*[@id='__next']/main/div/div[4]/div[2]/div/div/div[4]/div[1]/div[1]")
iconeSubset.click()
#coloca teu usuario e senha do site
campoUsuario = driver.find_element(By.XPATH, "//*[@id='username']")
campoUsuario.send_keys('seuemail@e-mail.com')
campoSenha = driver.find_element(By.XPATH, "//*[@id='current-password']")
campoSenha.send_keys('senha123')
clicarEntrar = driver.find_element(By.XPATH, "//*[@id='cm-overlays']/div/div[2]/div/div/form/div[2]/button")
clicarEntrar.click()

#mudar datas inicial e final
dataInicial = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "_l1-timeMin")))
dataInicial.send_keys("03/06/2020")
dataFinal = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "_l1-timeMax")))
dataFinal.send_keys("28/12/2020")
#mudar profundidade
depthIni = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "_l1-elevationMax")))
depthIni.send_keys("0,49402")
depthFin = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "_l1-elevationMin")))
depthFin.send_keys("0,49402")

#criar função de limpar e digitar no campo
def limpar_e_digita_campo(elemento, valor):
    elemento.send_keys(Keys.CONTROL + 'a')
    elemento.send_keys(Keys.DELETE)
    elemento.send_keys(valor)

#ler o CSV e fazer o loop de download
with open(caminho_csv, mode='r', encoding='utf-8') as arquivo:
    leitorCsv = csv.reader(arquivo, delimiter=';')
    cabecalho = next(leitorCsv)
    for linha in leitorCsv:
        try:
            #identificar os campos
            cordNorth = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "_l1-latMax")))
            cordSouth = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "_l1-latMin")))
            cordWest = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "_l1-lonMin")))
            cordEast = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "_l1-lonMax")))
            #escrever as coordenadas nos campos
            limpar_e_digita_campo(cordNorth, linha[0])
            limpar_e_digita_campo(cordSouth, linha[0])
            limpar_e_digita_campo(cordWest, linha[1])
            limpar_e_digita_campo(cordEast, linha[1])
            time.sleep(5)
            clicarDownload = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='__next']/main/div/div[4]/div[2]/div/div/div[5]/div/div[5]/div[2]/div[2]")))
            clicarDownload.click()
            time.sleep(25)
        except Exception as e:
            print(f"Erro ao processar a linha: {linha}. Erro: {e}")

print(f"Valide se tudo foi baixado corretamente!")
#Caso tu queira que o robô espere para fechar o navegador, irá fechar após você apertar Enter
#input("Pressionar enter para fechar navegador...")
#cordEast.send_keys(Keys.RETURN)
