## 🍀 Arquitetura do Sistema

A arquitetura do **Motorcycle Detection Dashboard** foi projetada para integrar de forma harmônica três camadas principais:  
1. **Processamento de vídeo e detecção de motocicletas** por meio do modelo **YOLOv8**.  
2. **Armazenamento dos dados** de detecção em um banco de dados relacional (**Oracle SQL** ou **SQLite**, em modo alternativo).  
3. **Visualização interativa e análise** através de um **dashboard desenvolvido em Streamlit**.

## 🍀 Fluxo de funcionamento

1. O usuário realiza o **upload** de um vídeo pela interface do dashboard.  
2. O sistema processa o vídeo, **identifica motocicletas** frame a frame e gera um arquivo anotado com as detecções.  
3. Cada detecção é **registrada no banco de dados**, contendo ID, coordenadas, confiança e data/hora.  
4. O dashboard apresenta os **resultados em tempo real**, incluindo gráficos, KPIs e histórico de execuções.  
5. O usuário pode **baixar relatórios CSV ou Excel** diretamente da interface.

## 🍀 Representação simplificada
📹 Upload do vídeo → 🧠 YOLOv8 (Detecção) → 💾 Banco de Dados Oracle/SQLite → 📊 Dashboard Streamlit

## 🍀 Dataset e Treinamento (Roboflow + YOLOv8)

O **dataset** utilizado neste projeto foi criado e anotado na plataforma **Roboflow**, contendo imagens de motocicletas em diferentes ângulos, distâncias e ambientes, garantindo maior diversidade e precisão durante o treinamento.

Após o processo de **rotulagem e limpeza dos dados**, o conjunto foi exportado no formato **YOLOv8** e dividido entre três subconjuntos:  
- **70%** para treinamento  
- **20%** para validação  
- **10%** para teste  

O modelo **YOLOv8** foi então treinado localmente utilizando GPU, com os seguintes parâmetros principais:

### 🍀 Comando de treinamento
```bash
yolo task=detect mode=train model=yolov8n.pt data=roboflow_dataset.yaml epochs=50 imgsz=640
```
## 🍀 Funcionalidades Principais

O **Motorcycle Detection Dashboard** reúne diversas funcionalidades que integram inteligência artificial, banco de dados e visualização de forma fluida e intuitiva.  
A seguir estão listadas as principais características do sistema:

### 🍀 Funcionalidades gerais

- **Upload de vídeo**: aceita arquivos nos formatos `.mp4`, `.avi`, `.mov` e `.mkv`.  
- **Detecção automática (YOLOv8)**: identifica motocicletas em cada frame do vídeo.  
- **Parâmetros configuráveis**: ajuste de *confidence*, *IoU* e *image size* diretamente na interface.  
- **Geração de vídeo anotado**: salva automaticamente um arquivo `_annotated.mp4` com as detecções marcadas.  
- **KPI visual**: exibe em tempo real o número total de motocicletas detectadas.  
- **Banco de dados Oracle/SQLite**: registra cada detecção, com ID, coordenadas, confiança e data/hora.  
- **Histórico e gráficos**: apresenta uma lista completa das detecções e um gráfico interativo com a distribuição diária.  
- **Exportações automáticas**: gera relatórios em **CSV** e **Excel** com os dados de cada processamento.  
- **Compatibilidade com GPU (CUDA)**: utiliza aceleração de hardware, quando disponível, para maior desempenho.  
- **Tema visual Mottu**: paleta de cores moderna e minimalista (`#040405`, `#34D231`, `#005A23`).  

### 🍀 Tabela de resumo

| Função                         | Descrição                                                       | Local no dashboard             |
|--------------------------------|-----------------------------------------------------------------|--------------------------------|
| Upload de vídeo                | Envio de arquivos de vídeo                                      | Sidebar → *Upload video*       |
| Detecção YOLOv8                | Processa e identifica motocicletas                              | Botão *Run Detection*          |
| Ajustes de parâmetros          | Define *confidence*, *IoU* e tamanho de imagem                  | Sidebar                        |
| Vídeo anotado                  | Salva o vídeo com *bounding boxes*                              | Pasta `outputs/`               |
| KPI visual                     | Mostra o total de motocicletas detectadas                       | Card superior no dashboard     |
| Histórico e gráfico            | Exibe registros e distribuição diária de detecções              | Seção inferior do dashboard    |
| Banco de dados Oracle/SQLite   | Armazena todas as informações das detecções                     | Tabela `TB_MOTOS`              |
| Exportações (CSV/Excel)        | Gera relatórios automáticos                                     | Botões *Download*              |
| GPU (opcional)                 | Acelera o processamento se disponível                           | Execução automática             |
| Tema Mottu                     | Layout visual com tons de preto e verde                         | Interface principal             |

Essas funcionalidades tornam o dashboard **completo, responsivo e de fácil uso**, oferecendo uma visão clara das operações e resultados.

## 🍀 Estrutura do Projeto

O projeto foi organizado de forma modular, permitindo fácil manutenção, expansão e integração com outras ferramentas.  
Abaixo está a estrutura de diretórios e arquivos, com uma breve explicação sobre a função de cada um:
### 🍀 Descrição resumida dos diretórios

| Diretório / Arquivo | Descrição |
|---------------------|------------|
| `app.py` | Contém toda a lógica principal do dashboard, detecção, banco e visualização. |
| `config.yaml` | Define parâmetros do modelo YOLOv8 e credenciais do banco Oracle. |
| `database/` | Scripts SQL para criação e consultas da tabela de detecção. |
| `models/` | Armazena o modelo YOLOv8 (`best.pt`) treinado no Roboflow. |
| `outputs/` | Gera os vídeos anotados, arquivos CSV, Excel e banco local SQLite. |
| `assets/` | Contém recursos visuais como logos e ícones. |
| `README.md` | Documentação técnica e instruções completas do projeto. |

Essa estrutura modular facilita o **entendimento do fluxo**, a **organização do código** e o **gerenciamento dos resultados**.

## 🍀 Requisitos de Sistema

Para executar o **Motorcycle Detection Dashboard** corretamente, é necessário garantir que o ambiente possua as versões mínimas de software, bibliotecas e dependências adequadas.  
Abaixo estão listados os principais requisitos do sistema:

### 🍀 Requisitos mínimos

| Item | Versão / Observação |
|------|----------------------|
| **Python** | 3.10 ou superior |
| **Streamlit** | 1.39 ou superior |
| **Ultralytics (YOLOv8)** | 8.2 ou superior |
| **Pandas** | 2.2 ou superior |
| **OpenCV** | 4.10 ou superior |
| **Oracle Database** | `oracle.fiap.com.br / ORCL` |
| **SQLite** | Utilizado como fallback local |
| **FFmpeg (opcional)** | Necessário para reprodução de vídeo no navegador |
| **GPU CUDA (opcional)** | Aceleração do modelo YOLOv8 |
| **Sistema Operacional** | Windows 10+, macOS ou Linux |

### 🍀 Principais dependências

O arquivo `requirements.txt` contém todas as bibliotecas necessárias para a execução do projeto:

```text
streamlit==1.39.0
pandas==2.2.2
opencv-python-headless==4.10.0.84
plotly==5.23.0
sqlalchemy==2.0.23
oracledb==2.1.1
ultralytics==8.2.91
xlsxwriter==3.2.0
pyyaml==6.0.1
torch==2.4.1
```
## 🍀 Instalação Passo a Passo

A instalação do **Motorcycle Detection Dashboard** é simples e pode ser realizada em poucos comandos.  
Siga as etapas abaixo para configurar o ambiente e executar o projeto corretamente.

---

### 🍀 1. Clonar o repositório

Baixe o código-fonte do projeto diretamente do GitHub:

```bash
git clone https://github.com/SEU-USUARIO/dashboardPro.git
cd dashboardPro
```
### 🍀 2. Instalar as dependências
Certifique-se de estar com o ambiente virtual ativo e instale todas as bibliotecas necessárias:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
### 🍀 3. Adicionar o modelo YOLOv8
Coloque o arquivo do modelo treinado (best.pt) dentro da pasta:
```bash
models/
└── best.pt
```
```text
Este arquivo é o resultado do treinamento feito no Roboflow e YOLOv8.
Ele é essencial para que a detecção funcione corretamente.
```
🍀 4. Configurar o banco de dados (opcional)
- Por padrão, o sistema utiliza Oracle SQL.
- Se desejar testar localmente sem conexão, o dashboard usará o SQLite automaticamente.
- Credenciais e opções de banco estão no arquivo config.yaml.

🍀 5. Executar o dashboard
Após configurar tudo, basta rodar o comando:
```bash
streamlit run app.py
```
👉 http://localhost:8501

## 🍀 Configuração (config.yaml)
O arquivo **`config.yaml`** é responsável por armazenar as principais configurações do sistema, incluindo o caminho do modelo YOLOv8, os parâmetros de inferência e as credenciais de acesso ao banco de dados Oracle.  
Todas as definições são **carregadas automaticamente** quando o aplicativo é iniciado.

---
### 🍀 Estrutura do arquivo `config.yaml`

```yaml
model_path: "models/best.pt"     # Caminho do modelo YOLOv8
conf: 0.5                        # Nível de confiança mínima para detecção
iou: 0.45                        # Valor do IoU (Intersection over Union)
imgsz: 640                       # Tamanho da imagem utilizada na inferência
sqlite_path: "outputs/results.db"  # Caminho do banco local (SQLite)

oracle:
  enabled: true                  # Define se o Oracle será utilizado
  user: "RM554921"               # Usuário de acesso ao banco Oracle
  password: "250701"             # Senha do usuário Oracle
  dsn: "oracle.fiap.com.br"      # Endereço de conexão
  sid: "ORCL"                    # Identificador do serviço Oracle
  table: "TB_MOTOS"              # Nome da tabela onde os dados serão armazenados
```
## 🍀 Execução do Dashboard

Após configurar o ambiente e o arquivo `config.yaml`, a execução do **Motorcycle Detection Dashboard** é simples e direta.  
Basta utilizar o comando abaixo para iniciar o sistema:

---

### 🍀 1. Executar o aplicativo

No terminal (com o ambiente virtual ativo), digite:

```bash
streamlit run app.py
```
```text
Local URL: http://localhost:8501
Network URL: http://<seu_ip_local>:8501
```
## 🍀 Exportações e Saídas

O **Motorcycle Detection Dashboard** gera automaticamente uma série de arquivos e registros após cada processamento de vídeo.  
Essas exportações permitem acompanhar o histórico das detecções, realizar análises e armazenar os resultados de forma organizada.

---

### 🍀 Tipos de arquivos gerados

Após cada execução de detecção, o sistema cria os seguintes arquivos:

| Tipo de Arquivo | Extensão | Descrição | Local |
|------------------|-----------|------------|--------|
| **Vídeo anotado** | `.mp4` | Vídeo original com *bounding boxes* marcando as motocicletas detectadas. | `outputs/` |
| **Relatório CSV** | `.csv` | Tabela com todos os registros de detecção (ID, coordenadas, confiança e data/hora). | `outputs/` |
| **Relatório Excel** | `.xlsx` | Versão formatada do relatório CSV, gerada automaticamente via *XlsxWriter*. | `outputs/` |
| **Banco de dados local** | `.db` | Base de dados SQLite usada como fallback quando o Oracle não está acessível. | `outputs/` |

---


