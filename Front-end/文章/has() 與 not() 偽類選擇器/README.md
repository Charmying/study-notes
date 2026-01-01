# `:has()` 與 `:not()` 偽類選擇器

在 CSS 中，`:has()` 與 `:not()` 是兩個強大的偽類選擇器，能夠根據元素的子元素結構或排除條件來設定樣式，讓樣式控制更加靈活。

<br />

## `:has()` 偽類選擇器

`:has()` 用來選擇包含指定子元素的元素，用來接受一個或多個選擇器作為參數，當目標元素內部符合所指定條件的子元素存在時，該元素就會被選中。

### 基本語法

```css
selector:has(selector)
```

`selector`：要檢查的元素選擇器。

### 範例

```css
div:has(.red) {
  background-color: red;
}
```

上述 CSS 將會選中包含 `.red` 類別元素的所有 `div` 元素，並將其背景顏色設為紅色。

```css
figure:has(.caption) {
  border: 1px solid black;
}
```

這段 CSS 會將包含 `.caption` 元素的 `figure` 元素設定為黑色邊框。

```css
div:has(ul) {
  padding: 10px;
}
```

若 `div` 元素中有一個 `ul` 就會套用 `padding: 10px;` 的樣式。

### 瀏覽器支援提醒

- `:has()` 是一項相對較新的 CSS 功能，目前支援

    - ✅ Chrome 105+

    - ✅ Safari 15.4+

    - ✅ Edge 105+

    - ❌ Firefox 尚未支援 (截至 2025 年 6 月)

- 若需兼容 Firefox，可考慮使用 JavaScript 進行 DOM 檢測與樣式套用。

<br />

## `:not()` 偽類選擇器

`:not()` 用來選擇不符合特定條件的元素，常用於排除某些類別或元素類型。

### 基本語法

```css
selector:not(selector)
```

`selector`：要排除的選擇器。

### 範例

```css
.red :not(img) {
  background-color: blue;
}
```

這段 CSS 會將 `.red` 類別元素中的所有非 `img` 子元素的背景顏色設定為藍色。

```css
img:not(.large) {
  width: 100px;
}
```

設定所有沒有 `.large` 類別的圖片寬度為 `100px`。

```css
.red:not(:has(ul)) {
  font-size: 18px;
}
```

會將所有 `.red` 類別但不包含 `ul` 元素的元素字體大小設定為 `18px`。

<br />

## `:has()` 與 `:not()` 的搭配使用

這兩個選擇器可以結合，進一步建立更細緻的條件樣式。例如：以下樣式會選擇所有不包含圖片的 section 元素：

```css
section:not(:has(img)) {
  opacity: 0.5;
}
```

<br />

## 注意事項

- `:not()` 的優先級 (Specificity) 說明

    - `:not()` 本身不增加優先級，但內部的選擇器會被計入優先級。

    - 例如：`div:not(.active)` 的優先級與 `div.active` 相同。

- 不能選擇父元素的傳統限制已被突破

    - `:has()` 是少數可以向上影響父元素樣式的 CSS 選擇器，在過去必須用 JavaScript 來實現。

- 效能考量

    - `:has()` 在大型 DOM 結構中可能影響效能，尤其在選擇器嵌套使用時。

<br />

## 總結

`:has()` 與 `:not()` 提供了強大的條件選擇能力，可以讓樣式設計更具彈性。不過，開發人員在使用時需注意

- `:has()` 的瀏覽器兼容性 (特別是 Firefox 尚未支援)。

- 使用這些選擇器時應保持結構清晰，避免過度複雜的選擇器造成維護困難與效能問題。

若搭配合適的結構與瀏覽器檢查策略，這兩個偽類選擇器將大幅提升 CSS 表現力。
