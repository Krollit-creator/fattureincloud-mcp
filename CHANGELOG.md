# Changelog

## v1.7.0
- NEW: `mark_payment_paid` — segna scadenza come pagata con data incasso
- NEW: `mark_payment_unpaid` — rollback pagamento a non pagato
- NEW: `convert_proforma_to_invoice` — converte proforma in fattura (elimina proforma di default, `keep_proforma=True` per mantenerla)
- NEW: `get_pdf_url` — restituisce URL PDF e link web del documento
- NEW: `create_client` — crea nuovo cliente in anagrafica
- NEW: `update_client` — aggiorna dati cliente esistente
- FIX: `get_situation` — ora sottrae le NDC dal fatturato (fatturato_netto = fatture - NDC) e supporta filtro per cliente

## v1.6.4
- FIX: `create_credit_note` — prezzi e payment positivi, FIC inverte internamente per type=credit_note
- FIX: `update_document` — stessa logica per NDC

## v1.6.3
- FIX: tentativo NDC senza payments_list (non funzionava)

## v1.6.2
- FIX: tentativo NDC con payment negativo (non funzionava)

## v1.6.1
- FIX: tentativo abs() su payment per NDC (non funzionava)

## v1.6.0
- NEW: `update_document` — modifica parziale di qualsiasi documento bozza (fattura, NDC, proforma): data, oggetto, righe, giorni pagamento. Carica l'originale e applica solo i campi passati.

## v1.5.0
- NEW: `create_credit_note` — crea nota di credito; importi positivi in input, negativi automaticamente; `source_invoice_id` opzionale
- NEW: `create_proforma` — crea proforma, non inviabile allo SDI
- CHANGE: `list_invoices` accetta parametro `type`: `invoice` (default), `credit_note`, `proforma`

## v1.4.0
- NEW: `list_invoices` accetta parametro `type`

## v1.3.0
- FIX: `create_invoice` include `ei_code` dall'anagrafica
- FIX: `duplicate_invoice` aggiorna `ei_code`
- NEW: `check_numeration`

## v1.2.0
- NEW: `delete_invoice`
- NEW: `payment_days` in `duplicate_invoice`

## v1.1.0
- Release iniziale
