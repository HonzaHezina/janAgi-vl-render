import json
from typing import Any, Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field
import vl_convert as vlc

app = FastAPI(title="Vega-Lite Renderer", version="1.0.0")


class RenderRequest(BaseModel):
    spec: dict[str, Any] = Field(..., description="Vega-Lite spec JSON")
    format: Literal["png", "svg", "vega"] = "png"
    scale: float = Field(2.0, ge=0.1, le=8.0)
    vl_version: str | None = None


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/render")
def render_chart(req: RenderRequest):
    try:
        spec_str = json.dumps(req.spec, ensure_ascii=False)
        kwargs: dict[str, Any] = {}
        if req.vl_version:
            kwargs["vl_version"] = req.vl_version

        if req.format == "png":
            png_bytes = vlc.vegalite_to_png(vl_spec=spec_str, scale=req.scale, **kwargs)
            return Response(content=png_bytes, media_type="image/png")

        if req.format == "svg":
            svg = vlc.vegalite_to_svg(vl_spec=spec_str, **kwargs)
            return Response(content=svg.encode("utf-8"), media_type="image/svg+xml")

        # req.format == "vega"
        vega = vlc.vegalite_to_vega(vl_spec=spec_str, **kwargs)
        if isinstance(vega, str):
            return JSONResponse(content=json.loads(vega))
        return JSONResponse(content=vega)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Render failed: {e}")
