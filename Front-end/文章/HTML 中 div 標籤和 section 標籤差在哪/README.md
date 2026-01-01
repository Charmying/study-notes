# HTML 中 `<div>` 標籤和 `<section>` 標籤差在哪

這是一個非常經典且重要的 HTML5 面試題，也是許多前端開發者在實作時容易混淆的地方。

簡單來說，兩者最大的差別在於語意 (Semantics)：

- `<div>`：沒有任何意義的通用容器，純粹為了 CSS 排版或 JavaScript 操作。

- `<section>`：有明確意義的內容區塊，代表文檔中的一個章節或主題，通常包含一個標題。

<br />

## `<div>` (Division)

`<div>` 是 HTML 中最通用的容器標籤，本身不傳達任何關於內容的訊息。

特點：無語意 (Non-semantic)。瀏覽器和螢幕閱讀器看到 `<div>` 時，只知道這裡把東西包起來了，但不知道為什麼。

主要用途：

- CSS 排版與佈局：例如用來製作 Flexbox 容器、Grid 網格、置中對齊的 Wrapper。

- 樣式修飾：例如需要一個額外的層級來加上陰影、背景色或邊框。

- JavaScript Hook：作為 JavaScript 操作 DOM 的標靶。

使用原則：如果找不到其他更合適的語意標籤 (例如：`<article>`, `<nav>`, `<header>`, `<section>`)，這時才使用 `<div>`。

<br />

## `<section>`

`<section>` 是 HTML5 引入的「語意化標籤」，用來定義文檔中的一個「區段」。

特點：有語意 (Semantic)，告訴瀏覽器和搜尋引擎：「這是一塊有特定主題的內容」。

主要用途：

- 將內容按主題分組 (例如：最新消息區、公司簡介區、聯絡我們區)。

- 通常區塊內會有一個標題 (`<h1>` - `<h6>`)。

Accessibility (無障礙)：螢幕閱讀器使用者可以透過跳轉到不同的 `<section>` 來快速瀏覽網頁架構。

<br />

## 快速比較表

| 特性 | `<div>` | `<section>` |
| - | - | - |
| 語意 | 無 (Generic) | 有 (Thematic grouping) |
| 用途 | 排版、佈局、純容器 | 區分內容主題、章節 |
| 標題需求 | 不強制 | 強烈建議內部要包含標題 (`h1` - `h6`) |
| SEO 影響 | 低 (僅作為結構) | 中高 (幫助搜尋引擎理解結構) |
| 何時使用 | 為了寫 CSS 樣式而需要包一層時 | 當內容是一個獨立主題時 |

<br />

## 程式碼範例對照

### 錯誤用法：濫用 `<section>` 做排版

以下只是為了把兩個按鈕包在一起排版，內容並非一個完整主題，應該用 `<div>`。

```html
<section class="button-wrapper">
  <button>登入</button>
  <button>註冊</button>
</section>
```

### 正確用法：`<section>` 代表特定主題

以下是一個完整的「關於我們」區塊，有標題、有內容。

```html
<section id="about-us">
  <h2>關於我們</h2>
  <p>我們是一間致力於 AI 技術的新創公司...</p>
</section>
```

### 混合用法：`<div>` 在 `<section>` 內部做排版

最常見的情況是外層用 `<section>` 定義區塊，內層用 `<div>` 來排版。

```html
<section id="features">
  <h2>產品特色</h2>
  <div class="grid-container">
    <div class="card">特色 A</div>
    <div class="card">特色 B</div>
    <div class="card">特色 C</div>
  </div>
</section>
```

<br />

## 判斷準則 (Rule of Thumb)

如果正在猶豫要用哪一個，就問自己這個問題：「如果把這個標籤拿掉，只看裡面的內容，能不能構成一個有標題的獨立章節」

- 如果是 → 使用 `<section>` (或是 `<article>`、`<aside>` 等更精確的標籤)

- 如果不是 (只是為了把東西包起來讓 CSS 好寫) → 使用 `<div>`
