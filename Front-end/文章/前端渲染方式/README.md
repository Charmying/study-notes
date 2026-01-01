# 前端渲染方式

| 名稱縮寫 | 中文名稱 | 使用時機 | 適用場景 |
| - | - | - | - |
| CSR | 用戶端渲染 | 使用者打開頁面後再渲染 | SPA、內部系統 |
| SSR | 伺服器端渲染 | 使用者請求時即時產生頁面 | SEO 網站、首頁 |
| SSG | 靜態網站生成 | 專案部署前一次性產出頁面 | 文件網站、公司官網 |
| ISR | 增量靜態再生 | 首次用 SSG，過期後重建 | 電商產品頁、新聞內容 |
| CSR + SSR | 混合渲染 (動靜皆可) | 第一頁 SSR，其他 CSR | Next.js 常見模式 |
| SPA | 單頁應用程式 | CSR 的一種表現 | App-like 網站 |
| MPA | 多頁應用程式 | 每頁重新載入與渲染 | 傳統網站、論壇、BBS |
| JAMstack | 靜態 + API 架構 | 搭配 CDN 和 Headless CMS | 文件、行銷頁、個人站 |

<br />

## CSR (Client-Side Rendering，用戶端渲染)

- 時間點：瀏覽器載入 JavaScript 後才產生畫面。

- 代表框架：原生 React、Vue 等 SPA 專案。

- 優點：互動性高，開發彈性。

- 缺點：第一頁慢、SEO 不佳。

<br />

## SSR (Server-Side Rendering，伺服器端渲染)

- 時間點：伺服器每次請求即時回傳完整 HTML。

- 代表框架：Next.js、Nuxt.js (SSR 模式)。

- 優點：利於 SEO、第一頁快。

- 缺點：伺服器壓力較大。

<br />

## SSG (Static Site Generation，靜態網站生成)

- 時間點：部署階段就產生好 HTML。

- 代表框架：Next.js、Nuxt.js (靜態模式)、Gatsby、Hugo。

- 優點：速度最快、安全性高。

- 缺點：更新資料需重新建置，較不適合即時內容。

<br />

## ISR (Incremental Static Regeneration，增量靜態再生)

- 時間點：像是 SSG，但支援「在背景重建特定頁面」。

- 代表框架：Next.js 專屬功能。

- 優點：兼具 SSG 的速度與 SSR 的即時性。

- 缺點：只支援部分框架，且需搭配伺服器或雲平台。

<br />

## SPA (Single Page Application，單頁應用程式)

- 其實是一種應用架構，不是渲染方式本身。

- 所有畫面在同一個頁面切換，不重新載入整頁。

- 常用技術：CSR + 路由切換。

- 適合：後台系統、管理平台、需要登入的 App。

<br />

## MPA (Multi Page Application，多頁應用程式)

- 每次點擊連結就會載入一個全新的 HTML 頁面。

- 適合：傳統網站、論壇、新聞、電商等。

<br />

## 混合渲染 (Hybrid Rendering)

- 有些框架 (例如：Next.js) 允許：

    - 某些頁面用 SSR

    - 某些頁面用 SSG

    - 某些頁面用 CSR

- 優點：根據頁面內容靈活選擇策略。

- 適合：大型平台、SEO 與速度並重的網站。

<br />

## JAMstack (JavaScript, API, Markup)

- 一種網站架構風格，搭配 SSG 與 API。

- 內容來源：Headless CMS、Markdown、API。

- 工具：Netlify、Vercel、Gatsby、Hugo。

- 優點：快、安全、可配雲端無伺服器架構。

- 適合：部落格、行銷頁、作品集。

<br />

## 總結

- 想要互動性強：選 CSR (例如：SPA)

- 想要 SEO 佳與首屏快：選 SSR

- 內容不常更新：選 SSG

- 想要靜態為主但又支援更新：選 ISR

- 想自由混搭：選 Next.js、Nuxt.js
