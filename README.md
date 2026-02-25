# janAgi-vl-render (Coolify + SSH tunel) — FastAPI + vl-convert-python

Renderer: **Vega-Lite spec (JSON) → PNG/SVG/Vega**.

## Endpoints
- `GET /health` → `{"ok": true}`
- `POST /render` → vrátí `image/png`, `image/svg+xml` nebo JSON (Vega)

## Docker Compose (Coolify)
- Soubor je **`docker-compose.yaml`** (Coolify ho často bere jako default).
- Pro kompatibilitu je v repu i `docker-compose.yml` se stejným obsahem.
- Port je publikovaný **jen na localhost VPS**:
  - `127.0.0.1:3000 -> container:8000`
  - není veřejně vystavený do internetu

### Ověření na VPS
```bash
curl http://127.0.0.1:3000/health
```

### SSH tunel z PC
Jednorázově:
```bash
ssh -N -L 3000:127.0.0.1:3000 root@TVE_VPS_IP
```

Potom na PC:
- `http://127.0.0.1:3000/health`

## Render – doporučené volání (pošli přímo Vega-Lite spec)
```bash
curl -X POST "http://127.0.0.1:3000/render?format=png&scale=2" \
  -H "Content-Type: application/json" \
  -d '{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "data": { "values": [ {"x":"A","y":10}, {"x":"B","y":20} ] },
    "mark": "bar",
    "encoding": {
      "x": {"field":"x","type":"nominal"},
      "y": {"field":"y","type":"quantitative"}
    }
  }' --output chart.png
```

## Wrapper (zpětná kompatibilita)
```bash
curl -X POST "http://127.0.0.1:3000/render" \
  -H "Content-Type: application/json" \
  -d '{
    "format": "png",
    "scale": 2,
    "spec": {
      "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
      "data": { "values": [ {"day":"Mon","count":12},{"day":"Tue","count":18},{"day":"Wed","count":9} ] },
      "mark": {"type":"line","point":true},
      "encoding": {
        "x": {"field":"day","type":"ordinal"},
        "y": {"field":"count","type":"quantitative"}
      }
    }
  }' --output chart.png
```

## Poznámky k produkci
- Doporučuju posílat data jako `data.values` (ne `data.url`) – bezpečnější a deterministické.
- Pokud budeš renderovat hodně bodů, SVG bývá rychlejší než PNG.
