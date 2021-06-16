from selenium import webdriver
# from selenium.webdriver.support.ui import expected_conditions as EC
import time
import pandas as pd
from pandas import DataFrame

# carregando driver e passando endereço
driver = webdriver.Chrome("/home/arch/Downloads/chromedriver")

#abrindo página
driver.get('https://transparencia.fortaleza.ce.gov.br/index.php/despesa/acompanhamentoExecucaoOrcamentaria')

# seleção via id
filtro_orgao = driver.find_element_by_id('filtroPorOrgao')
# coleta todas opções de um elemento
todos_orgaos = filtro_orgao.find_elements_by_tag_name("option")

orgaos = {}
funcoes = {}
sub_funcoes = {}

tabelas = [] #usar no pandas

for orgao in todos_orgaos:
  if orgao.get_attribute("text") != '':
    orgao.click()
    # pausa pra esperar ajax
    time.sleep(0.5)
    # coletando funções carregadas via ajax (elas variam dependendo do órgão)
    filtro_funcao = driver.find_element_by_id('cboFuncao')
    funcoes_carregadas = filtro_funcao.find_elements_by_tag_name("option")
    funcoes = {}
    for funcao in funcoes_carregadas:
      if funcao.get_attribute("text") != '':
        # print(funcao.get_attribute("text"))
        funcao.click()
        # pausa pra respirar
        time.sleep(0.5)
        
        # coletando subfunções (ajax novamente)
        filtro_sub_funcao = driver.find_element_by_id('cboSubFuncao')
        sub_funcoes_carregadas = filtro_sub_funcao.find_elements_by_tag_name("option")
        
        # reiniciando dicionário
        sub_funcoes = {}
        for sub_funcao in sub_funcoes_carregadas:
          if sub_funcao.get_attribute("text") != '':
            # sub_funcoes.add(sub_funcao.get_attribute("text"))
            
            sub_funcao.click()
            #  hora do cafézim
            time.sleep(0.6)
            filtro_acoes = driver.find_element_by_id('cboAcao')
            acoes_carregadas = filtro_acoes.find_elements_by_tag_name("option")
            acoes = []
            for acao in acoes_carregadas:
              if acao.get_attribute("text") != '':
                acoes.append(acao.get_attribute("text"))
                # preparando dados pro pandas
                tabelas.append( [orgao.get_attribute("text"), funcao.get_attribute("text"), sub_funcao.get_attribute("text"), acao.get_attribute("text")] )
            
            # jogando ações na subfunção
            sub_funcoes[sub_funcao.get_attribute("text")] = acoes
        funcoes[funcao.get_attribute("text")] = sub_funcoes
    orgaos[orgao.get_attribute("text")] = funcoes       

tabelas_concatenadas = DataFrame (tabelas,columns=['ORGAO', 'FUNCAO', 'SUBFUNCAO', 'ACAO'])
tabelas_concatenadas.to_csv("orgao_funcao_subfuncao_acao.csv", index=False)

