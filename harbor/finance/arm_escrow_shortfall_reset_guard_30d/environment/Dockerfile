# Must stay buildable from a public base alone: this bundle is built by whoever
# receives it, on a machine that has none of the author's local images. A
# `FROM <locally-built-image>` here fails with "pull access denied" there, and a
# structural delivery check cannot catch it — such checks inspect compose's
# `image:` keys, never a Dockerfile FROM.
#
# The default base is therefore public and the build needs nothing else. The ARG
# exists only so a caller who has pre-baked a heavier base (node + the agent CLI,
# to save time across repeated local runs) can opt in at build time:
#
#   docker build --build-arg BASE_IMAGE=<your-prebaked-image> \
#     -f environment/Dockerfile -t <tag> environment/
#
# Override the ARG; never edit FROM.
ARG BASE_IMAGE=python:3.12-slim
FROM ${BASE_IMAGE}

# Idempotent: a no-op when the pre-baked base already carries these.
#
# The build network's proxy intermittently answers 502 for deb.debian.org —
# observed once on a trixie-updates InRelease fetch and once on a jq .deb —
# which failed the whole compose build on a single transient response. Two
# layers of defense: apt's per-fetch retries (covers an individual InRelease or
# .deb), and an outer loop that re-runs the update+install pair. The loop keeps
# the build loud: if apt never succeeds the RUN still exits 1.
RUN ok=0; \
    for attempt in 1 2 3 4; do \
      if apt-get update -o Acquire::Retries=10 \
         && apt-get install -y --no-install-recommends -o Acquire::Retries=10 \
             bash ca-certificates coreutils curl jq procps sqlite3; then \
        ok=1; break; \
      fi; \
      echo "apt attempt $attempt failed; retrying after backoff"; \
      sleep 15; \
    done; \
    [ "$ok" = 1 ] || { echo "apt-get failed after 4 attempts"; exit 1; }; \
    rm -rf /var/lib/apt/lists/*

# --retries: pip defaults to 5; raise it to ride out the same proxy flakiness
# that hit apt above.
#
# Core mcp only. The task's client code uses ClientSession and
# streamablehttp_client; the [cli] extra pulls a typer/rich chain that cannot be
# resolved against mcp 1.25.0's pydantic pin, so requesting it makes this image
# unbuildable while adding nothing the task uses.
RUN pip install --no-cache-dir --retries 10 \
    "mcp==1.25.0" \
    "PyYAML==6.0.3" \
    "loguru==0.7.3"

# Codex tuning, baked into Codex's Unix system layer so the package is
# self-contained. Harbor recreates /tmp/codex-home for each step, writes its
# base URL and MCP settings to that user layer, then removes $CODEX_HOME in the
# step cleanup. A config baked there therefore disappears before the first
# `codex exec resume --last`; /etc/codex/config.toml survives that lifecycle,
# and Codex merges it with Harbor's per-step user config.
#
# model_auto_compact_token_limit: every step resumes the same session, so the
# conversation grows monotonically. Measured on this task set it reaches the
# 196,608-token window around step 20; compacting at 150,000 keeps later steps
# from repeatedly processing a full window. Compaction replacement history is
# persisted in the session and is available to later resume processes.
#
# web_search: this task talks only to vendored mocks. Codex 0.146.0 expects the
# top-level enum `web_search = "disabled"`; the deprecated boolean form
# `[tools] web_search = false` is accepted but silently deserializes to no
# override, so do not replace this with that form.
RUN mkdir -p /etc/codex \
    && printf 'model = "sub2api-gpt-5.6-sol"\nmodel_reasoning_effort = "xhigh"\nmodel_auto_compact_token_limit = 150000\nweb_search = "disabled"\n' \
       > /etc/codex/config.toml

COPY evidence-collector /opt/evidence-collector
RUN chmod +x /opt/evidence-collector/collect

WORKDIR /workspace
USER root
