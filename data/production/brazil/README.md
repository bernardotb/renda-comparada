# CDF brasileira de renda — PNAD Contínua 2025

Este diretório contém uma representação agregada da distribuição empírica brasileira validada nas Fases 1D e 1E.

## O que o artefato representa

O arquivo `brazil-income-cdf-2025.json` representa **pessoas elegíveis**, ponderadas por `V1032`, segundo o rendimento domiciliar per capita mensal real em **preços médios de 2025**.

Ele não representa domicílios, trabalhadores, salários individuais, patrimônio ou riqueza líquida.

## Estrutura

O JSON contém três vetores paralelos:

- `rdpc`: valores únicos de RDPC, em ordem crescente;
- `weightAt`: peso da população exatamente naquele valor;
- `cumAtOrBelow`: peso acumulado até e inclusive aquele valor.

Para o índice `i`, o peso estritamente abaixo é zero quando `i = 0` e `cumAtOrBelow[i - 1]` nos demais casos. Assim, não é necessário duplicar esse vetor no artefato.

## Semântica do lookup

Entrada:

```text
RDPC mensal em reais, a preços médios de 2025
```

Saída:

```text
shareBelow(x)      = peso com RDPC < x / peso total
shareAtOrBelow(x)  = peso com RDPC <= x / peso total
topShare(x)        = 1 - shareBelow(x)
```

A CDF é uma função em degraus. Não existe interpolação, extrapolação paramétrica ou ordenação fictícia de pessoas empatadas.

## Regeneração

A partir da raiz do repositório:

```powershell
python scripts/data/brazil/validate_brazil_cdf.py
```

O comando verifica o checksum do dataset intermediário, gera duas CDFs independentes, compara os hashes, executa testes e somente então promove o artefato validado.

## Bloqueio temporal

O artefato **não pode ser ligado diretamente ao formulário atual** enquanto `USER_INCOME_PRICE_ALIGNMENT_METHOD` estiver pendente. Uma renda corrente precisa ser convertida para a mesma referência monetária da distribuição, ou a distribuição precisa ser atualizada por método aprovado. Nenhuma dessas operações é realizada nesta fase.

O arquivo não está em `public/`, não é importado por `src/` e não altera o site publicado.
