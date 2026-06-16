(() => {
  const FEEDBACK_STORAGE_KEY = "chat-voyage-feedback-v1";
  const SCORE_VALUES = new Set(["love", "like", "pass"]);

  const albums = window.CHAT_VOYAGE_ALBUMS || [];
  const root = document.querySelector("[data-album-viewer]");
  if (!root || !albums.length) return;

  const params = new URLSearchParams(location.search);
  const requestedSlug = params.get("set");
  let albumIndex = albums.findIndex((item) => item.slug === requestedSlug);
  if (albumIndex < 0) albumIndex = 0;

  const album = albums[albumIndex];
  const images = album.images || [];
  let active = initialImageIndex(images.length);

  const title = document.getElementById("album-title");
  const date = document.getElementById("album-date");
  const count = document.getElementById("album-count");
  const place = document.getElementById("album-place");
  const summary = document.getElementById("album-summary");
  const select = document.getElementById("album-select");
  const stageImage = root.querySelector("[data-stage-image]");
  const stageLink = root.querySelector("[data-stage-link]");
  const caption = root.querySelector("[data-viewer-caption]");
  const openLink = root.querySelector("[data-open-image]");
  const notesLink = root.querySelector("[data-notes-link]");
  const current = root.querySelector("[data-current-image]");
  const total = root.querySelector("[data-total-images]");
  const imageTotal = root.querySelector("[data-image-total]");
  const thumbnailStrip = root.querySelector("[data-thumbnail-strip]");
  const grid = root.querySelector("[data-image-grid]");
  const previous = root.querySelector("[data-album-prev]");
  const next = root.querySelector("[data-album-next]");
  const previousAlbum = root.querySelector("[data-prev-album]");
  const nextAlbum = root.querySelector("[data-next-album]");
  const exportFeedbackButton = document.querySelector("[data-feedback-export]");
  const feedbackStatus = root.querySelector("[data-feedback-status]");
  const scoreButtons = Array.from(root.querySelectorAll("[data-feedback-score]"));
  const tagInputs = Array.from(root.querySelectorAll("[data-feedback-tag]"));
  const noteInput = root.querySelector("[data-feedback-note]");
  const resetFeedbackButton = root.querySelector("[data-feedback-reset]");
  let feedbackStorageMode = "local";
  let feedbackStore = readFeedbackStore();

  hydrateHeader();
  renderThumbnails();
  renderGrid();
  renderNeighbors();
  bindFeedbackControls();
  setActive(active);
  syncCanonicalUrl();

  select?.addEventListener("change", () => {
    if (select.value) location.href = select.value;
  });

  previous?.addEventListener("click", () => setActive(active - 1, true));
  next?.addEventListener("click", () => setActive(active + 1, true));

  document.addEventListener("keydown", (event) => {
    const tag = event.target?.tagName;
    if (tag === "INPUT" || tag === "SELECT" || tag === "TEXTAREA") return;
    if (event.altKey || event.ctrlKey || event.metaKey) return;
    if (event.key === "ArrowLeft") setActive(active - 1, true);
    if (event.key === "ArrowRight") setActive(active + 1, true);
  });

  function hydrateHeader() {
    document.title = `${album.title} - Chat Voyage`;
    title.textContent = album.shortTitle || album.title;
    date.textContent = album.date || "";
    count.textContent = String(images.length);
    place.textContent = (album.places || []).map(labelize).join(", ");
    summary.textContent = album.summary || "";
    total.textContent = String(images.length);
    imageTotal.textContent = `${images.length} images`;

    albums.forEach((item) => {
      const option = document.createElement("option");
      option.value = item.href;
      option.textContent = item.title;
      option.selected = item.slug === album.slug;
      select.appendChild(option);
    });

    if (album.notesHref) {
      notesLink.href = album.notesHref;
      notesLink.hidden = false;
    }
  }

  function renderThumbnails() {
    thumbnailStrip.replaceChildren();
    images.forEach((image, index) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "thumbnail";
      button.dataset.albumThumb = "";
      button.dataset.index = String(index);
      button.setAttribute("aria-pressed", String(index === active));
      button.setAttribute("aria-label", `Show image ${index + 1}: ${image.title || image.alt}`);

      const img = document.createElement("img");
      img.src = image.src;
      img.alt = "";
      img.loading = "lazy";
      img.decoding = "async";

      const label = document.createElement("span");
      label.textContent = image.label || String(index + 1).padStart(2, "0");

      button.append(img, label);
      button.addEventListener("click", () => setActive(index));
      applyFeedbackState(button, image);
      thumbnailStrip.appendChild(button);
    });
  }

  function renderGrid() {
    grid.replaceChildren();
    images.forEach((image, index) => {
      const figure = document.createElement("figure");
      figure.id = `image-${index + 1}`;

      const link = document.createElement("a");
      link.className = "image-link";
      link.href = image.src;

      const img = document.createElement("img");
      img.src = image.src;
      img.alt = image.alt || "";
      img.loading = "lazy";
      img.decoding = "async";

      const figcaption = document.createElement("figcaption");
      const number = document.createElement("p");
      number.className = "image-number";
      number.textContent = image.label || String(index + 1).padStart(2, "0");
      figcaption.append(number, createCaption(image));

      const open = document.createElement("a");
      open.className = "open-image";
      open.href = image.src;
      open.textContent = "Open image";
      figcaption.appendChild(open);

      link.appendChild(img);
      figure.append(link, figcaption);
      grid.appendChild(figure);
    });
  }

  function renderNeighbors() {
    const newer = albums[albumIndex - 1];
    const older = albums[albumIndex + 1];
    setNeighbor(previousAlbum, newer, "Previous album");
    setNeighbor(nextAlbum, older, "Next album");
  }

  function setNeighbor(link, item, label) {
    if (!item) {
      link.hidden = true;
      return;
    }
    link.hidden = false;
    link.href = item.href;
    link.textContent = `${label}: ${item.shortTitle || item.title}`;
  }

  function setActive(index, focusThumb = false) {
    if (!images.length) return;
    active = (index + images.length) % images.length;
    const image = images[active];
    stageImage.src = image.src;
    stageImage.alt = image.alt || "";
    stageLink.href = image.src;
    openLink.href = image.src;
    current.textContent = String(active + 1);
    caption.replaceChildren(createCaption(image));

    thumbnailStrip.querySelectorAll("[data-album-thumb]").forEach((thumb, thumbIndex) => {
      thumb.setAttribute("aria-pressed", String(thumbIndex === active));
      if (thumbIndex === active && focusThumb) focusWithoutScroll(thumb);
    });
    renderFeedback();
  }

  function bindFeedbackControls() {
    scoreButtons.forEach((button) => {
      button.setAttribute("aria-pressed", "false");
      button.addEventListener("click", () => {
        const score = button.dataset.feedbackScore || "";
        const currentFeedback = getCurrentFeedback();
        updateCurrentFeedback({
          score: currentFeedback.score === score ? "" : score,
        });
      });
    });

    tagInputs.forEach((input) => {
      input.addEventListener("change", () => {
        const currentFeedback = getCurrentFeedback();
        const tags = new Set(currentFeedback.tags);
        if (input.checked) tags.add(input.value);
        else tags.delete(input.value);
        updateCurrentFeedback({ tags: Array.from(tags).sort() });
      });
    });

    noteInput?.addEventListener("input", () => {
      updateCurrentFeedback({ note: noteInput.value }, false);
    });

    resetFeedbackButton?.addEventListener("click", () => {
      const key = getCurrentFeedbackKey();
      if (!key) return;
      const nextStore = { ...feedbackStore };
      delete nextStore[key];
      writeFeedbackStore(nextStore);
      renderFeedback();
      renderFeedbackIndicators();
    });

    exportFeedbackButton?.addEventListener("click", exportFeedback);
  }

  function getCurrentFeedbackKey() {
    const image = images[active];
    return image ? getFeedbackKey(album, image) : "";
  }

  function getFeedbackKey(item, image) {
    return `${item.slug}/${image.src}`;
  }

  function getCurrentFeedback() {
    return normalizeFeedback(feedbackStore[getCurrentFeedbackKey()]);
  }

  function updateCurrentFeedback(updates, rerender = true) {
    const key = getCurrentFeedbackKey();
    if (!key) return;
    const nextFeedback = normalizeFeedback({
      ...getCurrentFeedback(),
      ...updates,
      updatedAt: new Date().toISOString(),
    });
    const nextStore = { ...feedbackStore };
    if (hasFeedback(nextFeedback)) nextStore[key] = nextFeedback;
    else delete nextStore[key];
    writeFeedbackStore(nextStore);
    if (rerender) renderFeedback();
    else renderFeedbackStatus(nextFeedback);
    renderFeedbackIndicators();
  }

  function renderFeedback() {
    const feedback = getCurrentFeedback();
    scoreButtons.forEach((button) => {
      const selected = button.dataset.feedbackScore === feedback.score;
      button.setAttribute("aria-pressed", String(selected));
    });
    tagInputs.forEach((input) => {
      input.checked = feedback.tags.includes(input.value);
    });
    if (noteInput && noteInput.value !== feedback.note) {
      noteInput.value = feedback.note;
    }
    renderFeedbackStatus(feedback);
  }

  function renderFeedbackStatus(feedback) {
    if (!feedbackStatus) return;
    if (!hasFeedback(feedback)) {
      feedbackStatus.textContent = "Not saved";
      return;
    }
    feedbackStatus.textContent = feedbackStorageMode === "local" ? "Saved locally" : "Saved for this tab";
  }

  function renderFeedbackIndicators() {
    thumbnailStrip.querySelectorAll("[data-album-thumb]").forEach((thumb, index) => {
      applyFeedbackState(thumb, images[index]);
    });
  }

  function applyFeedbackState(element, image) {
    const feedback = normalizeFeedback(feedbackStore[getFeedbackKey(album, image)]);
    const activeFeedback = hasFeedback(feedback);
    element.classList.toggle("has-feedback", activeFeedback);
    if (feedback.score) element.dataset.feedbackState = feedback.score;
    else delete element.dataset.feedbackState;
  }

  function normalizeFeedback(value) {
    const feedback = value && typeof value === "object" ? value : {};
    const score = SCORE_VALUES.has(feedback.score) ? feedback.score : "";
    const allowedTags = new Set(tagInputs.map((input) => input.value));
    const tags = Array.isArray(feedback.tags)
      ? feedback.tags.filter((tag) => allowedTags.has(tag)).sort()
      : [];
    const note = typeof feedback.note === "string" ? feedback.note : "";
    const updatedAt = typeof feedback.updatedAt === "string" ? feedback.updatedAt : "";
    return { score, tags, note, updatedAt };
  }

  function hasFeedback(feedback) {
    return Boolean(feedback.score || feedback.tags.length || feedback.note.trim());
  }

  function readFeedbackStore() {
    try {
      const raw = window.localStorage?.getItem(FEEDBACK_STORAGE_KEY);
      if (!raw) return {};
      const parsed = JSON.parse(raw);
      return parsed && typeof parsed === "object" ? parsed : {};
    } catch {
      feedbackStorageMode = "memory";
      return {};
    }
  }

  function writeFeedbackStore(nextStore) {
    feedbackStore = nextStore;
    try {
      window.localStorage?.setItem(FEEDBACK_STORAGE_KEY, JSON.stringify(nextStore));
      feedbackStorageMode = "local";
    } catch {
      feedbackStorageMode = "memory";
    }
  }

  function exportFeedback() {
    const entries = Object.entries(feedbackStore)
      .map(([key, value]) => {
        const feedback = normalizeFeedback(value);
        if (!hasFeedback(feedback)) return null;
        const found = findImageByFeedbackKey(key);
        return {
          key,
          albumSlug: found.album?.slug || key.split("/")[0] || "",
          albumTitle: found.album?.title || "",
          imageIndex: found.index >= 0 ? found.index + 1 : null,
          imageSrc: found.image?.src || "",
          imageTitle: found.image?.title || "",
          imageAge: found.image?.age || "",
          imageCategory: found.image?.category || "",
          imageStyle: found.image?.style || "",
          imagePlace: found.image?.place || "",
          ...feedback,
        };
      })
      .filter(Boolean);

    const payload = {
      version: 1,
      source: "Chat Voyage album",
      exportedAt: new Date().toISOString(),
      storageKey: FEEDBACK_STORAGE_KEY,
      entryCount: entries.length,
      entries,
    };

    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `chat-voyage-feedback-${new Date().toISOString().slice(0, 10)}.json`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 0);
  }

  function findImageByFeedbackKey(key) {
    for (const item of albums) {
      const albumImages = item.images || [];
      const index = albumImages.findIndex((image) => getFeedbackKey(item, image) === key);
      if (index >= 0) return { album: item, image: albumImages[index], index };
    }
    return { album: null, image: null, index: -1 };
  }

  function createCaption(image) {
    const fragment = document.createDocumentFragment();
    const heading = document.createElement("h2");
    heading.textContent = image.title || image.alt || "Image";
    fragment.appendChild(heading);

    const rows = [
      ["Age", image.age],
      ["Category", image.category],
      ["Style", image.style],
      ["Place", image.place],
    ].filter(([, value]) => value);
    if (rows.length) {
      const dl = document.createElement("dl");
      rows.forEach(([key, value]) => {
        const dt = document.createElement("dt");
        dt.textContent = key;
        const dd = document.createElement("dd");
        dd.textContent = key === "Age" ? value : labelize(value);
        dl.append(dt, dd);
      });
      fragment.appendChild(dl);
    }
    return fragment;
  }

  function initialImageIndex(length) {
    const match = location.hash.match(/^#image-(\d+)$/);
    if (!match) return 0;
    const index = Number(match[1]) - 1;
    return index >= 0 && index < length ? index : 0;
  }

  function syncCanonicalUrl() {
    if (requestedSlug === album.slug) return;
    const nextUrl = `${location.pathname}?set=${album.slug}${location.hash}`;
    history.replaceState(null, "", nextUrl);
  }

  function focusWithoutScroll(element) {
    try {
      element.focus({ preventScroll: true });
    } catch {
      element.focus();
    }
  }

  function labelize(value) {
    return String(value || "")
      .split("-")
      .filter(Boolean)
      .map((part) => {
        const special = { "3d": "3D", cg: "CG", pbr: "PBR", v2: "V2" };
        return special[part] || part.charAt(0).toUpperCase() + part.slice(1);
      })
      .join(" ");
  }
})();
