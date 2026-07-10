(() => {
  const app = document.querySelector("[data-album-app]");
  if (!app) return;

  const groups = ["collection", "character", "month", "place", "occasion", "venue", "activity", "outfit", "style"];
  const advancedGroups = ["place", "occasion", "venue", "activity", "outfit", "style"];
  const DEFAULT_COLLECTION = "character";
  const groupLabels = {
    collection: "アルバム",
    character: "人物",
    month: "月",
    place: "都市",
    occasion: "場面",
    venue: "場所",
    activity: "行動",
    outfit: "服装",
    style: "絵柄",
    query: "検索",
  };
  const state = {
    collection: DEFAULT_COLLECTION,
    character: "all",
    month: "all",
    place: "all",
    occasion: "all",
    venue: "all",
    activity: "all",
    outfit: "all",
    style: "all",
    query: "",
    sort: "newest",
    view: "grid",
    size: "small",
  };

  const cards = Array.from(document.querySelectorAll(".album-card"));
  const dateTiles = Array.from(document.querySelectorAll(".date-image-tile"));
  const search = document.getElementById("album-search");
  const sort = document.getElementById("album-sort");
  const reset = document.getElementById("reset-filters");
  const visibleCount = document.getElementById("visible-count");
  const totalCount = document.getElementById("total-count");
  const resultUnit = document.querySelector("[data-result-unit]");
  const activeFilters = document.getElementById("active-filters");
  const emptyState = document.getElementById("empty-state");
  const albumSections = Array.from(document.querySelectorAll("[data-album-section]"));
  const albumLists = Array.from(document.querySelectorAll("[data-album-list]"));
  const listsByCollection = new Map(albumLists.map((list) => [list.dataset.albumList, list]));
  const dateSections = Array.from(document.querySelectorAll("[data-date-image-section]"));
  const dateBrowser = document.querySelector("[data-date-image-browser]");
  const filterDrawer = document.querySelector("[data-filter-drawer]");
  const filterSummary = document.querySelector("[data-filter-summary]");
  const sizeButtons = Array.from(document.querySelectorAll("[data-size-option]"));

  cards.forEach((card, index) => {
    card.dataset.originalIndex = String(index);
  });
  dateTiles.forEach((tile, index) => {
    tile.dataset.originalIndex = String(index);
  });
  totalCount.textContent = String(cards.filter((card) => valuesFor(card, "collection").includes(DEFAULT_COLLECTION)).length);

  function activeItems() {
    return isDateMode() ? dateTiles : cards;
  }

  function isDateMode() {
    return state.sort === "date-groups";
  }

  function normalise(value) {
    return (value || "").trim().toLowerCase();
  }

  function valuesFor(card, group) {
    return (card.dataset[group] || "").split(" ").filter(Boolean);
  }

  function matches(card, overrides = {}) {
    const next = { ...state, ...overrides };
    for (const group of groups) {
      if (next[group] !== "all" && !valuesFor(card, group).includes(next[group])) {
        return false;
      }
    }
    if (next.query && !(card.dataset.search || "").includes(next.query)) {
      return false;
    }
    return true;
  }

  function compareText(a, b, key) {
    return (a.dataset[key] || "").localeCompare(b.dataset[key] || "");
  }

  function compareDateDesc(a, b) {
    const byDate = (b.dataset.date || "").localeCompare(a.dataset.date || "");
    if (byDate) return byDate;
    return Number(a.dataset.originalIndex) - Number(b.dataset.originalIndex);
  }

  function sortCards() {
    const sorted = [...cards].sort((a, b) => {
      if (state.sort === "oldest") {
        return (a.dataset.date || "").localeCompare(b.dataset.date || "");
      }
      if (state.sort === "city") {
        return compareText(a, b, "city") || compareDateDesc(a, b);
      }
      if (state.sort === "title") {
        return compareText(a, b, "title");
      }
      if (state.sort === "images") {
        return Number(b.dataset.imageCount || 0) - Number(a.dataset.imageCount || 0) || compareDateDesc(a, b);
      }
      return compareDateDesc(a, b);
    });
    sorted.forEach((card) => {
      const collection = state.collection === "all" ? "all" : card.dataset.collection || "daily";
      const list = listsByCollection.get(collection) || listsByCollection.get("daily") || albumLists[0];
      if (list) list.appendChild(card);
    });
  }

  function setPressed(group, value) {
    document.querySelectorAll(`[data-filter-group="${group}"] button[data-filter]`).forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.filter === value));
    });
  }

  function isValidFilter(group, value) {
    return Array.from(document.querySelectorAll(`[data-filter-group="${group}"] button[data-filter]`)).some((button) => {
      return button.dataset.filter === value;
    });
  }

  function selectedFilterLabel(group, value) {
    const button = Array.from(document.querySelectorAll(`[data-filter-group="${group}"] button[data-filter]`)).find((item) => {
      return item.dataset.filter === value;
    });
    return button?.querySelector(".filter-text")?.textContent || value;
  }

  function setView(view) {
    app.dataset.view = isDateMode() ? "date" : view;
    document.querySelectorAll("[data-view-option]").forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.viewOption === view));
    });
  }

  function setSize(size) {
    app.dataset.imageSize = size;
    sizeButtons.forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.sizeOption === size));
    });
  }

  function updateOptionCounts() {
    const items = activeItems();
    groups.forEach((group) => {
      document.querySelectorAll(`[data-filter-group="${group}"] button[data-filter]`).forEach((button) => {
        const value = button.dataset.filter;
        const count = items.filter((item) => matches(item, { [group]: value })).length;
        const label = button.querySelector(".filter-count");
        if (label) label.textContent = String(count);
        const isZero = count === 0;
        button.classList.toggle("is-zero", isZero);
        button.disabled = isZero && button.getAttribute("aria-pressed") !== "true";
      });
    });
  }

  function renderActiveFilters() {
    activeFilters.replaceChildren();
    const entries = [];
    groups.forEach((group) => {
      if (group !== "collection" && state[group] !== "all") entries.push([group, state[group]]);
    });
    if (state.query) entries.push(["query", state.query]);
    entries.forEach(([group, value]) => {
      const chip = document.createElement("button");
      chip.type = "button";
      chip.dataset.clearFilter = group;
      const label = group === "query" ? value : selectedFilterLabel(group, value);
      chip.textContent = `${groupLabels[group] || group}: ${label}`;
      activeFilters.appendChild(chip);
    });
    renderFilterSummary(entries);
  }

  function updateSectionCounts() {
    const visibleByCollection = new Map();
    albumSections.forEach((section) => {
      const collection = section.dataset.albumSection;
      const sectionCards = collection === "all"
        ? cards
        : cards.filter((card) => (card.dataset.collection || "daily") === collection);
      const visible = sectionCards.filter((card) => !card.classList.contains("is-hidden")).length;
      const count = section.querySelector(`[data-section-count="${collection}"]`);
      if (count) count.textContent = String(visible);
      if (collection === "all") {
        section.hidden = state.collection !== "all" || visible === 0 || isDateMode();
      } else {
        section.hidden = state.collection === "all" || visible === 0 || isDateMode();
      }
      visibleByCollection.set(collection, visible);
    });
  }

  function updateDateSections() {
    dateSections.forEach((section) => {
      const tiles = Array.from(section.querySelectorAll(".date-image-tile"));
      const visible = tiles.filter((tile) => !tile.classList.contains("is-hidden")).length;
      const count = section.querySelector("[data-date-visible-count]");
      if (count) count.textContent = String(visible);
      section.hidden = visible === 0;
    });
    if (dateBrowser) {
      dateBrowser.hidden = !isDateMode();
    }
  }

  function renderFilterSummary(entries) {
    if (!filterSummary) return;
    const visibleEntries = entries.filter(([group]) => group !== "collection");
    if (!visibleEntries.length) {
      filterSummary.textContent = "すべて";
      return;
    }
    filterSummary.textContent = visibleEntries
      .map(([group, value]) => {
        const label = group === "query" ? value : selectedFilterLabel(group, value);
        return `${groupLabels[group] || group}: ${label}`;
      })
      .join(", ");
  }

  function syncUrl() {
    const params = new URLSearchParams();
    groups.forEach((group) => {
      if (group === "collection") {
        if (state.collection !== DEFAULT_COLLECTION) params.set(group, state.collection);
        return;
      }
      if (state[group] !== "all") params.set(group, state[group]);
    });
    if (state.query) params.set("q", state.query);
    if (state.sort !== "newest") params.set("sort", state.sort);
    if (state.view !== "grid") params.set("view", state.view);
    if (state.size !== "small") params.set("size", state.size);
    const query = params.toString();
    const nextUrl = query ? `${location.pathname}?${query}` : location.pathname;
    history.replaceState(null, "", nextUrl);
  }

  function update(pushUrl = true) {
    state.query = normalise(search.value);
    sortCards();
    const items = activeItems();
    const currentCollectionTotal = items.filter((item) => {
      return state.collection === "all" || valuesFor(item, "collection").includes(state.collection);
    }).length;
    let visible = 0;
    cards.forEach((card) => {
      const show = matches(card);
      card.classList.toggle("is-hidden", !show);
    });
    dateTiles.forEach((tile) => {
      const show = matches(tile);
      tile.classList.toggle("is-hidden", !show);
    });
    items.forEach((item) => {
      if (!item.classList.contains("is-hidden")) visible += 1;
    });
    visibleCount.textContent = String(visible);
    totalCount.textContent = String(currentCollectionTotal);
    if (resultUnit) resultUnit.textContent = isDateMode() ? "枚" : "件";
    emptyState.hidden = visible !== 0;
    updateSectionCounts();
    updateDateSections();
    groups.forEach((group) => setPressed(group, state[group]));
    setView(state.view);
    setSize(state.size);
    updateOptionCounts();
    renderActiveFilters();
    if (pushUrl) syncUrl();
  }

  function restoreFromUrl() {
    const params = new URLSearchParams(location.search);
    groups.forEach((group) => {
      const value = params.get(group);
      if (value && isValidFilter(group, value)) state[group] = value;
    });
    state.query = normalise(params.get("q") || "");
    const sortValue = params.get("sort") || "newest";
    state.sort = Array.from(sort.options).some((option) => option.value === sortValue) ? sortValue : "newest";
    const viewValue = params.get("view") || "grid";
    if (viewValue === "date") state.sort = "date-groups";
    state.view = Array.from(document.querySelectorAll("[data-view-option]")).some((button) => button.dataset.viewOption === viewValue)
      ? viewValue
      : "grid";
    const sizeValue = params.get("size") || "small";
    state.size = sizeButtons.some((button) => button.dataset.sizeOption === sizeValue) ? sizeValue : "small";
    search.value = state.query;
    sort.value = state.sort;
    if (filterDrawer) {
      filterDrawer.open = advancedGroups.some((group) => state[group] !== "all");
    }
  }

  document.querySelectorAll("[data-filter-group]").forEach((groupEl) => {
    const group = groupEl.dataset.filterGroup;
    groupEl.addEventListener("click", (event) => {
      const button = event.target.closest("button[data-filter]");
      if (!button) return;
      state[group] = button.dataset.filter;
      update();
    });
  });

  document.querySelectorAll("[data-view-option]").forEach((button) => {
    button.addEventListener("click", () => {
      state.view = button.dataset.viewOption;
      update();
    });
  });

  sizeButtons.forEach((button) => {
    button.addEventListener("click", () => {
      state.size = button.dataset.sizeOption || "small";
      update();
    });
  });

  activeFilters.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-clear-filter]");
    if (!button) return;
    const key = button.dataset.clearFilter;
    if (key === "query") {
      search.value = "";
      state.query = "";
    } else if (groups.includes(key)) {
      state[key] = "all";
    }
    update();
  });

  search.addEventListener("input", () => update());
  sort.addEventListener("change", () => {
    state.sort = sort.value;
    update();
  });
  reset.addEventListener("click", () => {
    groups.forEach((group) => {
      state[group] = "all";
    });
    state.collection = DEFAULT_COLLECTION;
    state.query = "";
    state.sort = "newest";
    state.view = "grid";
    state.size = "small";
    search.value = "";
    sort.value = "newest";
    update();
  });

  restoreFromUrl();
  update(false);
})();
