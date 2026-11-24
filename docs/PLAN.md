# Little Whys: A Series of Read-Together Books for Toddlers

Plan and write-up. Status: **all 10 launch books written and building; free local website running.** See section 12 for the decisions and section 13 for what is built.

*(The earlier voice-app plan is kept in [archive/APP_PLAN.md](archive/APP_PLAN.md). We are no longer building
an app: it is screen-based, and the product is now a book that a parent reads *with* a child.)*

---

## 1. The idea in one paragraph

A series of short picture books for **parents to read with children aged 2–4**. Each book has
**20 stories**. Every story is one small question a toddler might ask ("Why do we wash our hands?"),
a short, simple answer, and a hands-on "Let's try!" activity. The series covers **knowledge** (sky,
animals, the body), **values** (kindness, empathy, honesty, gratitude), **practical skills** (counting,
sorting, tidying up, keeping clean) and anything else that helps a child grow up good and curious.
Books are screen-free: the child never touches a device. Parents buy a book as a PDF to print or read,
and later we may add real printed copies. A website sells each book through Stripe.

**Why this works as a product:** parents of toddlers already want screen-free, co-reading content;
the format is proven by the first book (which you liked); and 20 stories per book makes each book small
enough to finish in a few weeks and cheap enough to sell at a low price.

---

## 2. What the first book taught us

I read the PDF you made (103 pages, ReportLab, 800×800 square pages). Its structure is the template
for the whole series:

| Part | What it is | Keep? |
|---|---|---|
| Cover | Title, subtitle, "a read-together book for ages 2–4" | Keep, add series branding and volume number |
| "For the grown-up" page | 6 tips: read 1–2 at a time, ask first, point and name, do the activity, simplified on purpose, "let's find out together" | Keep. This is what makes it a *parent* book. Make it specific to each book |
| Question page (full page) | Big picture, numbered badge, the question | Keep |
| Answer page | Small picture, 2–4 sentences, **"Let's try!"** activity box | Keep, add one more element (below) |
| End page | "Keep asking WHY!" | Keep, add a recap and a "what's next" page |

**What works:** one idea per spread, very short text, a physical activity on every answer, and the "ask
them first" advice. **What to improve:**

1. **Add a "Talk about it" prompt** next to "Let's try!". For example, "When did you last share?". Asking
   open questions while reading is one of the most effective things a parent can do, and it is the
   difference between a book that is read *to* a child and one read *with* them.
2. **Add a "grown-up corner"** (one line, small print): a fuller fact for the parent, or the value behind
   the story. This lets parents answer the follow-up "but why?".
3. **Repeating characters.** The first book has anonymous kids. A small cast (say 4 children and a pet)
   that returns in every book builds attachment and brand.
4. **Better art for a paid product.** The first book's flat vector art is clean and consistent, but it is
   basic (see section 6, the biggest risk for selling).
5. **Fact-check pass.** Some answers are simplified. That is fine for age 2–4, but nothing should be
   *wrong*. Every story gets a short review before release (section 8).
6. **Spelling:** the first book is British ("colours", "Practise"). The series now supports **both US and
   British spelling**, chosen when the PDF is generated (section 5.1).

---

## 3. The series

### 3.1 Book format

- **20 stories per book.** 20 stories × 2 pages = 40 pages, plus front and back matter = **48 pages**
  (a multiple of 4, so it can also be printed and bound later).
- Page layout per book:

| Pages | Content |
|---|---|
| 1 | Cover |
| 2 | Title page and "For the grown-up" (book-specific) |
| 3 | Contents: the 20 questions as a picture checklist (tick off as you read) |
| 4–43 | 20 stories (question page + answer page) |
| 44 | "What we learned": all 20 answers as tiny pictures, for recap |
| 45 | Activity page: colouring or a simple printable (sticker chart, shapes to cut out) |
| 46 | "Next in the series" |
| 47 | Credits, copyright, usage licence |
| 48 | Back cover |

- **Reading time:** one story is about 2–3 minutes. A book lasts 3–4 weeks at a story a day, which is a
  good "one book per month" rhythm for a subscription-like habit.

### 3.2 Launch catalogue: 10 books, 200 stories

Your 50 existing stories are all reused, and **150 new stories** need writing. Every book has a theme
and a "value or skill" it teaches.

| # | Book | Teaches | Reused from book 1 | New |
|---|---|---|---|---|
| 1 | **Sky, Weather & Seasons** | Curiosity about nature | Sky blue, sun at night, moon, stars, rain, thunder, rainbows, wind, ice, snow, leaves, shadow (12) | 8 |
| 2 | **Plants & Animals** | Care for living things | Flowers, bees, plants need water, birds, fish, dogs, cats, kangaroos, ducks (9) | 11 |
| 3 | **How Things Work** | Cause and effect | Sea is salty, waves, balls bounce, things fall, boats float, wheels (6) | 14 |
| 4 | **My Amazing Body** | Knowing and loving your body | Tummy rumbles, belly button, two eyes, ears, sneeze, hiccups, yawn, grow, heartbeat (9) | 11 |
| 5 | **Clean, Healthy & Strong** | Cleanliness and habits | Teeth, baths, hand-washing, sleep, vegetables, water, shoes, sun hat (8) | 12 |
| 6 | **Kind Hearts** | Kindness, empathy, sharing | Please and thank you, sharing, family love (3) | 17 |
| 7 | **Feelings & Friends** | Naming feelings, friendship | Why do I cry (1) | 19 |
| 8 | **Little Mathematicians** | Practical maths | none | 20 |
| 9 | **Safe & Smart** | Safety, honesty, listening | Holding hands near the road (1) | 19 |
| 10 | **Helpers & Our World** | Community, jobs, caring for Earth | Why grown-ups work (1) | 19 |
| | **Total** | | **50** | **150** |

### 3.3 Ideas for the new stories (starting list, not final)

- **Kind Hearts (empathy):** Why do we say sorry? Why is it nice to help? Why do we hug someone who is
  sad? Why do we wait for our turn? Why do we use gentle hands? Why do we say hello? Why do we help
  tidy up? Why do we listen when someone talks?
- **Feelings & Friends:** Why do I get angry? Why do I feel scared of the dark? Why do I get shy? Why
  is it OK to feel sad? Why do friends matter? Why do we take deep breaths?
- **Little Mathematicians (practical maths):** Why do we count? Why do we have two shoes? Why is it
  "more" or "less"? Why do we set the table with one plate each? Why do we sort laundry? Why do shapes
  matter? What is half? Why do we need a clock? What are coins for?
- **Safe & Smart:** Why do we tell the truth? Why do we not touch hot things? Why do we stay close in
  the shop? Why do we wear a seatbelt? Why do we ask before taking something?
- **Clean, Healthy & Strong (new part):** Why do we cover our cough? Why do we wipe our nose? Why do we
  put rubbish in the bin? Why do we wash fruit? Why do we need exercise?
- **Helpers & Our World:** Why do we recycle? Why do we switch off the light? Why do we not waste food?
  Who grows our food? What does a doctor do?

**Later volumes:** Feelings 2, Numbers 2, Letters & Sounds, Food (farm to table), Seasons around the
world, Money basics, Manners at the table, Bedtime stories, My Family and My Culture. Parents will
also ask for **age 4–6 editions** ("Why Why Why: Big Kids") with more detail.

### 3.4 A learning framework for every story

Each story carries four tags in its data. They keep the series balanced and let us sell by theme.

| Tag | Examples |
|---|---|
| **Domain** | Science, My body, Maths, Social-emotional, Health, Safety, Community |
| **Value** (if any) | Kindness, empathy, honesty, gratitude, patience, responsibility, courage |
| **Skill** | Counting, sorting, naming feelings, turn-taking, hygiene routine |
| **Activity type** | Move, touch, pretend, sing, count, make, look around |

Each book must cover at least two domains, and the whole series should include roughly 40% knowledge,
40% values/emotional skills and 20% practical skills, so that it is not only "science facts".

---

## 4. How a story is written (the content rules)

- **Question:** starts with "Why" or "How", under 8 words, in a child's voice.
- **Answer:** 2–4 short sentences, 8–12 words each, concrete words a 2–4-year-old knows, one idea,
  something they can see or feel. For values stories, use a tiny scene rather than a lecture ("Mia
  shares her ball. Now Ben is smiling too").
- **Let's try!:** one physical action that needs no equipment or only household items, and takes a minute.
- **Talk about it:** one open question that has no wrong answer.
- **Grown-up corner:** one or two sentences of real explanation or the value behind the story.
- **Tone:** warm, never scary, never shaming, nothing about punishment. Values are shown as "this makes
  hearts happy", not "good children do this".
- **Inclusive:** varied skin tones, family types and abilities in the cast. Avoid gender stereotypes in
  jobs and roles.
- **Readability check:** automated (sentence length, word list) plus a human read-aloud test.

### Story file format (YAML, one file per story)

```yaml
id: kind-hearts-03
book: kind-hearts
order: 3
question: "Why do we say sorry?"
answer: >
  Sometimes we bump into a friend or grab a toy. That can make them sad.
  Saying sorry shows we care, and it helps our friend feel better.
lets_try: "Pretend to bump a teddy. Then say, 'Sorry, teddy!' and give it a gentle pat."
talk_about: "How do you feel when someone says sorry to you?"
grown_up_corner: >
  Toddlers say sorry best when they see the other child's face. Point out the feeling first,
  then practise the words.
tags: {domain: social-emotional, value: empathy, skill: apologising, activity: pretend}
scene: {template: two_kids_with_toy, mood: gentle, palette: warm_pink}
reviewed: {facts: false, values: false, readability: false}
```

---

## 5. Python production pipeline

Everything is generated by Python from the content files. **Write content once, build every format.**

```
content (YAML)  →  validate  →  illustrate (SVG)  →  lay out pages  →  PDF  →  QA checks  →  publish
```

| Step | What it does | Tool |
|---|---|---|
| Validate | Schema check, word counts, readability, banned words, all 20 stories present | `pydantic`, `textstat` |
| Illustrate | Build each scene from reusable parts: characters, backgrounds, objects, palettes | `svgwrite` or hand-built SVG, rendered with `cairosvg` |
| Lay out | Page templates: cover, question page, answer page, recap, activity page | `reportlab` (already used for book 1, installed here) |
| Fonts | Embedded child-friendly font with open licence (e.g. Nunito or Andika, plus DejaVu as fallback) | TTF files in repo |
| Output | **Screen PDF** (RGB, small file), **Print PDF** (A5/US 8×8, CMYK-safe, 3 mm bleed), **Sample PDF** (first 3 stories), **Thumbnails/preview images** for the shop | `reportlab`, `pypdf`, `pillow` |
| QA | Fonts embedded, no text overflow, no empty pages, page count = 48, file size limit, contrast check | custom checks + `pypdf` |

**Why ReportLab and not HTML-to-PDF (WeasyPrint)?** ReportLab is already working for you and is
installed here. WeasyPrint gives easier layout with CSS but needs system libraries. We can switch later if
page design gets complicated; the content files do not change.

### 5.1 US and British spelling from one source

Content is written once. Where the two spellings differ, the text marks the choice inline as
`{us|uk}`, for example `all the {colors|colours} of the rainbow` or `Let's {practice|practise}`.
The builder resolves each marker for the chosen variant, so **one command builds both** PDFs:
`--spelling us` or `--spelling uk`. A checker flags common unmarked words (color, mom, gray…) so nothing
slips through. This is explicit on purpose: an automatic word-swapper cannot tell the noun "practice"
from the verb "practise".

### Proposed repository layout

```
ai-kids-teacher/
├── content/
│   ├── series.yaml                 # series name, cast, palettes, book list
│   └── books/
│       ├── 01-sky-weather/
│       │   ├── book.yaml           # title, grown-up note, cover scene
│       │   └── stories/01.yaml … 20.yaml
│       └── 02-plants-animals/ …
├── kit/                            # illustration kit
│   ├── characters/                 # cast with moods and poses
│   ├── scenes/                     # reusable backgrounds
│   ├── objects/                    # sun, ball, toothbrush, etc.
│   └── palettes.py
├── builder/                        # the Python package
│   ├── schema.py   validate.py   illustrate.py
│   ├── layout.py   build_pdf.py  qa.py   cli.py
├── site/                           # the shop (section 7)
├── tests/
├── out/                            # generated PDFs (git-ignored)
└── docs/
```

CLI sketch: `python -m builder build 01-sky-weather --target screen|print|sample`, and
`python -m builder qa --all`.

---

## 6. Illustrations: the biggest decision

The first book's art is generated by code from flat shapes. It is consistent and free, but it is simple
and a paying customer will compare it with professionally illustrated toddler books.

| Option | Cost | Quality | Consistency | Notes |
|---|---|---|---|---|
| **A. Code-drawn vector kit** (as in book 1, but richer) | Free | OK | Perfect | Good enough to *launch and test demand*. Slow to make new scenes look rich |
| **B. AI-generated images** | Low per image | High but uneven | Hard (characters drift between pages) | 200 stories need the same characters. Legal point: in the US, purely AI-made images are not copyrightable, so competitors could copy them. Also check each tool's commercial-use terms |
| **C. Commissioned illustrator, then compose in Python** | One-off fee for a character and asset kit (often a few hundred to a few thousand dollars) | Best | Perfect, because the kit is fixed | Illustrator draws the cast (poses, emotions) and about 100 objects and backgrounds as SVG. Python assembles them into every page. You **own** the art |
| **D. Hybrid** | | | | Start with A for books 1–3 at low price. Commission C once sales prove the idea, and re-release |

**Recommendation: D.** Launch with an upgraded version of A (still cheap, still consistent), run a small
paid test, and commission C with the revenue. The pipeline treats the kit as a swappable folder, so the
change is not a rewrite.

---

## 7. The shop (long term)

### 7.1 Do it in two steps

1. **Validate first:** a **Stripe Payment Link** for each book needs no code: Stripe hosts the checkout and
   you deliver the PDF by link or email. You learn whether people buy.
2. **Own site:** build the custom Python site below once you see demand.

### 7.2 Recommended stack

| Part | Choice | Why |
|---|---|---|
| Web framework | **FastAPI** + Jinja templates (HTMX for small interactions) | Python, fast, little JavaScript, clear structure |
| Database | SQLite first, move to PostgreSQL when needed | Simple at the start |
| Payments | **Stripe Checkout** (hosted page, created by our server) + **Stripe Tax** for sales tax/VAT/GST | Handles cards, wallets, many currencies and countries, so we can sell to anyone. PayPal can be added later as an extra option through Stripe, if wanted |
| File storage | Private object storage (S3 or Cloudflare R2), or local disk at the start | PDFs must never be public URLs |
| Delivery | **Signed, expiring download links** (e.g. 7 days, 5 downloads) sent by email | Prevents link sharing |
| Email | Resend, Postmark or SES | Receipts and download links |
| Hosting | Fly.io, Render or a small VPS | Cheap, Python-friendly |

### 7.3 Purchase flow

```
Visitor → book page (preview images, sample PDF, price)
   → buyer picks spelling (US / UK) → "Buy" → our server creates a Stripe Checkout Session
   → buyer pays on Stripe's page → Stripe sends webhook `checkout.session.completed`
   → we verify the signature, save the order → email with signed download link
```

Rules that matter:

- **Never trust the browser.** Mark an order paid only after a verified Stripe webhook (check the
  signature with the webhook secret), never because the buyer reached a "thank you" page.
- **Idempotent:** a repeated webhook must not create a second order.
- **Refunds/disputes:** a webhook handler (`charge.refunded`, `charge.dispute.created`) marks the order refunded and disables the link.
- **Per-buyer watermark:** the build step stamps a tiny line ("Licensed to name@email") on the last page
  of the buyer's copy. It deters sharing without hurting honest customers. (Generated on demand and
  cached, ~1 second per book.)
- **Spelling choice:** the buyer chooses **US or British** on the book page (and can download the other
  version later from their library at no cost). Both versions are built from the same content files.
- **Pages:** Home, Series/Catalogue, Book page, Cart or Buy now, "My downloads" (by email link),
  Free sample, About, FAQ, Terms/Privacy/Refunds, Contact.

### 7.4 Data model (first draft)

```
book(id, slug, title, volume, theme, price_cents, status, cover_url, sample_pdf, master_pdf)
bundle(id, slug, title, price_cents)           bundle_item(bundle_id, book_id)
customer(id, email, created_at)
order(id, customer_id, stripe_session_id, stripe_payment_intent, status, total_cents, currency, created_at)
order_item(order_id, book_id|bundle_id, price_cents, spelling)   -- spelling: 'us' | 'uk'
download_token(id, order_item_id, token_hash, expires_at, downloads_left)
event_log(id, source, type, payload, created_at)   -- raw Stripe webhooks for auditing
```

### 7.5 Pricing (to test, not fixed)

- Single book (48 pages PDF): **US$4.99–6.99**
- Bundle of all 10: about **US$29–39** (roughly 40–50% off)
- **Free sample:** first 3 stories of each book, plus one full free "starter" book to collect emails
- Stripe's card fee is roughly 3% plus a small fixed fee per sale (higher for some countries and
  currencies, and Stripe Tax has its own fee); check current rates, since a fixed fee hurts most on low
  prices. Bundles help. Show prices in the buyer's currency with Stripe's currency options.
- Later: printed copies through print-on-demand (Lulu, Amazon KDP or IngramSpark). The print PDF target
  in section 5 prepares for this.

### 7.6 Legal and admin to check early

- Business registration and taxes for digital goods in your country and in your customers' countries
  (some places, like the EU, UK and Australia, require VAT/GST on digital downloads). **Stripe Tax**
  calculates and collects it, but *you* still register and file in each place you must. If you sell to
  "anyone" from day one, a merchant-of-record platform such as Paddle or Lemon Squeezy would do the
  filing for you at a higher fee. This is worth a short decision once you know where buyers are.
- Privacy policy, terms, refund policy. We collect only email and order data. **No child data at all**
  (a big advantage of the book format over the app).
- Trademark and domain check for the series name before printing it on 10 covers.
- Copyright notice and usage licence ("for personal and classroom use, no resale").

---

### 7.7 What exists today (free, localhost) and how Stripe plugs in

The `webapp/` package is a working free site: home page, a page per book, US/UK switch (cookie, or the
browser's language), cover and page previews, an **online reader** for every page, PDF and 3-story sample
downloads built on demand and cached.
Run it with `python -m webapp`.

Stripe is a small addition rather than a rewrite:

1. `webapp/app.py` has one function, `can_download(request, settings, book)`, that decides who may download.
   Today it returns `True`. With payments, it checks a paid order for the visitor.
2. Set `Settings(free=False)` to switch the site into paid mode. A test already checks that full downloads
   then return **402** while the free sample still works.
   In paid mode the reader keeps the first 9 pages (front matter and 3 stories) open as a preview and returns **402**
   for the rest; the text of locked pages is never sent to the browser.
3. Add: a Stripe Checkout Session route, a verified webhook route, the `order` and `download_token` tables
   from 7.4, signed expiring links, and email. Everything else stays as it is.

---

## 8. Quality and trust

For a children's brand, trust is the product. Every book passes these gates before it is sold:

1. **Automated:** schema, readability, word lists, page count, fonts embedded, no overflow.
2. **Fact check:** each answer checked against a reliable source (this can be done with AI help and a
   human read). Simplification is allowed; false statements are not.
3. **Values and safety review:** nothing scary, shaming, stereotyped or unsafe in the "Let's try!" tasks
   (no activity that needs a hot stove, small parts a toddler could swallow, or running near roads).
4. **Educator review:** ideally a preschool teacher or early-childhood specialist reads each book once
   (a small paid review, or a friendly teacher). If you make learning claims on the shop, this also
   supports them.
5. **Real-child test:** read the finished book to 2–3 toddlers. Note which stories hold attention and
   which are skipped, and use that to improve later books.

---

## 9. Roadmap

| Phase | Scope | Result |
|---|---|---|
| **0. Foundations (1–2 weeks)** | Repo layout; story schema; port the 50 existing stories to YAML; rebuild book 1 PDF from YAML with the pipeline; choose the font and palette | One command reproduces a book from content files |
| **1. Prototype book (2 weeks)** | Build **Book 6, "Kind Hearts"** (values test), with 17 new stories and the new elements (Talk about it, Grown-up corner, recap, activity page); first character cast | A complete, polished 48-page book |
| **2. Test the market (2–3 weeks)** | Books 1, 5 and 6 done; 3-story samples; a landing page with Stripe Payment Links; ask 10–20 parents for feedback | Real signals: who buys, what they ask for |
| **3. Build the series (6–10 weeks)** | Books 2–4, 7–10; print target; QA pipeline; educator review | 10 books ready |
| **4. Own shop (3–4 weeks)** | FastAPI site, Stripe Checkout + webhook, signed downloads, email, watermarking, admin page | Live store on your domain |
| **5. Grow** | Commissioned illustration kit, printed books, age 4–6 editions, bundles, bilingual editions | Brand and revenue |

Phases 2 and 3 can overlap. **One person (with Claude doing the heavy lifting on code and drafting)** can do
phases 0–2 in about **6 weeks** part-time; the exact time depends on how much of the writing review you do.

---

## 10. Risks and how to handle them

| Risk | Impact | Response |
|---|---|---|
| Art looks too basic to sell | Low conversion | Free samples, test price, commission the kit with early revenue (section 6) |
| Illustrations inconsistent if AI-made | Brand looks cheap | Use the fixed Python kit; do not generate characters per page |
| Factual mistakes in simplified answers | Loses trust | Fact-check gate and a "grown-up corner" with the real explanation |
| PDF sharing / piracy | Lost sales | Signed links, per-buyer watermark, low price; do not over-engineer DRM |
| Payment bugs (double charge, unpaid access) | Money and trust | Server-side capture, verified webhooks, idempotency, tests |
| Taxes on digital goods | Legal exposure | Check early, or use a merchant-of-record platform at first |
| Burnout writing 150 stories | Project stalls | Batch by book, template the format, release a book at a time |
| Name clashes ("Why Why Why") | Rebrand cost | Search trademarks and domains now |

---

## 11. Success measures

- **Quality:** 3 of 3 test toddlers ask to read it again; parents complete the "Let's try!" on 7 of 10
  stories.
- **Market test (phase 2):** at least 5% of sample downloaders buy; at least 10 parents give feedback.
- **Operations:** a new 20-story book goes from draft to published PDF in about 2 weeks after the
  pipeline is set up.

---

## 12. Decisions made

| # | Question | Decision |
|---|---|---|
| 1 | Series name | **Little Whys.** Every story is a "why" question, and every book title is "Little Whys: <theme>" |
| 2 | Spelling | **Both US and British**, selected when the PDF is generated and by the buyer in the shop (section 5.1) |
| 3 | Market | **Any country.** Payments through **Stripe** (Checkout + Stripe Tax). See section 7.6 for tax filing |
| 4 | Cast | **Recurring characters.** Small cast, returning in every book |
| 5 | Languages | **English only** for now. Content in YAML keeps other languages possible later |
| 6 | Print | **PDF only.** Parents print at home. A print-friendly layout is still built in (clean margins, black-and-white activity page) |
| 7 | Illustration route | Option D: code-drawn first, commission an illustrator later |

Still open: the budget for an educator review and an illustrator, and trademark/domain checks for
"Little Whys".

---

## 13. Build status

| Item | Status |
|---|---|
| Plan | Done (this document) |
| Story schema, validator and US/UK spelling markers | Built and tested |
| **All 200 stories** (50 ported from book 1, 150 new), each with a question, answer, "Let's try!", "Talk about it" and "Grown-up corner" | Written. 10 books, all marked `ready`, 48 pages each |
| Builder: 48-page layout, sample build, per-book covers, stage scenes with 100+ drawn items | Built |
| Free website (FastAPI): catalogue, book pages, US/UK switch, previews, **online reader** (all 48 pages, keyboard, swipe, jump to a story), PDF and sample downloads, parents' guide, About page | Built, 33 tests passing. Deployable with Docker (Render) |
| Stripe checkout, accounts, emails, hosting | **Not started, on purpose** (see 7.7) |
| Fact check, educator review, real-child test (section 8) | **Not done.** The text was written by an AI assistant and has had an automatic check only. Do not sell it before a human review |
| Illustration kit by a real illustrator | Not started. Current pictures are code-drawn placeholders, and many stories share a similar scene |

### Known limits of this first full version

- **Pictures** are simple and repeat across stories. They are fine for a free launch and need an illustrator before paid sales.
- **Content review is the gate.** Facts, safety of activities and tone need a person (ideally an early-childhood educator) before launch.
- One ported sentence (`my-body-17`, hiccups) is longer than the 18-word guideline.
- The site has no accounts, no analytics and no email. That is intentional until payments exist.

---

## Sources and background

- Existing book: `Why_Why_Why_Picture_Book.pdf`, 103 pages, 50 stories, ReportLab, ages 2–4.
- Dialogic reading (asking open questions while reading with a child) is a well-studied method for
  building early language skills.
- Early learning domains used for tags are based on the Head Start Early Learning Outcomes Framework
  (language, cognition, social-emotional, approaches to learning, physical development).
- Stripe Checkout and webhooks: https://docs.stripe.com/payments/checkout and https://docs.stripe.com/webhooks
- Please check current fees, tax rules and print-on-demand specifications before launch; these change.
