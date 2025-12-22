# 📘 README - Sistema de previsão de demanda, necessidade de compras e gestão de estoque

## Visão Geral

Este projeto implementa um pipeline completo de previsão de demanda e gestão de estoque, totalmente modular e orientado a objetos. 
O objetivo é permitir que qualquer operação — restaurante, varejo, produção ou distribuição — consiga responder a quatro perguntas fundamentais:

- O que foi vendido?
- Quanto vou vender?
- Quanto preciso comprar?
- Quanto tenho disponível?

O sistema automatiza todo o processo, desde a leitura dos dados até a geração das necessidades de compra e atualização do estoque.

## Arquitetura do Projeto

A estrutura é organizada para manter clareza, modularidade e facilidade de manutenção:

```
/projeto_previsao/
│
├── data/
│   ├── estoque.csv
│   ├── vendas.csv
│   ├── compras.csv
│   ├── fornecedores.csv
│
├── modules/
│   ├── consumo.py
│   ├── previsao.py
│   ├── necessidade.py
│   ├── estoque.py
│
├── main.py
└── README.md
```

Cada módulo contém uma classe com responsabilidade única, seguindo boas práticas de arquitetura.

## Componentes principais: 

### 1️. ConsumoMedio (modules/consumo.py)
Responsável por analisar o histórico de vendas e calcular:

- consumo médio diário (7, 15, 30, 90 dias)
- tendência de consumo (subindo, caindo, estável)

Essa classe transforma dados brutos de vendas em indicadores úteis para previsão.

### 2️. PrevisaoDemanda (modules/previsao.py)
Responsável por gerar a previsão de demanda futura usando Facebook Prophet, um modelo estatístico avançado que captura:

- tendência
- sazonalidade semanal
- sazonalidade anual
- variações naturais de consumo

Ela estima o consumo futuro para um período definido (ex.: próximos 10 dias).

### 3️. NecessidadeCompras (modules/necessidade.py)
Responsável por calcular quanto precisa ser comprado, considerando:

- demanda prevista
- estoque atual
- compras futuras já realizadas
- prazo de entrega
- estoque alvo

A fórmula geral é:
necessidade = max(estoque_alvo - (estoque_atual + compras_futuras), 0)
Ou seja: só recomenda comprar se realmente faltar produto.

### 4️. EstoqueManager (modules/estoque.py)
Responsável por atualizar o estoque automaticamente:

- subtrai vendas do período
- soma compras recebidas
- mantém o estoque sempre atualizado

Isso garante que o sistema trabalhe sempre com dados reais.

## Fluxo Completo do Sistema 
O arquivo main.py orquestra todo o processo:

### 1. Carrega os dados:

- estoque
- vendas
- compras
- fornecedores

### 2. Atualiza o estoque:

- aplica vendas do último dia
- aplica compras recebidas

### 3. Calcula consumo médio para cada produto:

- consumo 7 dias
- consumo 15 dias
- consumo 30 dias
- consumo 90 dias
- tendência

### 4. Gera previsão de demanda:
Usando Prophet, estima o consumo futuro (ex.: próximos 15 dias).

### 5. Calcula necessidade de compras com base em:

- previsão
- estoque atual
- compras futuras
- estoque alvo

### 6. Gera relatórios:
- necessidade de compras
- estoque atualizado

## Próximos passos e melhorias

- criar um banco de dados (talvez SQL) para atualizar e armazenar melhor os dados
- automatizar alguns parquivos que ainda não foram automatizados nessa versão, que ainda devem ser atualizados manualmente (compras e fornecedores)

