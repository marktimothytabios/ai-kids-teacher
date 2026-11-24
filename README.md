# Little Whys

A series of screen-free, read-together picture books that parents use to teach children aged 2-4:
knowledge, values (kindness, empathy, honesty), cleanliness and practical maths.
**10 books x 20 stories = 200 stories**, built with Python, with a free local website to browse and download them.

See [docs/PLAN.md](docs/PLAN.md) for the plan, series catalogue, production pipeline, shop design and roadmap.
The earlier voice-app plan is archived in [docs/archive/APP_PLAN.md](docs/archive/APP_PLAN.md).

> **Before selling:** the text has only had an automatic check. Get a human fact check, safety review and an
> educator read-through first (PLAN section 8).

## Put it online

See [docs/DEPLOY.md](docs/DEPLOY.md): a free Render deploy straight from GitHub, nothing to install.

## Run the website on your computer

```bash
pip install -r requirements-dev.txt
python -m webapp
```

Open <http://127.0.0.1:8000>. The first start builds all the PDFs and
covers in the background (about 20 seconds); pages work while that happens. Options:
`--port 9000`, `--reload` (restart on code changes), `--no-warm` (do not pre-build).

Downloads are free for now. To add Stripe later, see PLAN section 7.7.

## Build books from the command line

```bash
python -m builder validate                       # check all content
python -m builder build 6 --spelling us          # one book, US spelling
python -m builder build all --spelling both      # every book, US and UK
python -m builder build 6 --sample               # free sample (first 3 stories)
python -m pytest                                 # tests
```

PDFs are written to `out/` (not in git).

## Where things are

```
content/books/NN-slug/book.yaml        one folder per book
content/books/NN-slug/stories/NN.yaml  one file per story (20 per book)
builder/                               validator, spelling, drawing kit, stage scenes, PDF layout
webapp/                                FastAPI site (templates, static files)
tests/                                 builder and website tests
docs/                                  plan and archived app plan
```

Write words that differ between US and British English as `{color|colour}`. Pictures are described with a
`scene:` line, either a ready scene such as `day`, or a stage such as `kitchen|kid,apple*3,row,cup`.
