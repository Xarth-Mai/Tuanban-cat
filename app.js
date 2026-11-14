/* Classic scripts deliberately support file://. No fetch, imports, framework, or remote requests. */
(() => {
  "use strict";
  const character = window.TUANBAN_CHARACTER;
  const lore = window.TUANBAN_LORE;
  const stickers = window.TUANBAN_STICKERS;
  const $ = (id) => document.getElementById(id);
  if (!character || !lore || !Array.isArray(stickers)) {
    $("gallery-status").textContent = "图库数据未完整加载。请确认 data 文件夹和 index.html 在同一目录。";
    return;
  }
  const categories = [
    ["all", "全部"], ["greeting", "问候"], ["happy", "开心"], ["confused", "疑惑"],
    ["comfort", "安慰"], ["sleepy", "困困"], ["daily", "日常"], ["playful", "玩闹"],
    ["shy", "害羞"], ["love", "亲近"]
  ];
  const labels = Object.fromEntries(categories);
  let category = "all";
  let query = "";
  let visible = stickers.slice();
  let selected = 0;
  const dialog = $("sticker-dialog");
  function node(tag, text, className) {
    const el = document.createElement(tag);
    if (text !== undefined) el.textContent = text;
    if (className) el.className = className;
    return el;
  }
  function pills(target, values) {
    target.replaceChildren(...values.map((value) => node("span", value)));
  }
  $("tagline").textContent = character.tagline;
  $("introduction").textContent = character.introduction;
  $("reference-status").textContent = character.referenceStatus;
  const facts = [["名字", `${character.name} / ${character.englishName}`], ["性别", character.gender],
    ["品种", character.breed], ["年龄", character.age], ["生日", character.birthday]];
  for (const [label, value] of facts) {
    const row = node("div");
    row.append(node("dt", label), node("dd", value));
    $("profile-facts").append(row);
  }
  pills($("personality"), character.personality);
  for (const id of ["likes", "dislikes"]) {
    $(id).replaceChildren(...character[id].map((text) => node("li", text)));
  }
  $("features").textContent = character.features.join("；") + "。";
  $("story-copy").replaceChildren(...lore.paragraphs.map((text) => node("p", text)));
  for (const moment of lore.moments) {
    const card = node("article", undefined, "moment");
    card.append(node("span", moment.number, "moment-number"), node("h3", moment.title), node("p", moment.text));
    $("story-moments").append(card);
  }
  for (const color of character.palette) {
    const swatch = node("div", undefined, "swatch");
    const chip = node("span", undefined, "swatch-color");
    chip.style.backgroundColor = color.hex;
    chip.setAttribute("aria-hidden", "true");
    const description = node("p", color.name);
    description.append(node("code", color.hex));
    swatch.append(chip, description);
    $("palette").append(swatch);
  }
  pills($("style-words"), character.style);
  for (const [id, label] of categories) {
    const button = node("button", label, "filter");
    button.type = "button";
    button.dataset.category = id;
    button.setAttribute("aria-pressed", String(id === category));
    const count = id === "all" ? stickers.length : stickers.filter((s) => s.category === id).length;
    button.append(node("span", String(count), "filter-count"));
    button.addEventListener("click", () => { category = id; render(); });
    $("filters").append(button);
  }
  function showSticker(index) {
    if (!visible.length) return;
    selected = (index + visible.length) % visible.length;
    const sticker = visible[selected];
    $("dialog-image").src = sticker.filename;
    $("dialog-image").alt = sticker.description;
    $("dialog-title").textContent = sticker.title;
    $("dialog-category").textContent = `${labels[sticker.category]} / ${sticker.category.toUpperCase()}`;
    $("dialog-description").textContent = sticker.description;
    $("dialog-story").textContent = sticker.story;
    pills($("dialog-tags"), sticker.keywords);
    $("dialog-metadata").textContent = `1024 × 1024 · WebP · v${sticker.version} · MPL-2.0`;
    $("dialog-download").href = sticker.filename;
    $("dialog-download").download = `${sticker.id}.webp`;
    $("previous-sticker").disabled = $("next-sticker").disabled = visible.length < 2;
    if (!dialog.open) dialog.showModal();
  }
  function render() {
    const words = query.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    visible = stickers.filter((sticker) => {
      const text = [sticker.id, sticker.title, sticker.category, labels[sticker.category], sticker.description,
        sticker.story, ...sticker.mood, ...sticker.keywords].join(" ").toLocaleLowerCase();
      return (category === "all" || sticker.category === category) && words.every((word) => text.includes(word));
    });
    const cards = visible.map((sticker, index) => {
      const card = node("article", undefined, "sticker-card");
      const button = node("button", undefined, "sticker-preview");
      button.type = "button";
      button.setAttribute("aria-label", `查看${sticker.title}大图及使用场景`);
      const image = node("img");
      image.src = sticker.filename;
      image.alt = sticker.description;
      image.width = image.height = 1024;
      image.loading = "lazy";
      const plus = node("span", "+", "preview-plus");
      plus.setAttribute("aria-hidden", "true");
      button.append(image, plus);
      button.addEventListener("click", () => showSticker(index));
      const heading = node("div", undefined, "sticker-details");
      heading.append(node("h3", sticker.title), node("span", labels[sticker.category], "sticker-category"));
      card.append(button, heading, node("p", sticker.keywords.slice(0, 3).join(" · "), "sticker-caption"));
      return card;
    });
    $("sticker-grid").replaceChildren(...cards);
    $("empty-state").hidden = visible.length > 0;
    $("gallery-status").textContent = `${labels[category]} · ${visible.length} 张贴图${query.trim() ? " · 已按关键词筛选" : ""}`;
    for (const button of $("filters").querySelectorAll("button")) {
      button.setAttribute("aria-pressed", String(button.dataset.category === category));
    }
  }
  $("search").addEventListener("input", (event) => { query = event.target.value; render(); });
  $("reset-filters").addEventListener("click", () => {
    category = "all"; query = ""; $("search").value = ""; render(); $("filters").querySelector("button").focus();
  });
  $("dialog-close").addEventListener("click", () => dialog.close());
  $("previous-sticker").addEventListener("click", () => showSticker(selected - 1));
  $("next-sticker").addEventListener("click", () => showSticker(selected + 1));
  dialog.addEventListener("click", (event) => {
    const bounds = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < bounds.left || event.clientX > bounds.right ||
        event.clientY < bounds.top || event.clientY > bounds.bottom)) dialog.close();
  });
  dialog.addEventListener("keydown", (event) => {
    if (event.key === "ArrowRight") { event.preventDefault(); showSticker(selected + 1); }
    if (event.key === "ArrowLeft") { event.preventDefault(); showSticker(selected - 1); }
  });
  render();
})();
