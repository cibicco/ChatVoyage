(() => {
  const app = document.querySelector("[data-album-app]");
  if (!app) return;

  const groups = ["month", "place", "category", "occasion", "venue", "activity", "outfit", "style"];
  const groupLabels = {
    month: "月",
    place: "都市",
    category: "旧カテゴリ",
    occasion: "場面",
    venue: "場所",
    activity: "行動",
    outfit: "服装",
    style: "絵柄",
    query: "検索",
  };
  const state = {
    month: "all",
    place: "all",
    category: "all",
    occasion: "all",
    venue: "all",
    activity: "all",
    outfit: "all",
    style: "all",
    query: "",
    sort: "newest",
    view: "grid",
  };

  const cards = Array.from(document.querySelectorAll(".album-card"));
  const search = document.getElementById("album-search");
  const sort = document.getElementById("album-sort");
  const reset = document.getElementById("reset-filters");
  const visibleCount = document.getElementById("visible-count");
  const totalCount = document.getElementById("total-count");
  const activeFilters = document.getElementById("active-filters");
  const emptyState = document.getElementById("empty-state");
  const albums = document.getElementById("albums");
  const filterDrawer = document.querySelector("[data-filter-drawer]");
  const filterSummary = document.querySelector("[data-filter-summary]");

  cards.forEach((card, index) => {
    card.dataset.originalIndex = String(index);
  });
  totalCount.textContent = String(cards.length);

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
    sorted.forEach((card) => albums.appendChild(card));
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
    app.dataset.view = view;
    document.querySelectorAll("[data-view-option]").forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.viewOption === view));
    });
  }

  function updateOptionCounts() {
    groups.forEach((group) => {
      document.querySelectorAll(`[data-filter-group="${group}"] button[data-filter]`).forEach((button) => {
        const value = button.dataset.filter;
        const count = cards.filter((card) => matches(card, { [group]: value })).length;
        const label = button.querySelector(".filter-count");
        if (label) label.textContent = String(count);
      });
    });
  }

  function renderActiveFilters() {
    activeFilters.replaceChildren();
    const entries = [];
    groups.forEach((group) => {
      if (state[group] !== "all") entries.push([group, state[group]]);
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

  function renderFilterSummary(entries) {
    if (!filterSummary) return;
    if (!entries.length) {
      filterSummary.textContent = "すべて";
      return;
    }
    filterSummary.textContent = entries
      .map(([group, value]) => {
        const label = group === "query" ? value : selectedFilterLabel(group, value);
        return `${groupLabels[group] || group}: ${label}`;
      })
      .join(", ");
  }

  function syncUrl() {
    const params = new URLSearchParams();
    groups.forEach((group) => {
      if (state[group] !== "all") params.set(group, state[group]);
    });
    if (state.query) params.set("q", state.query);
    if (state.sort !== "newest") params.set("sort", state.sort);
    if (state.view !== "grid") params.set("view", state.view);
    const query = params.toString();
    const nextUrl = query ? `${location.pathname}?${query}` : location.pathname;
    history.replaceState(null, "", nextUrl);
  }

  function update(pushUrl = true) {
    state.query = normalise(search.value);
    sortCards();
    let visible = 0;
    cards.forEach((card) => {
      const show = matches(card);
      card.classList.toggle("is-hidden", !show);
      if (show) visible += 1;
    });
    visibleCount.textContent = String(visible);
    emptyState.hidden = visible !== 0;
    groups.forEach((group) => setPressed(group, state[group]));
    setView(state.view);
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
    state.view = Array.from(document.querySelectorAll("[data-view-option]")).some((button) => button.dataset.viewOption === viewValue)
      ? viewValue
      : "grid";
    search.value = state.query;
    sort.value = state.sort;
    if (filterDrawer && window.matchMedia("(max-width: 640px)").matches) {
      filterDrawer.open = false;
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
    state.query = "";
    state.sort = "newest";
    state.view = "grid";
    search.value = "";
    sort.value = "newest";
    update();
  });

  restoreFromUrl();
  update(false);
})();
