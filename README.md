<h1 align="center">Case - Estágio em IA - Escalabilidade Operacional (Cromai)</h1>

## Descrição do Projeto
<p align="center">Este projeto consiste em um sistema de monitoramento web para sistemas Linux que rastreia o uso da CPU, Disco e Memória em tempo real. Ele utiliza uma interface HTML/CSS com um layout de painel separado para cada componente. O servidor é hospedado no Flask, e as atualizações em tempo real são realizadas com JavaScript. Os dados são obtidos via SSH e comandos de shell no mainframe e armazenados em um banco de dados SQLite3 para fins de histórico. Para garantir a segurança, a autenticação é feita por meio de chaves SSH. Este sistema oferece uma solução completa para monitorar recursos em sistemas Linux de forma eficaz e segura. </p>

### 🚀 Começando

Essas instruções permitirão que você obtenha uma cópia do projeto em operação na sua máquina local.

### 📋 Pré-requisitos
# Configurar a autenticação baseada em chaves SSH
## Gere um par de chaves SSH:

```
ssh-keygen
```
#### O utilitário irá solicitar que seja selecionado um local para as chaves que serão geradas. Por padrão, as chaves serão armazenadas no diretório ~/.ssh dentro do diretório home do seu usuário. A chave privada será chamada de id_rsa e a chave pública associada será chamada de id_rsa.pub.
```
Generating public/private rsa key pair.
Enter file in which to save the key (/home/username/.ssh/id_rsa):
```

#### Pressione ENTER para salvar o par de chaves no sub-diretório .ssh/ no seu diretório home, ou especifique um caminho alternativo.


## Copiando a sua chave pública

## Copiando sua chave pública usando o ssh-copy-id
```
ssh-copy-id username@remote_host
```
#### Pode ser que apareça uma mensagem como esta:
```
The authenticity of host '111.111.11.111 (111.111.11.111)' can't be established.
ECDSA key fingerprint is fd:fd:d4:f9:77:fe:73:84:e1:55:00:ad:d6:6d:22:fe.
Are you sure you want to continue connecting (yes/no)? yes
```
#### Isso significa que seu computador local não reconhece o host remoto. Isso acontecerá na primeira vez que você se conectar a um novo host. Digite “yes” e pressione ENTER para continuar.

#### Em seguida, o utilitário irá analisar sua conta local em busca da chave id_rsa.pub que criamos mais cedo. Quando ele encontrar a chave, irá solicitar a senha da conta do usuário remoto;

```
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
username@111.111.11.111's password:
```
#### Digite a senha (sua digitação não será exibida para fins de segurança) e pressione ENTER.
#### Você verá um resultado que se parece com este:
```
Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'username@111.111.11.111'"
and check to make sure that only the key(s) you wanted were added.
```
## Copiando sua chave pública manualmente

#### Se não tiver o ssh-copy-id disponível, erá necessário completar o processo acima manualmente.

#### O conteúdo do seu arquivo id_rsa.pub precisará ser adicionado a um arquivo em ~/.ssh/authorized_keys em sua máquina remota de alguma maneira.

#### Para exibir o conteúdo de sua chave id_rsa.pub, digite o seguinte em seu computador local:

```
cat ~/.ssh/id_rsa.pub
```

#### Você verá o conteúdo da chave, que deve ser parecido com este:

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCqql6MzstZYh1TmWWv11q5O3pISj2ZFl9HgH1JLknLLx44+tXfJ7mIrKNxOOwxIxvcBF8PXSYvobFYEZjGIVCEAjrUzLiIxbyCoxVyle7Q+bqgZ8SeeM8wzytsY+dVGcBxF6N4JS+zVk5eMcV385gG3Y6ON3EG112n6d+SMXY0OEBIcO6x+PnUSGHrSgpBgX7Ks1r7xqFa7heJLLt2wWwkARptX7udSq05paBhcpB0pHtA1Rfz3K2B+ZVIpSDfki9UVKzT8JUmwW6NNzSgxUfQHGwnW7kj4jp4AT0VZk3ADw497M2G/12N0PPB5CnhHf7ovgy6nL1ikrygTKRFmNZISvAcywB9GVqNAVE+ZHDSCuURNsAInVzgYo9xgJDW8wUw2o8U77+xiFxgI5QSZX3Iq7YLMgeksaO4rBJEa54k8m5wEiEE1nUhLuJ0X/vh2xPff6SQ1BL/zkOhvJCACK6Vb15mDOeCSq54Cr7kvS46itMosi/uS66+PujOO+xt/2FWYepz6ZlN70bRly57Q06J+ZJoc9FfBCbCyYH7U/ASsmY095ywPsBo1XQ9PqhnN1/YOorJ068foQDNVpm146mUpILVxmq41Cj55YKHEazXGsdBIbXWhcrRf4G2fJLRcGUr9q8/lERo9oxRm5JFX6TCmj6kmiFqv+Ow9gI0x8GvaQ== demo@test
```
#### Crie um diretório 

```
mkdir -p ~/.ssh
```

#### Agora, você pode criar ou modificar o arquivo authorized_keys dentro deste diretório. Você pode adicionar o conteúdo do seu arquivo id_rsa.pub ao final do arquivo authorized_keys, criando-o se for necessário, usando este comando:

```
echo public_key_string >> ~/.ssh/authorized_keys
```
#### No comando acima, substitua o public_key_string pelo resultado do comando cat ~/.ssh/id_rsa.pub que você executou no seu sistema local. Ela deve começar com ssh-rsa AAAA....


## Autenticando-se ao seu servidor Ubuntu usando chaves SSH

#### Se tiver completado um dos procedimentos acima com êxito, você deve conseguir fazer login no host remoto.

```
ssh username@remote_host
```
#### Se essa é a primeira vez que você se conecta a este host (caso tenha usado o último método acima), pode ser que veja algo como isso:

```
Output
The authenticity of host '203.0.113.1 (203.0.113.1)' can't be established.
ECDSA key fingerprint is fd:fd:d4:f9:77:fe:73:84:e1:55:00:ad:d6:6d:22:fe.
Are you sure you want to continue connecting (yes/no)? yes
```
#### Isso significa que seu computador local não reconhece o host remoto. Digite “yes” e então pressione ENTER para continuar.

#### Se não forneceu uma frase secreta para sua chave privada, você será logado imediatamente. Caso tenha fornecido uma frase secreta para a chave privada quando criou a chave, você será solicitado a digitá-la agora (note que sua digitação não será exibida na sessão do terminal como medida de segurança). Após a autenticação, uma nova sessão de shell deve abrir para você com a conta configurada no servidor Ubuntu.


### 🔧 Instalação

### Abra o arquivo na pasta /Case_Cromai 

## Criando um ambiente virtual com Virtualenv

#### Utilize o comando abaixo para instalar a virtualenv:
```
pip install virtualenv
```
#### Criando uma virtualenv:
```
virtualenv .venv
```
#### Ativando a virtualenv
```
source .venv/bin/activate
```
## Instalar bibliotecas

```
pip install -r requirements.txt
```
### ⚙️ Executando

#### Abra o primeiro terminal em /Case_Cromai

#### Execute o comando:
```
python main.py
```
#### Abra o segundo terminal também em /Case_Cromai
#### Execute o comando:
```
python dados_mainframe.py
```
#### Abra o endereço abaixo no navegador:
```
http://localhost:5000
```
#### A página abrirá em uma tela de login, utilize como hostname o ip local da máquina e no username utilize o usuário da máquina 

## Caso enfremte algum problena na execução do código estou à disposição em izadora.mirandar@hotmail.com

