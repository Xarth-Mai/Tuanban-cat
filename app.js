/* Classic scripts keep the site usable on file:// without fetch or a build step. */
(() => {
  "use strict";

  const character = window.TUANBAN_CHARACTER;
  const lore = window.TUANBAN_LORE;
  const stickers = window.TUANBAN_STICKERS;
  const $ = (id) => document.getElementById(id);

  if (!character || !lore || !Array.isArray(stickers)) {
    $("gallery-status").textContent = "图库数据未完整加载。请确认 data 文件夹与主页在同一目录。";
    return;
  }

  const categories = [
    ["greeting", "问候"], ["happy", "开心"], ["confused", "疑惑"],
    ["comfort", "安慰"], ["sleepy", "困困"], ["daily", "日常"],
    ["playful", "玩闹"], ["shy", "害羞"], ["love", "亲近"]
  ];
  const labels = Object.fromEntries(categories);
  const available = categories.filter(([id]) => stickers.some((item) => item.category === id));
  const dialog = $("sticker-dialog");
  let category = "all";
  let query = "";
  let visible = stickers.slice();
  let selected = 0;

  function node(tag, content, className) {
    const element = document.createElement(tag);
    if (content !== undefined) element.textContent = content;
    if (className) element.className = className;
    return element;
  }

  function pills(target, values) {
    target.replaceChildren(...values.map((value) => node("span", value)));
  }

  $("tagline").textContent = character.tagline;
  $("introduction").textContent = character.introduction;
  $("reference-status").textContent = character.referenceStatus;
  const facts = [
    ["名字", character.name + " / " + character.englishName],
    ["品种", character.breed],
    ["年龄", character.age],
    ["生日", character.birthday]
  ];
  for (const [label, value] of facts) {
    const row = node("div");
    row.append(node("dt", label), node("dd", value));
    $("profile-facts").append(row);
  }
  pills($("personality"), character.personality);
  $("story-copy").replaceChildren(
    ...[lore.paragraphs[0], lore.paragraphs[2]].map((paragraph) => node("p", paragraph))
  );
  $("features").textContent = character.features.join("；") + "。";

  for (const color of character.palette) {
    const item = node("div", undefined, "swatch");
    const chip = node("span", undefined, "swatch-color");
    chip.style.backgroundColor = color.hex;
    chip.setAttribute("aria-hidden", "true");
    const description = node("span", color.name);
    item.append(chip, description);
    $("palette").append(item);
  }

  const categoryOptions = [["all", "全部"], ...available];
  for (const [id, label] of categoryOptions) {
    const count = id === "all" ? stickers.length : stickers.filter((item) => item.category === id).length;
    const button = node("button", label, "filter");
    button.type = "button";
    button.dataset.category = id;
    button.setAttribute("aria-pressed", String(id === "all"));
    button.append(node("span", String(count), "filter-count"));
    button.addEventListener("click", () => {
      category = id;
      render();
    });
    $("filters").append(button);
  }

  $("collection-summary").textContent =
    stickers.length + " 张小表情，" + available.length + " 种心情，慢慢挑一个喜欢的。";
  $("gallery-footer-count").textContent =
    "共 " + stickers.length + " 张贴图 · " + available.length + " 个分类";

  function showSticker(index) {
    if (!visible.length) return;
    selected = (index + visible.length) % visible.length;
    const sticker = visible[selected];
    $("dialog-image").src = sticker.filename;
    $("dialog-image").alt = sticker.description;
    $("dialog-title").textContent = sticker.title;
    $("dialog-category").textContent = labels[sticker.category] || sticker.category;
    $("dialog-description").textContent = sticker.description;
    $("dialog-story").textContent = sticker.story;
    pills($("dialog-tags"), sticker.keywords.slice(0, 4));
    $("dialog-metadata").textContent = "1024 × 1024 · WebP · MPL-2.0";
    $("dialog-download").href = sticker.filename;
    $("dialog-download").download = sticker.id + ".webp";
    $("previous-sticker").disabled = $("next-sticker").disabled = visible.length < 2;
    if (!dialog.open) dialog.showModal();
  }

  function render() {
    const words = query.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    visible = stickers.filter((sticker) => {
      const fullText = [
        sticker.id, sticker.title, sticker.category, labels[sticker.category],
        sticker.description, sticker.story, ...sticker.mood, ...sticker.keywords
      ].join(" ").toLocaleLowerCase();
      return (category === "all" || sticker.category === category) &&
        words.every((word) => fullText.includes(word));
    });

    $("sticker-grid").replaceChildren(...visible.map((sticker, index) => {
      const card = node("article", undefined, "sticker-card");
      const button = node("button", undefined, "sticker-preview");
      button.type = "button";
      button.setAttribute("aria-label", "查看" + sticker.title + "大图");
      const image = node("img");
      image.src = sticker.filename;
      image.alt = sticker.description;
      image.width = image.height = 1024;
      image.loading = "lazy";
      button.append(image);
      button.addEventListener("click", () => showSticker(index));
      const info = node("div", undefined, "sticker-details");
      info.append(node("h3", sticker.title), node("span", labels[sticker.category], "sticker-category"));
      card.append(button, info);
      return card;
    }));

    $("empty-state").hidden = visible.length > 0;
    $("gallery-status").textContent =
      (category === "all" ? "全部表情" : labels[category]) + " · " + visible.length + " 张" +
      (query.trim() ? " · 已筛选" : "");

    for (const button of $("filters").querySelectorAll("button")) {
      button.setAttribute("aria-pressed", String(button.dataset.category === category));
    }
  }

  $("search").addEventListener("input", (event) => {
    query = event.target.value;
    render();
  });
  $("reset-filters").addEventListener("click", () => {
    category = "all";
    query = "";
    $("search").value = "";
    render();
    $("filters").querySelector("button").focus();
  });
  $("dialog-close").addEventListener("click", () => dialog.close());
  $("previous-sticker").addEventListener("click", () => showSticker(selected - 1));
  $("next-sticker").addEventListener("click", () => showSticker(selected + 1));
  dialog.addEventListener("click", (event) => {
    const bounds = dialog.getBoundingClientRect();
    if (event.target === dialog &&
        (event.clientX < bounds.left || event.clientX > bounds.right ||
         event.clientY < bounds.top || event.clientY > bounds.bottom)) {
      dialog.close();
    }
  });
  dialog.addEventListener("keydown", (event) => {
    if (event.key === "ArrowRight") {
      event.preventDefault();
      showSticker(selected + 1);
    }
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      showSticker(selected - 1);
    }
  });
  render();
})();
