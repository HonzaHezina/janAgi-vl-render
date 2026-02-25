import json
from typing import Any, Literal, Optional

from fastapi import Body, FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse, Response
import vl_convert as vlc

app = FastAPI(title="Vega-Lite Renderer", version="1.1.0")


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/render")
def render_chart(
    payload: dict[str, Any] = Body(..., description="Buď přímo Vega-Lite spec, nebo wrapper {spec, format, scale, vl_version}."),
    format: Literal["png", "svg", "vega"] = Query("png", description="Výstupní formát (fallback, pokud nepoužiješ wrapper)."),
    scale: float = Query(2.0, ge=0.1, le=8.0, description="Scale pro PNG (fallback, pokud nepoužiješ wrapper)."),
    vl_version: Optional[str] = Query(None, description="Volitelně vega-lite verze (fallback, pokud nepoužiješ wrapper)."),
):
    """Render Vega-Lite spec -> PNG/SVG/Vega.

    Podporuje 2 režimy:

    1) Přímý spec (doporučené pro tvoje flow):
       POST /render?format=png&scale=2
       BODY: { ... Vega-Lite spec ... }

    2) Wrapper (zpětná kompatibilita):
       POST /render
       BODY: { "spec": {...}, "format":"png", "scale":2, "vl_version": "5.16.3" }
    """
    try:
        # Wrapper režim?
        if isinstance(payload, dict) and "spec" in payload and isinstance(payload["spec"], dict):
            spec = payload["spec"]
            format = payload.get("format", format)
            scale = float(payload.get("scale", scale))
            vl_version = payload.get("vl_version", vl_version)
        else:
            spec = payload

        spec_str = json.dumps(spec, ensure_ascii=False)

        kwargs: dict[str, Any] = {}
        if vl_version:
            kwargs["vl_version"] = vl_version

        if format == "png":
            png_bytes = vlc.vegalite_to_png(vl_spec=spec_str, scale=scale, **kwargs)
            return Response(content=png_bytes, media_type="image/png")

        if format == "svg":
            svg = vlc.vegalite_to_svg(vl_spec=spec_str, **kwargs)
            return Response(content=svg.encode("utf-8"), media_type="image/svg+xml")

        # format == "vega"
        vega = vlc.vegalite_to_vega(vl_spec=spec_str, **kwargs)
        if isinstance(vega, str):
            return JSONResponse(content=json.loads(vega))
        return JSONResponse(content=vega)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Render failed: {e}")
