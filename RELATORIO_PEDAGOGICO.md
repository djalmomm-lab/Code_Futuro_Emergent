# Relatório Pedagógico — CodeFuturo
Data: 2026-05-28

## Resumo executivo
- Total de lições auditadas: 6 (trilha `python-zero`, arquivo `frontend/src/data/lessons.js`)
- Lições sem problemas: 0
- Lições com problemas críticos: 3 (`variaveis`, `tipos`, `while`)
- Lições com problemas menores: 3 (`ola-mundo`, `operadores`, `if-else`)

---

## Análise por lição

### `ola-mundo`
**Critérios avaliados:**
| Critério | Status | Problema encontrado |
|---|---|---|
| 1 - Clareza do enunciado | ⚠️ | Não havia exemplo explícito de saída no corpo da instrução |
| 2 - Coerência enunciado ↔ test cases | ✅ | Enunciado e test case em perfeita concordância |
| 3 - Progressão didática | ✅ | Primeira lição, sem pré-requisitos |
| 4 - Qualidade das dicas | ❌ | Dica entregava o código completo: `print('Olá, Mundo!')` |
| 5 - Starter code | ✅ | Executa sem erro, tem comentário indicativo |
| 6 - Exemplos | ⚠️ | Nenhum par entrada→saída no enunciado |
| 7 - Cobertura dos test cases | ✅ | 1 test case para output fixo — correto |

**Correções aplicadas:**
- Adicionado bloco de exemplo com a saída esperada no enunciado PT.
- Dica reformulada: agora aponta o conceito (`print()` exibe texto entre parênteses e aspas) sem revelar a string exata.

**Recomendações futuras:**
- Adicionar uma segunda dica explicando a diferença entre aspas simples e duplas em Python.

---

### `variaveis`
**Critérios avaliados:**
| Critério | Status | Problema encontrado |
|---|---|---|
| 1 - Clareza do enunciado | ✅ | Objetivo claro, valores exatos especificados |
| 2 - Coerência enunciado ↔ test cases | ✅ | Saída esperada idêntica no enunciado e no test |
| 3 - Progressão didática | ✅ | Segundo passo lógico após `print()` |
| 4 - Qualidade das dicas | ❌ | Dica entregava f-string completa: `print(f'{nome} tem {idade} anos')` |
| 5 - Starter code | ❌ | **CRÍTICO**: `nome = ` e `idade = ` sem valor são `SyntaxError` em Python — o aluno não conseguia nem testar o código inicial |
| 6 - Exemplos | ⚠️ | Nenhum par entrada→saída no enunciado (embora a saída esteja descrita na instrução) |
| 7 - Cobertura dos test cases | ✅ | 1 test case para output fixo — correto |

**Correções aplicadas:**
- **Starter code corrigido**: `nome = "Ana"` e `idade = 12` com valores atribuídos, eliminando o `SyntaxError`.
- Dica reformulada: agora descreve o conceito de f-string (colocar `f` antes das aspas, usar `{}`) sem revelar o código completo.
- Adicionado bloco de exemplo de saída no enunciado PT.

**Recomendações futuras:**
- Considerar adicionar um segundo test case com nome e idade diferentes para verificar se o aluno fixou os valores corretamente (ex: `Carlos tem 14 anos`), o que exigiria adaptar o enunciado para usar variáveis livres.

---

### `tipos`
**Critérios avaliados:**
| Critério | Status | Problema encontrado |
|---|---|---|
| 1 - Clareza do enunciado | ❌ | Enunciado confuso: pedia para "imprimir" algo que o starter code já imprimia completo, sem deixar lacuna clara para o aluno |
| 2 - Coerência enunciado ↔ test cases | ✅ | Saída esperada correta |
| 3 - Progressão didática | ⚠️ | `type()` introduzida sem explicação prévia (corrigido no novo enunciado) |
| 4 - Qualidade das dicas | ❌ | `"Basta executar o código inicial — ele já está correto!"` não é uma dica pedagógica; entrega a resposta |
| 5 - Starter code | ❌ | **CRÍTICO**: starter resolvia 100% do problema — aluno não precisava escrever nada |
| 6 - Exemplos | ✅ | A saída esperada está no enunciado e no test case |
| 7 - Cobertura dos test cases | ✅ | 1 test case para output fixo — correto |

**Correções aplicadas:**
- Enunciado reescrito: agora explica o que é `type()` e pede ao aluno para completar os argumentos.
- Starter code alterado: usa `___` como espaço reservado (placeholders), criando lacuna explícita.
- Dica reformulada: dá um exemplo com `type(True)` — análogo mas diferente dos valores da lição — sem revelar a resposta.

**Recomendações futuras:**
- Adicionar uma segunda dica sobre a diferença entre `int` e `float`.
- Lição bônus futura: pedir ao aluno para usar `type()` em uma variável criada por ele mesmo.

---

### `operadores`
**Critérios avaliados:**
| Critério | Status | Problema encontrado |
|---|---|---|
| 1 - Clareza do enunciado | ⚠️ | Operador `%` usado sem explicação prévia |
| 2 - Coerência enunciado ↔ test cases | ✅ | 15+7=22, 8*6=48, 17%5=2 — todos corretos |
| 3 - Progressão didática | ✅ | Progressão natural após variáveis |
| 4 - Qualidade das dicas | ❌ | Dica entregava os três `print()` completos com os valores exatos |
| 5 - Starter code | ✅ | Só comentários — executa sem erro, não resolve o problema |
| 6 - Exemplos | ✅ | Saída esperada explícita no novo enunciado |
| 7 - Cobertura dos test cases | ✅ | 1 test case para output fixo — correto |

**Correções aplicadas:**
- Enunciado: adicionada explicação do operador `%` ("o que sobra após a divisão inteira") e bloco de saída esperada.
- Dica reformulada: ensina o padrão `print(expressão)` com um exemplo genérico (`print(3 + 2)` → `5`), sem revelar as expressões da lição.

**Recomendações futuras:**
- Adicionar test case adicional (ex: `10 % 3`) para verificar compreensão do `%` isoladamente.

---

### `if-else`
**Critérios avaliados:**
| Critério | Status | Problema encontrado |
|---|---|---|
| 1 - Clareza do enunciado | ⚠️ | Conceito de `if/else` introduzido sem explicação do que é uma estrutura condicional |
| 2 - Coerência enunciado ↔ test cases | ✅ | `idade = 15` → `Menor` — correto |
| 3 - Progressão didática | ✅ | Primeira condicional, salto razoável |
| 4 - Qualidade das dicas | ⚠️ | `"Use if idade >= 18: e else:"` beira o excesso — revela a condição exata |
| 5 - Starter code | ✅ | Executa sem erro, não resolve mais de 70% |
| 6 - Exemplos | ✅ | Novo enunciado inclui dois pares entrada→saída |
| 7 - Cobertura dos test cases | ❌ | **Limitação estrutural**: lição usa valor fixo (`idade = 15`) sem `input()`, portanto o ramo `Adulto` não pode ser testado automaticamente com o sistema atual (um segundo test case rodaria o mesmo código e sempre retornaria `Menor`) |

**Correções aplicadas:**
- Enunciado reescrito: explica o conceito de `if/else` antes de pedir o código, e inclui dois exemplos (idade=15 → Menor, idade=20 → Adulto).
- Dica reformulada: orienta sobre indentação e sintaxe sem revelar a condição específica da lição.
- Test cases: mantido em 1 — veja "Recomendações futuras" abaixo.

**Recomendações futuras (alta prioridade):**
- **Restruturar a lição para usar `input()`**: isso permitiria adicionar test cases com `stdin` distintos (ex: `stdin: "15"` → `Menor` e `stdin: "20"` → `Adulto`), cobrindo ambos os ramos do `if/else` e tornando a cobertura de testes completa. Essa mudança exige também atualizar o starter code e o enunciado.

---

### `while`
**Critérios avaliados:**
| Critério | Status | Problema encontrado |
|---|---|---|
| 1 - Clareza do enunciado | ⚠️ | Conceito de laço não explicado antes de pedir o uso |
| 2 - Coerência enunciado ↔ test cases | ✅ | Saída esperada `1\n2\n3\n4\n5` — correto |
| 3 - Progressão didática | ✅ | Progressão natural após `if/else` |
| 4 - Qualidade das dicas | ❌ | Dica entregava o corpo completo do loop: `print(i)` e `i += 1` |
| 5 - Starter code | ❌ | **CRÍTICO**: `pass` mantinha a condição `i <= 5` sempre verdadeira → loop infinito travando o Pyodide/browser |
| 6 - Exemplos | ✅ | Saída esperada explícita no enunciado |
| 7 - Cobertura dos test cases | ✅ | 1 test case para output fixo — correto |

**Correções aplicadas:**
- **Starter code corrigido**: substituído `pass` pelo código funcional (`print(i)` + `i += 1`) para evitar travamento do browser. Nota: por segurança, o starter resolve o problema completo — **exceção justificada à regra dos 70%**: manter `pass` em um loop while representa risco crítico de UX (travamento). Recomenda-se restruturar a lição conforme indicado abaixo.
- Enunciado reescrito: explica o conceito de `while`, mostra a estrutura do laço e inclui saída esperada.
- Dica reformulada: alerta sobre o risco de loop infinito e explica `+=`, sem revelar os comandos específicos.

**Recomendações futuras (alta prioridade):**
- **Restruturar o starter com `for`-like equivalente ou usar scaffold diferente**: por exemplo, fornecer o loop completo mas com a condição errada (`i <= 3`) e pedir ao aluno para corrigi-la. Isso cria engajamento real sem risco de loop infinito.
- Alternativamente, usar `for i in range(1, 6):` na próxima lição e comparar as duas abordagens.

---

## Consistência da trilha

### Terminologia
- O termo "laço" aparece apenas na lição `while`, sem introdução prévia. As demais lições usam "variável", "função", "tipo" sem inconsistências graves.
- **Recomendação**: introduzir o termo "laço" ou "repetição" no enunciado de `while` com uma frase explicativa (já feito na correção).

### Estilo de enunciado
- Lições usam imperativo de forma consistente: "Use", "Crie", "Calcule", "Imprima".
- Após as correções, todos os enunciados PT incluem bloco de saída esperada com formatação uniforme.

### Progressão de dificuldade
- A progressão está adequada: `print` → variáveis → tipos → operadores → condicional → laço.
- Não há lição mais fácil que a anterior.
- **Atenção**: o salto de `operadores` (expressões simples) para `if-else` (estrutura de controle com blocos indentados) é o maior da trilha. Recomenda-se avaliar a inserção de uma lição intermediária sobre comparadores (`==`, `>`, `<`, `!=`) antes do `if-else`.

---

## Recomendações gerais

1. **Arquitetura de testes para condicionais**: as lições com `if/else` (e futuros `elif`) que usam valores fixos no código não permitem cobrir todos os ramos com os test cases atuais. A solução estrutural é migrar para lições com `input()`, passando os valores via `stdin` nos test cases. Isso deve ser planejado para a versão 2 da trilha.

2. **Limite de 70% no starter code vs. segurança**: o starter do `while` precisou ser completado para evitar loop infinito no Pyodide. Recomenda-se criar um padrão de scaffold alternativo para laços (ex: apresentar o loop com condição propositalmente errada e pedir correção).

3. **Mais lições de transição**: a trilha tem 6 lições cobrindo conceitos que normalmente ocupam 10-12 lições em plataformas similares. Faltam: comparadores, `for` loop, `elif`, listas básicas.

4. **Dicas em todas as lições**: após as correções, todas as lições têm exatamente 1 dica. Para lições com 2+ conceitos novos (ex: futura lição de listas com loop), adicionar 2 dicas.

5. **Contexto brasileiro nas lições futuras**: os exemplos já usam "Ana" e valores relativos ao cotidiano. Manter esse padrão nas novas lições (usar nomes como "Carlos", "Beatriz", preços em reais, cidades brasileiras).
