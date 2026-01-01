# Angular CLI 如何部署到 GitHub 上並取得 GitHub Pages 網址

若想要將 SPA (Single Page Application) 前端框架 (例如：Angular、React 或 Vue) 部署到 GitHub Pages 時，因為 GitHub Pages 主要是靜態網站托管服務，所以會有不支持處理客戶端路由等問題。

<br />

## Angular CLI 取得 GitHub Pages 網址步驟

1. 首先先進入要進行部屬的專案 Repository 的 Setting 頁籤，在進入側邊欄的 Pages。

2. 找到 Build and deployment 標題，選擇好分支和 Build 完成的資料夾路徑 (這邊選 `master` 分支和 `docs` 資料夾) 後，點選 Save。

    <img src="https://github.com/user-attachments/assets/75e6eb81-f9b3-4a75-bec2-ba5182ae1b8f" width="100%" />

3. 使用指令 `ng build --output-path=docs` 來 Build Angular CLI，指令完成後會出現名為 `docs` 的資料夾。

    <img src="https://github.com/user-attachments/assets/20becf38-2edc-4da3-8121-278fed91de8b" width="100%" />

4. 若 `docs` 資料夾裡像上圖一樣有 `browser` 資料夾和 `server` 資料夾的話，把 `browser` 資料夾內的檔案全部移到 `docs` 資料夾，再把 `browser` 資料夾和 `server` 資料夾刪除。

    <img src="https://github.com/user-attachments/assets/cbd45f96-a29b-43ec-8599-4824cbcbec4b" width="100%" />

5. 最後把檔案全部 Push 到 GitGub 上。
