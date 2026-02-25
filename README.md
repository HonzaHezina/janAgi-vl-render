# vl-render-fastapi (FastAPI + vl-convert-python)

Minimalní renderer: **Vega-Lite spec (JSON) → PNG/SVG/Vega**.

## Lokálně (Docker Compose)
```bash
docker compose up --build
```

## Test
Health:
```bash
curl http://localhost:8000/health
```

Render PNG:
```bash
curl -X POST "http://localhost:8000/render" \
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

## Poznámka
- Doporučeně používej `data.values` (ne `data.url`) pro bezpečnost a determinističnost.
