# Pregătire pentru interviu — n8n Invoice Review

Roluri țintă: n8n / Finance Operations Automation.

## Prezentare de 90 de secunde

1. Explică problema concretă și cine folosește rezultatul.
2. Rulează `make demo` sau fluxul din UI.
3. Arată testul pentru un caz de eșec, apoi explică mecanismul din cod.
4. Spune ce limite are demonstrația și ce ai construi pentru producție.

Decizia de explicat: n8n submits an invoice into a durable review queue. Vendor plus invoice number detect duplicates. Integer cents validate totals. A separate explicit operator approval archives the invoice transactionally.

## Cinci întrebări

1. De ce nu aprobi automat după extracție?
2. Cum alegi cheia de deduplicare?
3. De ce integer cents?
4. Cum corectezi o factură fără să pierzi istoricul?
5. Ce autoritate are workflow-ul?

## Exercițiu înainte de a aplica

Add a dedicated review form and a versioned correction endpoint, then a real document store adapter.

Alege o parte mică a acestei modificări, implementeaz-o personal, adaugă un test care verifică comportamentul și descrie rezultatul într-un commit real. Nu declara că ai înțeles sau construit singur o parte pe care nu o poți explica.

## Checklist personal

- [ ] Pot porni proiectul dintr-un checkout curat.
- [ ] Pot urmări cererea până la rezultatul salvat.
- [ ] Pot explica diferența dintre fixture și model local.
- [ ] Pot demonstra un eșec și recuperarea lui.
- [ ] Am făcut o modificare proprie și o pot explica în engleză.

Aceste puncte necesită review-ul tău; nu au fost bifate automat.
