# GitLab Runner

GitLab Runner 是一個工具，主要用於執行自動化的任務和工作流程，尤其是在軟體開發的過程中。

GitLab Runner 是 GitLab 開發的開源專案，專門設計用來執行 GitLab CI/CD Pipeline 中的任務。這些任務可涵蓋程式碼的編譯、測試到部署等自動化操作。Runner 可以部署在不同的平台和環境中，並能根據需求動態分配與執行任務。

<br />

## GitLab Runner 的主要功能

- 自動化測試與部署：可自動執行測試、構建、打包和部署，協助團隊在提交程式碼時即時檢查品質並快速交付。

- 多平台支持：支援 Linux、macOS、Windows，以及 Docker、Shell、Kubernetes 等執行環境，具備高度靈活性。

- 並行執行：允許同時運行多個作業，加快流程。

- 自定義執行環境：透過 Docker 保證每次執行環境一致。

- 彈性與擴展性：可依需求增加 Runner，提升處理能力。

- 多種執行模式：依專案需求選擇不同模式

    - Shell executor (Shell 執行器)：直接在主機 Shell 中執行。

    - Docker executor (Docker 執行器)：於 Docker 容器中執行，確保環境一致性。

    - Kubernetes executor (Kubernetes 執行器)：在 Kubernetes 叢集上執行，適合大規模任務。

<br />

## GitLab Runner 的運作原理

1. 註冊 Runner

    將 Runner 註冊至 GitLab，取得專屬 Token 綁定專案或整個 GitLab 實例，GitLab 才能調用 Runner。

2. 配置 CI/CD Pipeline

    使用 `.gitlab-ci.yml` 定義 Pipeline，內容包括作業 (Jobs) 與階段 (Stages)。

    ```yaml
    stages:
      - build
      - test
      - deploy

    build_job:
      stage: build
      script:
        - echo "Building the app..."
        - npm install
        - npm run build

    test_job:
      stage: test
      script:
        - echo "Running tests..."
        - npm test

    deploy_job:
      stage: deploy
      script:
        - echo "Deploying to production..."
        - ./deploy.sh
    ```

    上面定義了三個階段：`build`、`test`、`deploy`，Runner 會依序執行。

3. 執行作業

    當程式碼提交至指定分支時，CI/CD Pipeline 會被觸發，Runner 依照設定下載並執行作業，完成後回傳結果。

4. 報告與通知

    結果 (成功或失敗) 會回傳 GitLab，並可透過 Email、Slack 等方式通知相關人員。

<br />

## GitLab Runner 的優缺點

### 優點

- 多平台支持：支援多作業系統與多執行模式 (Shell、Docker、Kubernetes)。

- 靈活配置：可使用 `.gitlab-ci.yml` 精細定義 Pipeline 與條件。

- 自動化與高效率：支援並行作業，減少人工干預並加速交付。

- 可擴展性：支援分散式架構與彈性伸縮，適應動態工作負載。

- 開源社群支持：活躍的社群、plugin 資源與持續更新。

### 缺點

- 學習曲線：需熟悉 CI/CD、Docker、Kubernetes 等技術。

- 資源消耗：大型專案可能需大量計算資源，管理也更複雜。

- 整合挑戰：與外部工具或平台整合時，可能需要額外配置。

- 依賴外部技術：功能多依賴 Docker 與 Kubernetes，增加運維負擔。

<br />

## 如何最大化 GitLab Runner 的優勢

- 精細化配置 Pipeline：準確定義作業流程與執行環境。

- 優化資源使用：監控並調整 Runner 資源，避免浪費。

- 持續學習與社群參與：跟進最新功能與最佳實踐。

- 定期審查與優化：確保 CI/CD Pipeline 隨專案規模與需求演進。
