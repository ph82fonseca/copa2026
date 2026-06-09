# ⚽ Calendário Copa 2026 no iPhone — Setup em 5 passos
## (Zero manutenção depois de configurado)

---

## O que você vai ter no final

- Todos os **104 jogos** da Copa no Calendário do seu iPhone
- Eventos com **estádio, fato do jogo, escalações** e lembrete de 15 min
- Mata-mata que **exibe as seleções certas automaticamente** conforme a Copa avança
- **Nada a fazer manualmente** — o calendário se atualiza sozinho a cada 30 min

---

## Passo 1 — Criar conta no GitHub (grátis, 2 min)

1. Abra [github.com](https://github.com) no celular ou computador
2. Clique em **Sign up** → preencha e-mail, senha, nome de usuário
3. Confirme o e-mail

> Se já tem conta GitHub, pule para o Passo 2.

---

## Passo 2 — Criar o repositório com todos os arquivos

1. Clique no **`+`** (canto superior direito) → **New repository**
2. Preencha:
   - **Repository name:** `copa2026` (ou qualquer nome)
   - Marque **Public** (necessário para GitHub Pages gratuito)
   - Não marque "Add README" nem nada
3. Clique em **Create repository**
4. Na próxima tela, clique em **uploading an existing file**
5. **Arraste e solte** todos os arquivos que você baixou desta conversa:
   ```
   copa_2026_icalendar.ics
   copa_2026_outlook.ics
   generate_calendar.py
   build_data.py
   sync.py
   data/data.json          ← esta fica numa pasta "data"
   .github/workflows/sync.yml  ← esta fica em ".github/workflows"
   ```

   > Para os arquivos dentro de pastas: no campo "Commit changes" haverá
   > um campo de caminho — escreva o caminho completo como `data/data.json`
   > e `.github/workflows/sync.yml`.

   **Dica mais simples:** use o botão **"Add file → Upload files"** e
   faça o upload em duas rodadas — primeiro os arquivos da raiz, depois
   crie a estrutura de pastas pelo campo de nome do arquivo.

6. Clique em **Commit changes** (botão verde).

---

## Passo 3 — Ativar o GitHub Pages (1 clique)

1. No seu repositório, clique em **Settings** (engrenagem)
2. No menu lateral esquerdo, clique em **Pages**
3. Em **Source**, selecione **Deploy from a branch**
4. Em **Branch**, escolha **main** e pasta **/ (root)**
5. Clique em **Save**

GitHub vai te mostrar o endereço do seu site — algo como:
```
https://SEU_USUARIO.github.io/copa2026/
```

> Pode levar 2-3 minutos na primeira vez.

---

## Passo 4 — Copiar o link do calendário

O link do seu `.ics` será:
```
https://SEU_USUARIO.github.io/copa2026/copa_2026_icalendar.ics
```

Para usar no **iPhone**, troque `https://` por `webcal://`:
```
webcal://SEU_USUARIO.github.io/copa2026/copa_2026_icalendar.ics
```

*(Substitua `SEU_USUARIO` pelo seu nome de usuário do GitHub e `copa2026`
pelo nome que você deu ao repositório.)*

---

## Passo 5 — Assinar o calendário no iPhone (1 vez)

### Opção A — Link direto (mais fácil)
1. No iPhone, abra o **Safari**
2. Cole o link `webcal://SEU_USUARIO.github.io/copa2026/copa_2026_icalendar.ics`
3. O iPhone vai perguntar **"Deseja assinar o calendário?"** → toque em **Assinar**
4. Configure **"Atualizar automaticamente"** → Pronto ✅

### Opção B — Pelo aplicativo Ajustes
1. **Ajustes** → **Calendário** → **Contas**
2. **Adicionar conta** → **Outro**
3. **Adicionar calendário assinado**
4. Cole o link `webcal://SEU_USUARIO.github.io/copa2026/copa_2026_icalendar.ics`
5. Toque em **Próximo** → **Salvar** ✅

---

## O que acontece depois

| Evento | Automático? |
|---|---|
| Copa começa, jogos da fase de grupos aparecem | ✅ Já estão no calendário |
| Um jogo termina — placar registrado | ✅ Sync a cada 30 min |
| Grupos fecham — mata-mata mostra seleções certas | ✅ Auto-resolve |
| Oitavas, quartas, semis e final se resolvem | ✅ Tudo automático |
| iPhone atualiza sem você fazer nada | ✅ A cada 1-2h (iOS padrão) |

---

## Forçar atualização imediata no iPhone

Se quiser o calendário mais fresco agora mesmo:
**Ajustes → Calendário → Contas → seu calendário da Copa → Buscar novos eventos**

---

## Verificar se o GitHub Actions está rodando

1. No repositório, clique em **Actions** (aba no topo)
2. Você verá as últimas execuções do workflow "⚽ Atualizar Calendário Copa 2026"
3. Ícone verde ✅ = funcionou | Ícone vermelho ❌ = erro (raro)

---

## Sobre as escalações dos 26 convocados

O motor já está estruturado para exibir os 26 convocados de cada seleção
(posição GOL/DEF/MEI/ATA + número de camisa) nas notas de cada jogo.
Peça ao Claude para preencher as escalações por lote (ex.: "preencha
o Grupo C completo") e o arquivo `data.json` atualizado substitui o atual
no repositório — o calendário passa a exibir as escalações em todos os
eventos dessa seleção automaticamente.

---

## Arquivo para Outlook

O arquivo `copa_2026_outlook.ics` contém as mesmas informações com as
propriedades extras `X-MICROSOFT-CDO-BUSYSTATUS:FREE` para garantir
"mostrar como livre" no Outlook. Para assiná-lo, use:
```
webcal://SEU_USUARIO.github.io/copa2026/copa_2026_outlook.ics
```
