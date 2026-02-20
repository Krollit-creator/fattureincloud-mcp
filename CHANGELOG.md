# Changelog

## v1.5.0
- NEW: `create_credit_note` — crea nota di credito (importi positivi in input, negativi automaticamente); parametro opzionale `source_invoice_id` per collegare alla fattura originale
- NEW: `create_proforma` — crea documento proforma (stessa struttura di create_invoice, tipo proforma, non inviabile allo SDI)
- CHANGE: `list_invoices` ora accetta parametro `type`: `invoice` (default), `credit_note`, `proforma`

## v1.4.0
- NEW: `list_invoices` accetta parametro `type`: `invoice` (default), `credit_note`, `proforma`

## v1.3.0
- FIX: `create_invoice` ora include `ei_code` dall'anagrafica cliente
- FIX: `duplicate_invoice` aggiorna `ei_code` dall'anagrafica
- NEW: `check_numeration` per verificare continuità numerica fatture

## v1.2.0
- NEW: `delete_invoice` per eliminare bozze
- NEW: `payment_days` in `duplicate_invoice`

## v1.1.0
- Release iniziale su PyPI e MCP Registry
