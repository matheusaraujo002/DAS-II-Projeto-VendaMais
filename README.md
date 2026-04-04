# Plataforma de Inteligência Operacional - VendaMais

## 📌 Descrição do Projeto

Este projeto tem como objetivo desenvolver uma Plataforma de Inteligência Operacional para a empresa VendaMais Distribuidora Ltda.

A solução proposta automatiza a extração de dados do ERP corporativo, realiza o processamento e armazenamento em nuvem (Microsoft Azure) e disponibiliza dashboards interativos no Power BI para apoio à tomada de decisão.

---

## 🎯 Objetivos do Projeto

* Automatizar a extração de dados do ERP (vendas, estoque, financeiro e logística)
* Armazenar dados na nuvem com histórico e rastreabilidade
* Aplicar transformações e regras de negócio
* Disponibilizar dashboards interativos com KPIs
* Reduzir o tempo de geração de relatórios e melhorar a tomada de decisão

---

## 🧱 Visão Geral da Arquitetura

A solução segue o padrão de pipeline de dados:

**Ingestão → Armazenamento → Transformação → Consumo**

---

## 📊 Diagramas C4

### 🔹 Nível 1 – Contexto

O diagrama de contexto apresenta a visão geral do sistema, destacando:

* Usuários (Comercial, Estoque, Financeiro, Logística e Diretoria)
* Sistema ERP como fonte de dados
* Plataforma de Inteligência como núcleo do sistema
* Power BI como ferramenta de visualização

📁 Caminho: `docs/c4/nivel-1.png`

---

### 🔹 Nível 2 – Containers

O diagrama de containers detalha a arquitetura interna da solução:

* Serviço de Ingestão de Dados (Azure Functions - Python)
* Azure Blob Storage (armazenamento de dados brutos)
* Serviço de Transformação de Dados (Azure Functions - Python)
* Azure SQL Database (dados estruturados)
* Power BI (visualização de dashboards)

📁 Caminho: `docs/c4/nivel-2.png`

---

## 🏗️ Tecnologias Utilizadas

* Microsoft Azure

  * Azure Functions
  * Azure Blob Storage
  * Azure SQL Database
* Power BI
* Python

---

## 👥 Integrantes

* Yohann - (https://github.com/YohannPohl)
* Integrante 2 - link github
* Integrante 3 - link github

---

## 📁 Estrutura do Repositório

```
docs/
 ├── c4/
 │   ├── nivel-1.png
 │   ├── nivel-2.png
 │
 └── adr/
     ├── adr-001.md
     ├── adr-002.md

README.md
```

---

## ⚙️ Como navegar no projeto

* Acesse a pasta **docs/c4** para visualizar os diagramas arquiteturais
* Acesse a pasta **docs/adr** para entender as decisões técnicas do projeto

---

## 🔄 Processo de Desenvolvimento

O projeto foi desenvolvido seguindo boas práticas de versionamento:

* Uso de branches para desenvolvimento de funcionalidades
* Commits descritivos
* Uso de Pull Requests para revisão de código

---

## ⚠️ Observações

* Nenhuma credencial sensível foi adicionada ao repositório
* Os dados utilizados são apenas para fins acadêmicos
* O projeto segue os conceitos do modelo C4 para documentação arquitetural

---

## 📌 Conclusão

A plataforma proposta permite que a empresa VendaMais tenha acesso a dados atualizados e confiáveis, reduzindo o esforço manual na geração de relatórios e melhorando a tomada de decisões estratégicas.
