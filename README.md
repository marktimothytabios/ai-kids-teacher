# Little Whys (working title)

A series of screen-free, read-together picture books that parents use to teach children aged 2–4:
knowledge, values (kindness, empathy, honesty), cleanliness and practical maths. 20 stories per book,
built with Python, sold as PDFs through a Stripe-powered site.

See [docs/PLAN.md](docs/PLAN.md) for the plan, series catalogue, production pipeline, shop design and roadmap.

The earlier voice-app plan is archived in [docs/archive/APP_PLAN.md](docs/archive/APP_PLAN.md).

## Build the books

```bash
pip install reportlab pyyaml pypdf pytest
python -m builder validate                       # check all content
python -m builder build 1 --spelling us          # one book, US spelling
python -m builder build all --spelling both      # every book, US and UK
python -m builder build 6 --sample               # free sample (first 3 stories)
python -m pytest                                 # tests
```

Stories live in `content/books/NN-slug/stories/NN.yaml`. Write words that differ between US and
British English as `{color|colour}`. PDFs are written to `out/`.
