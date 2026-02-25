# janAgi-vl-render (jednotný port 31873) — Coolify + SSH tunel

Renderer: **Vega-Lite spec (JSON) → PNG/SVG/Vega**.

✅ Vše běží na portu **31873**:
- **uvnitř kontejneru**: 31873
- **interně mezi kontejnery**: `http://vl-render:31873`
- **na VPS jen lokálně**: `http://127.0.0.1:31873` (pro SSH tunel)

## Endpoints
- `GET /health` → `{"ok": true}`
- `POST /render` → `image/png`, `image/svg+xml` nebo JSON (Vega)

## Ověření na VPS
```bash
curl http://127.0.0.1:31873/health
```

## SSH tunel z PC
Jednorázově:
```bash
ssh -N -L 31873:127.0.0.1:31873 root@TVE_VPS_IP
```

Potom na PC:
- `http://127.0.0.1:31873/health`

## Interní volání (n8n ve stejném stacku/síti)
- `http://vl-render:31873/health`
- `http://vl-render:31873/render`

## Render – doporučené volání (pošli přímo Vega-Lite spec)
```bash
curl -X POST "http://127.0.0.1:31873/render?format=png&scale=2" \
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
curl -X POST "http://127.0.0.1:31873/render" \
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
