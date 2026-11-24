"""Run the site locally: python -m webapp [--port 8000] [--reload]"""
import argparse

import uvicorn


def main() -> None:
    ap = argparse.ArgumentParser(prog="webapp", description="Run the Little Whys site on localhost")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--reload", action="store_true", help="restart when code changes (development)")
    ap.add_argument("--no-warm", action="store_true", help="do not pre-build the PDFs at start-up")
    a = ap.parse_args()
    print(f"\n  Little Whys is starting at http://{a.host}:{a.port}\n")
    if a.reload:
        import os
        os.environ["LITTLE_WHYS_WARM"] = "0" if a.no_warm else "1"
        uvicorn.run("webapp.main:app", host=a.host, port=a.port, reload=True)
    else:
        from .app import create_app
        uvicorn.run(create_app(warm=not a.no_warm), host=a.host, port=a.port)


if __name__ == "__main__":
    main()
