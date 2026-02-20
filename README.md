# Fatture in Cloud MCP Server

[🇮🇹 Italiano](#italiano) | [🇬🇧 English](#english)

<!-- mcp-name: io.github.aringad/fattureincloud-mcp -->

---

## Italiano

Server MCP (Model Context Protocol) per integrare **Fatture in Cloud** con Claude AI e altri assistenti compatibili.

Permette di gestire fatture elettroniche italiane tramite conversazione naturale.

### ✨ Funzionalità (20 tool)

| Tool | Descrizione |
|------|-------------|
| `list_invoices` | Lista fatture/NDC/proforma emesse per anno/mese |
| `get_invoice` | Dettaglio completo documento |
| `get_pdf_url` | URL PDF e link web documento |
| `list_clients` | Lista clienti con filtro |
| `get_company_info` | Info azienda collegata |
| `create_client` | 🆕 Crea nuovo cliente in anagrafica |
| `update_client` | 🆕 Aggiorna dati cliente esistente |
| `create_invoice` | Crea nuova fattura (bozza) con codice SDI automatico |
| `create_credit_note` | Crea nota di credito (bozza) |
| `create_proforma` | Crea proforma (bozza, non inviabile SDI) |
| `convert_proforma_to_invoice` | 🆕 Converte proforma in fattura elettronica |
| `update_document` | Modifica parziale documento bozza |
| `duplicate_invoice` | Duplica fattura con codice SDI aggiornato |
| `delete_invoice` | Elimina documento bozza (non inviato) |
| `send_to_sdi` | Invia fattura allo SDI |
| `get_invoice_status` | Stato fattura elettronica SDI |
| `send_email` | Invia copia cortesia via email |
| `list_received_documents` | Fatture passive (fornitori) |
| `get_situation` | Dashboard: fatturato netto, incassato, costi, margine |
| `check_numeration` | Verifica continuità numerica fatture |

> **Nota:** La marcatura dei pagamenti come "pagato" non è supportata. Usa il pannello web di Fatture in Cloud per questa operazione.

### 🚀 Installazione

#### Prerequisiti
- Python 3.10+
- Account [Fatture in Cloud](https://www.fattureincloud.it/) con API attive
- [Claude Desktop](https://claude.ai/download) o altro client MCP

#### 1. Clona il repository

```bash
git clone https://github.com/aringad/fattureincloud-mcp.git
cd fattureincloud-mcp
```

#### 2. Crea ambiente virtuale e installa dipendenze

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure: venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

#### 3. Configura le credenziali

Copia il file di esempio e inserisci i tuoi dati:

```bash
cp .env.example .env
```

Modifica `.env`:
```env
FIC_ACCESS_TOKEN=a/xxxxx.yyyyy.zzzzz
FIC_COMPANY_ID=123456
FIC_SENDER_EMAIL=fatturazione@tuaazienda.it
```

**Come ottenere le credenziali:**
1. Accedi a [Fatture in Cloud](https://secure.fattureincloud.it/)
2. Vai su *Impostazioni > API e Integrazioni*
3. Crea un **Token Manuale** con i permessi necessari
4. Il `COMPANY_ID` è visibile nell'URL quando sei loggato

#### 4. Configura Claude Desktop

Modifica `~/Library/Application Support/Claude/claude_desktop_config.json` (Mac) o `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "fattureincloud": {
      "command": "/percorso/completo/fattureincloud-mcp/venv/bin/python",
      "args": ["/percorso/completo/fattureincloud-mcp/server.py"],
      "env": {
        "FIC_ACCESS_TOKEN": "a/xxxxx.yyyyy.zzzzz",
        "FIC_COMPANY_ID": "123456",
        "FIC_SENDER_EMAIL": "fatturazione@tuaazienda.it"
      }
    }
  }
}
```

#### 5. Riavvia Claude Desktop

Chiudi completamente Claude Desktop (Cmd+Q su Mac) e riaprilo.

### 💬 Esempi d'uso

```
"Mostrami le fatture di dicembre 2024"
"Qual è la situazione finanziaria del 2025?"
"Duplica la fattura 310 cambiando 2025 in 2026"
"Invia la fattura 326 allo SDI"
"Manda la copia cortesia via email"
"Quali fatture devo ancora incassare?"
"Verifica la numerazione delle fatture 2025"
"Converti la proforma 12 in fattura"
"Crea un nuovo cliente: Rossi SRL, P.IVA 01234567890"
```

### ⚠️ Note di sicurezza

- Le operazioni di scrittura (create, send_to_sdi) richiedono **sempre conferma**
- L'invio allo SDI è **irreversibile**
- Le fatture vengono create come **bozze** (draft)
- Il codice univoco SDI viene recuperato **automaticamente** dall'anagrafica cliente
- Il metodo di pagamento di default è **MP05** (bonifico)

### 📋 Changelog

Vedi [CHANGELOG.md](CHANGELOG.md)

### 📄 Licenza

MIT - Vedi [LICENSE](LICENSE)

### 👨‍💻 Autore

Sviluppato da **[Mediaform s.c.r.l.](https://media-form.it)** - Genova, Italia

---

## English

MCP (Model Context Protocol) Server to integrate **Fatture in Cloud** with Claude AI and other compatible assistants.

Manage Italian electronic invoices through natural conversation.

### ✨ Features (20 tools)

| Tool | Description |
|------|-------------|
| `list_invoices` | List invoices/credit notes/proforma by year/month |
| `get_invoice` | Full document details |
| `get_pdf_url` | PDF URL and web link for document |
| `list_clients` | List clients with filter |
| `get_company_info` | Connected company info |
| `create_client` | 🆕 Create new client in registry |
| `update_client` | 🆕 Update existing client data |
| `create_invoice` | Create new invoice (draft) with automatic SDI code |
| `create_credit_note` | Create credit note (draft) |
| `create_proforma` | Create proforma (draft, not sendable to SDI) |
| `convert_proforma_to_invoice` | 🆕 Convert proforma to electronic invoice |
| `update_document` | Partial update of draft document |
| `duplicate_invoice` | Duplicate invoice with updated SDI code |
| `delete_invoice` | Delete draft document (not yet sent) |
| `send_to_sdi` | Send invoice to SDI (Italian e-invoice system) |
| `get_invoice_status` | E-invoice SDI status |
| `send_email` | Send courtesy copy via email |
| `list_received_documents` | Received invoices (suppliers) |
| `get_situation` | Dashboard: net revenue, collected, costs, margin |
| `check_numeration` | Verify invoice numbering continuity |

> **Note:** Marking payments as "paid" is not supported. Use the Fatture in Cloud web panel for this operation.

### 🚀 Installation

#### Prerequisites
- Python 3.10+
- [Fatture in Cloud](https://www.fattureincloud.it/) account with API enabled
- [Claude Desktop](https://claude.ai/download) or other MCP client

#### 1. Clone the repository

```bash
git clone https://github.com/aringad/fattureincloud-mcp.git
cd fattureincloud-mcp
```

#### 2. Create virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

#### 3. Configure credentials

Copy the example file and fill in your data:

```bash
cp .env.example .env
```

Edit `.env`:
```env
FIC_ACCESS_TOKEN=a/xxxxx.yyyyy.zzzzz
FIC_COMPANY_ID=123456
FIC_SENDER_EMAIL=billing@yourcompany.com
```

**How to get credentials:**
1. Log into [Fatture in Cloud](https://secure.fattureincloud.it/)
2. Go to *Settings > API and Integrations*
3. Create a **Manual Token** with required permissions
4. The `COMPANY_ID` is visible in the URL when logged in

#### 4. Configure Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (Mac) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "fattureincloud": {
      "command": "/full/path/to/fattureincloud-mcp/venv/bin/python",
      "args": ["/full/path/to/fattureincloud-mcp/server.py"],
      "env": {
        "FIC_ACCESS_TOKEN": "a/xxxxx.yyyyy.zzzzz",
        "FIC_COMPANY_ID": "123456",
        "FIC_SENDER_EMAIL": "billing@yourcompany.com"
      }
    }
  }
}
```

#### 5. Restart Claude Desktop

Fully quit Claude Desktop (Cmd+Q on Mac) and reopen it.

### 💬 Usage examples

```
"Show me invoices from December 2024"
"What's the financial situation for 2025?"
"Duplicate invoice 310 changing 2025 to 2026"
"Send invoice 326 to SDI"
"Send the courtesy copy via email"
"Which invoices are still pending payment?"
"Check invoice numbering for 2025"
"Convert proforma 12 to invoice"
"Create a new client: Rossi SRL, VAT 01234567890"
```

### ⚠️ Security notes

- Write operations (create, send_to_sdi) **always require confirmation**
- Sending to SDI is **irreversible**
- Invoices are created as **drafts**
- SDI unique code is **automatically retrieved** from client registry
- Default payment method is **MP05** (bank transfer)

### 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md)

### 📄 License

MIT - See [LICENSE](LICENSE)

### 👨‍💻 Author

Developed by **[Mediaform s.c.r.l.](https://media-form.it)** - Genova, Italy
