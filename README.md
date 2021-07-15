# **Simulador runcodes**
[![Py3.9](https://img.shields.io/badge/Python-3.9-blueviolet.svg)](https://docs.python.org/release/3.9.0/whatsnew/changelog.html#changelog)
[![license](https://img.shields.io/badge/license-MIT-blueviolet.svg)](https://github.com/biogui/simple-image-editor-with-openCV/blob/master/LICENSE)

Olá, eu sou o [Bio](https://github.com/biogui)!

E esse é um script em python para usuários do [run.codes](https://we.run.codes/) testarem seus programas localmente.

Obrigado por testar, feedbacks são bem vindos no meu telegram [(clica aqui)](https://t.me/gui_bio) :) .

## **Recursos** (exemplos no fim)
- ***Contagem de casos corretos***, mostrando o resultado em relação ao total de casos.

- ***Verificação de diferenças detalhada***, feita via comparação byte a byte da saída esperada com a saída gerada.

- ***Checagem de memória***, feita via comando `valgrind`, detalhando "bugs" em relação ao uso geral de memória.

## **Instalando**
Certifique-se de:
- Ter uma versão recente [(3.x.x)](https://www.python.org/downloads/) de  ***python*** instalada.
- Ter as seguintes ferramentas disponíveis em seu terminal Linux:
	- ***gcc***      - use `sudo apt install gcc`
	- ***valgrind*** - use `sudo apt install valgrind`
	- ***unzip***    - use `sudo apt install unzip`

Depois disso, basta clonar o repositório e rodar o ***setup.sh***:

```bash
git clone https://github.com/biogui/simulador-runcodes.git ~/.rcSim
```

```bash
cd ~/.rcSim
```

```bash
sh setup.sh
```

## **Uso**
Agora, em qualquer diretório, basta ***usar o comando `rcsim`***:
```bash
rcsim <caminhoDoPrograma> <caminhoDosTestes> <caminhoDosArquivos(opcional)>
```

***Obs.:*** *`rcsim` pode ser trocado por `python3 rcSim.py`, mas é necessário que o script do simulador esteja na pasta atual.*

#### **O `<caminhoDoPrograma>`**
Esse simulador suporta dois tipos de programas: aqueles com um único arquivo .c e aqueles compilados/executados via arquivo Makefile. Em `<caminhoDoPrograma>` deve ser passado o caminho (absoluto ou relativo) desse arquivo .c ou Makefile.

#### **O `<caminhoDosTestes>`**
Esse simulador suporta dois modos de adição de testes: via uma pasta contendo as entradas (arquivos do tipo .in) e as respectivas saídas esperadas (arquivos do tipo .out) ou um arquivo .zip arquivo de mesmo conteúdo. Em `<caminhoDosTestes>` deve ser passado o caminho (absoluto ou relativo) dessa pasta ou desse arquivo .zip.

#### **O `<caminhoDosArquivos>` (opcional)**
Esse simulador suporta dois modos de adição de arquivos para execução, caso necessário: via uma pasta contendo os arquivos necessários ou um arquivo .zip arquivo de mesmo conteúdo. Em `<caminhoDosTestes>` deve ser passado o caminho (absoluto ou relativo) dessa pasta ou desse arquivo .zip.

***Obs.:*** *`<caminhoDosArquivos>` pode ser igual ao `<caminhoDosArquivos>`, o simulador organiza os testes e arquivos em novas pastas ("rcSimTestes", "rcSimArquivos" e "rcSimSaidas") criadas durante execução do script. Essas pastas não são deletadas automaticamente ao fim da execução, para, caso ocorrá algum erro, o usuário possa verificar as saídas. Ao fim do uso basta rodar `rm -rf rcSim*` para limpar os dados gerados pelo simulador.*

## **Notas**
- ***Priorize rodar o simulador na pasta onde está contido seu programa ou arquivo Makefile***.
- ***Evite matar o processo durante sua execução***. Interrupções inesperadas podem gerar problemas futuros, seja paciente.
- ***Atente-se à organização dos casos testes na pasta ou arquivo .zip usado***. Certifique-se de que o número de entradas é equivalente ao número de saídas esperadas e de que exista a respectiva saída "x.out" para cada entrada "x.in".

## **Exemplos**
- ***Contagem de casos corretos***
&nbsp;&nbsp;&nbsp;&nbsp;![](https://i.imgur.com/yK2ZW3n.png)
&nbsp;&nbsp;&nbsp;&nbsp;![](https://i.imgur.com/j8BMdFU.png)
&nbsp;&nbsp;&nbsp;&nbsp;![](https://i.imgur.com/YfZo5cH.png)

- ***Verificação de diferenças detalhada***
&nbsp;&nbsp;&nbsp;&nbsp;![](https://i.imgur.com/6cOLKSz.png)
&nbsp;&nbsp;&nbsp;&nbsp;![](https://i.imgur.com/TBF7y1M.png)
&nbsp;&nbsp;&nbsp;&nbsp;![](https://i.imgur.com/WVzuNg0.png)
&nbsp;&nbsp;&nbsp;&nbsp;![](https://i.imgur.com/Bo2ePeO.png)
&nbsp;&nbsp;&nbsp;&nbsp;![](https://i.imgur.com/7ypCRYn.png)

- ***Checagem de memória***
&nbsp;&nbsp;&nbsp;&nbsp;![](https://i.imgur.com/Ih5lxEX.png)
&nbsp;&nbsp;&nbsp;&nbsp;![](https://i.imgur.com/lUGTpv7.png)
&nbsp;&nbsp;&nbsp;&nbsp;![](https://i.imgur.com/qrsGW34.png)
&nbsp;&nbsp;&nbsp;&nbsp;![](https://i.imgur.com/Sag8zsJ.png)
&nbsp;&nbsp;&nbsp;&nbsp;![](https://i.imgur.com/NxivAag.png)
