# Put Little Whys online (nothing to install)

The site runs from the `Dockerfile` in this repo, so any host that runs Docker works. The easiest is
**Render**, which has a free plan and deploys straight from GitHub.

## Render, step by step (about 10 minutes)

1. Create an account at <https://render.com> and choose **Sign up with GitHub**.
2. Click **New** → **Blueprint**.
3. Connect the `ai-kids-teacher` repository when asked (allow Render to see it).
4. Pick the branch that contains `render.yaml`. Until the pull request is merged, that is
   `claude/trusting-fermi-fzo80g`.
5. Click **Apply**. Render builds the image (about 5 minutes: it installs the packages and builds all 20 PDFs).
6. When it says **Live**, open the address it shows, like `https://little-whys.onrender.com`.

Every time you merge to that branch, Render redeploys automatically (`autoDeploy: true`).

### What to expect on the free plan

- The site **sleeps after about 15 minutes without visitors** and takes roughly 30 to 60 seconds to wake up on the next visit.
- It has little memory (512 MB). That is plenty for browsing and downloads.
- Files are not kept between deploys. That is fine today because the PDFs are built into the image.
  When you add Stripe, orders need a real database, which means a paid plan or an outside database.

## Hidden until you launch

The site tells search engines **not to index it** (`noindex` and `robots.txt`). People with the link can
still open it. When you are ready to be found on Google, add an environment variable in Render:

```
SITE_INDEXABLE=1
```

Please get the human review (fact check, safety, educator read-through) done first. See PLAN section 8.

## Other hosts

- **Fly.io, Railway, Google Cloud Run, a VPS:** point them at the `Dockerfile`. It listens on `$PORT`
  (default 8000) on `0.0.0.0` and answers `/healthz` for health checks.
- **Your own server:** `docker build -t little-whys . && docker run -p 8000:8000 little-whys`.

## Adding a custom domain later

In Render: your service → **Settings** → **Custom Domains**. Buy the domain anywhere and follow the DNS
instructions it shows. HTTPS is added automatically.
