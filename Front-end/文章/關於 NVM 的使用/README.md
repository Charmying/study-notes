# 關於 NVM 的使用

一開始是看到有人在下載 Node.js 時是直接去官網下載，雖然沒有不可以，但是若已經在官網下載了任一版本，之後想使用 NVM 來下載其他版本並切換時會失敗，需要先去電腦的設定中刪掉在官網下載的版本才能完全使用 NPM 進行操作。

NVM (Node Version Manager) 是一個管理 Node.js 版本的工具，能夠輕鬆在不同的 Node.js 版本之間切換。在開發 JavaScript 應用程式或是使用 Node.js 相關的工具時，某些專案可能會依賴特定的 Node.js 版本。透過 NVM 可以安裝、使用以及管理多個 Node.js 版本，避免在開發環境中產生衝突或不相容的問題。

<br />

## 安裝 & 使用 NVM

由於沒有用過 Unix 系統 (例如：macOS、Linux)，所以以下提供 Windows 系統的安裝方法。

在 Windows 系統上，安裝 NVM 有一個專門的工具叫 nvm-windows，是 Windows 的 NVM 版本。

1. 下載 nvm-windows 安裝包

    - 前往 [nvm-windows 的 GitHub 頁面](https://github.com/coreybutler/nvm-windows/releases)。

    - 找到最新的發佈版本，點擊下載 `nvm-setup.exe`。

2. 解壓並安裝

    - 若是點擊下載 `nvm-setup.zip`，那就需要解壓縮 `nvm-setup.zip`，然後執行其中的 `nvm-setup.exe` 安裝程式

    - 安裝過程中，會要求選擇安裝路徑，建議使用默認設置。

3. 設定環境變數

    安裝過程會自動配置系統環境變數，不過還是可以手動檢查

    - 打開 系統設定 -> 高級系統設置 -> 環境變數，並檢查 `NVM_HOME` 和 `NVM_SYMLINK` 是否已經正確添加到環境變數中。

        - `NVM_HOME` 指向的是 NVM 的安裝路徑 (例如：C:\Program Files\nvm)。

        - `NVM_SYMLINK` 是 Node.js 的符號鏈接路徑 (例如：C:\Program Files\nodejs)。

4. 開啟終端機 (Terminal)

    接下來開啟 CMD (命令提示字元) 或 Windows PowerShell 來使用 NVM 的指令了 (沒有嘗試過其他終端機不確定是否可以使用，但是應該可以)。

<br />

## NVM 的相關指令

- 檢查 NVM 版本

    ```text
    nvm version
    ```

- 安裝 Node.js

    - 安裝 Node.js 最新的 LTS 版本

    	```text
    	nvm install lts
    	```

    - 安裝特定版本的 Node.js

    	```text
    	nvm install 18.20.3
    	```

- 解除安裝 Node.js

    ```text
    nvm uninstall 18.20.3
    ```

- 檢查已經有的 Node.js 版本

    ```text
    nvm list
    ```

    會出現已經下載的 Node.js 版本，現在正在使用的版本前面會出現 `*`。

- 切換 Node.js 版本

    ```text
    nvm use 版本號
    ```

- 檢查目前使用的 Node.js 版本

    雖然 nvm list 可以直接檢查現行的 Node.js 版本，但是以下的指令比較正規準確。

    ```text
    node --version
    ```

    或簡寫

    ```text
    node -v
    ```
