(() => {
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

  hydrateHeader();
  renderThumbnails();
  renderGrid();
  renderNeighbors();
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
