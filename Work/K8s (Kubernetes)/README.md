# K8s (Kubernetes)

K8s 是 Kubernetes 的縮寫 (因為 "Kubernetes" 中有 8 個字母在 K 和 s 之間)，是一個開源的容器資源調度平台，由 Google 開發並於 2014 年開源，主要目的是自動化應用程式的部署、擴展和管理，特別是在容器化應用程式的環境中。

K8s 的構想理念是 Automated container deployment, scaling, and management，就是透過自動化功能提升應用程式的可靠性和減輕維運負擔，讓開發人員專注於軟體開發任務。

在傳統的軟體部署模式中，開發人員需要確保應用程式在不同的環境中 (例如：開發、測試、和生產環境) 能夠一致運行。而 Docker 作為最受歡迎的容器化技術，使應用程式和其依賴的環境能夠打包在一起來保證一致性，K8s 則進一步提供工具來管理和協調這些容器的運行。

K8s 的微服務管理 Cluster，能夠達成 Docker Compose 的所有功能，例如：啟動容器，管理網路以及容器間的通訊。除此之外，還能將多個 Container 分派到多台主機上，並監控每個 Container 的運行狀態。

若 K8s 偵測到某個 Container 或 Pod 故障會啟動 Replica Set 來確保服務持續運行。除了能夠監控節點狀態，K8s 的自動擴展功能 (Auto Scaling) 可以幫助開發團隊自動調整 K8s 的節點數量來配合開發和營運時所需的資源用量。

在部署方面，K8s 的容器自動部署 (Automated deployment) 功能讓使用者能透過一個描述狀態的文件 (通常是 YAML 格式) 指定服務所需的容器和設定，讓 K8s 根據這份文件建立所需的資源或配置。

<br />

## K8s 能夠解決什麼問題

K8s 可以協助交付和管理容器化、傳統和雲端原生應用，以及重構為微服務的應用程式。 

- 加快開發速度：K8s 可以協助建構以微服務為基礎的雲端原生應用程式，此外也支援現有應用程式的容器化，因此能做為翻新應用程式的基礎，讓加速開發應用程式。

- 在任何環境中部署應用程式：K8s 可在任何環境中使用，無論是採用現場部署、公有雲，還是混合式部署，都能執行應用程式。也就是說，K8s 可以在任何需要的地方執行應用程式。

- 執行高效率服務：K8s 可以自動調整執行服務所需的 Cluster 大小，可以根據需求自動調度應用程式資源，更有效率的方式執行應用程式。

在還沒有 K8s 前，想透過 Docker 快速啟動由容器組成的微服務，可以在單一伺服器上使用 Docker Compose。開發人員只需寫 YAML 文件，將參數設定好後直接執行設定檔，就能啟動或終止一組相依的服務。

雖然有效降低測試和部署的難度，但 Docker Compose 的運行範圍受限於單一主機。而在面對需要跨越多台主機協同工作的大規模服務時，K8s 的容器自動化部署、擴展功能就成為大規模管理容器通訊的解決方案。

<br />

## K8s 的基礎知識

容器是與其相依性封裝在一起的單一應用程式或微型服務，可以做為獨立環境和一個環境中的應用程式執行。現代應用程式採用分散式微型服務架構，每個應用程式都包含非常多獨立執行的離散型軟體元件。每個元件 (或微型服務) 都執行單一獨立函數，增強程式碼模組化。透過為每項服務建立獨立的容器，可以在多台電腦上部署和分散應用程式。而透過擴展或縮減個別微型服務工作負載和運算功能，可以將應用程式效率最大化。

K8s 是開放原始碼容器協同運作軟體，可以大規模簡化容器管理，像是排程、執行、啟動和關閉容器，以及自動化管理功能。開發人員可以大規模獲得容器化的好處，不需要管理費用。

<br />

## K8s 的核心概念

- Pod

    Pod 是 K8s 底下的標準可部署單位，通常用來執行一個應用程式的某個部分或一個完整的應用程式。Pod 包含一或多個容器，而且在 Pod 內容器共用相同的系統資源，例如：儲存空間和網路。每個 Pod 都會獲得一個唯一的 IP 地址。 

    Pod 內的容器不會被隔離。將 Pod 視為類似於虛擬機器 (VM)，具有類似於在 VM 上執行之應用程式的容器。Pod 和 Pod 群組可以透過將屬性標籤附加到其中來整理，例如：環境類型的標籤 'dev' 或 'prod'。

- 節點與 Cluster

    K8s 的基本運行單元是 Cluster，每個 Cluster 由多個節點組成。

    節點是執行 Pod 的機器，可以是實體或虛擬伺服器，例如：Amazon EC2 執行個體。節點上的元件包括

    - 主節點 (Master Node)：負責管理整個，包括調度、監控和管理。

    - 工作節點 (Worker Node)：執行實際的應用程式負載，運行容器。

        - Kubelet：適用於節點和容器的管理。

        - Kube-proxy：適用於網路的 Proxy。

        - Container Runtime：必須在節點上安裝相容的 Container Runtime 才能執行容器。K8s 支援多個 Container Runtime ，例如：K8s Container Runtime 界面和容器。

- 控制器

    控制器負責管理 K8s 中的不同資源類型。

    - ReplicaSet：確保指定數量的 Pod 副本在 Cluster 中運行。

    - Deployment：管理應用程式的生命週期，支持滾動更新和 Rolling Back。

    - StatefulSet：用來管理需要有狀態的應用程式。

    - DaemonSet：確保所有 (或指定) 節點上運行一個 Pod 副本。

- 複本集與部署

    Pod 是一個獨立成品，當其節點停機時不會自動重新啟動。若 Pod 被分組到複本集，則在 K8s 中可以指定始終跨節點執行的複本集，對於擴展和縮減以及確保應用程式和服務的持續性非常重要。 

    部署是 K8s 管理物件，用於部署應用程式，以及在不離線的情況下更新或回復應用程式。

- 服務和輸入

    使用 K8s 服務，透過端點公開網路上的 Pod 或 Pod 群組，取得遵循標準網路通訊規則的互動性。對於公有網際網路流量存取，K8s 輸入將會附加到服務，然後連結到一個或多個 Pod。

<br />

## K8s 的流程

<img src="https://github.com/user-attachments/assets/2eb62739-c949-47ef-b810-d90e85837664" width="100%" />

### K8s 兩大基本元件

- Master Node (Control Plane)

    Control plane 又叫控制平台，是 K8s 的運作的指揮中心，負責下達指揮命令。例如：容器排程 (Scheduling Containers)、服務管理 (Managing Services) 和回應 API 請求 (Serving API Requests)。

    Control Plane 會透過專用 API 與各個 Node 進行通訊，也會監控所有 Node 的工作負載，並下發指令來應對突發狀況。例如：若 Control Plane 偵測到應用程式的使用量暴增，就會調度相應的運算資源來應對，並在使用量下降時，自動縮減運算資源。

    <img src="https://github.com/user-attachments/assets/e4177e45-2f71-4784-8429-334280478556" width="100%" />

    Control plane 由 4 個重要元件組成：

    - Kube-API Server： 是所有請求的唯一入口，也是 Cluster 中各個 Node 的溝通橋樑，

    負責身份驗證 (Authentication)、授權 (Authorization)、存取控制 (Access Control) 和 API 註冊 (Registration)。

    - etcd：是用來存放 K8s Cluster 備份資訊的資料庫，紀錄整個 K8s 的狀態。 當 Controller Plane 發生故障，etcd 可以還原 K8s 的狀態。

    - Kube-scheduler：是 K8s 的工作調度器，負責監控所有使用者開啓 Pod 的指令，並根據 Worker Node 的資源規定和硬體限制找出最合適的 Worker Node。

    - kube-controller-manager：是 K8s Cluster 的自動化控制中心，負責管理並運行 K8s Controller 的元件。

- Worker Node

    Worker Node 是 K8s 中的工作主機，負責管理和運行 Pod，可以是實體機或虛擬機 (例如：AWS 上的 EC2)。每個 Node 都包含運行 Pod 所需的服務，並由 Master Node 管理。

    <img src="https://github.com/user-attachments/assets/8f23b464-523f-4785-8b05-a0d2a4ba4e08" width="100%" />

    Worker Node 上的服務包括

    - Pod

       Pod 是 K8s 中最小的資源部署單位，設計目的是簡化容器化應用程式的部署和管理。

        一個 Pod 封裝了一個或多個 Container，這些容器共同執行相同的工作任務，也共享相同的網路資源 (例如：IP 地址、記憶體和主機名)。這種架構讓容器間能高效共享和交換資料，同時也保證了容器間通訊的簡便性和安全性。

        雖然使用者能將應用程式上的所有容器封裝至同一個 Pod，但最佳做法是讓每個 Pod 對應一個 Container，接著再把這些 Pod 裝入 Namespace，這樣就能組成一個完整的應用程式。

    - Kubelet

        Kubelet 是 Worker Node 與 Kube-API Server 進行溝通的元件，主要負責接收 API server 發送的新或修改後的 Pod 規格，確保 Pod 及 Pod 內的容器在 API Server 的期望下運行。

        Kubelet 也會定時從 Worker Node 上收集 Pod/Container 上的狀態 (例如：運行什麼 Container、副本運行數量、資源配置)，並將這些資訊匯報給 Control Plane。若 Controller 沒有收到節點的運行資訊，該 Node 就會被斷定為 Unhealthy。

    - Kube-proxy

        Kube-Proxy 是每個 Node 上運行的網路代理服務，負責管理 Pod 間的網路通訊規則、 Cluster 內部的通訊與回應 Cluster 外部的 request 。若作業系統中存在封包過濾器 (packet filtering layer)，Kube-proxy 會將處理 request 的請求轉由 Worker Node 的作業系統處理。

    - Container Runtime

        Container Runtime 屬於較為底層的元件，負責實際運行容器，並聽從 Kubelet 的命令管理容器。K8s 支援多種不同的 Container Runtime，例如：containerd、runC、CRI-O 等。

<br />

## K8s 的核心功能

- 動態擴展 (Dynamic Scaling)

    在實際應用中，DevOps 人員經常面臨資源不足的問題，這是因為每個應用在每個時間點的流量都不是固定的，但每個應用分配到的資源卻是固定的。 K8s 透過 Dynamic Scaling 可以動態增加或減少運算資源，其中常見的方式有 Horizontal Scaling 和 Vertical Scaling。

    - 水平擴展 (Horizontal Scaling)：根據負載自動調整 Pod 的數量。

        水平擴展的核心概念是根據「工作負載的變化來更新 Pod 的數量」。也就是說，說當負載增加時，可以自動部署更多的 Pod，以確保服務的性能。而負載減少時，也能減少 Pod 的數量，確保資源不被浪費。

        具體來說， K8s 會透過 Horizontal Pod Autoscaler (簡稱：HPA，一種用於自動調整應用程式中 Pod 副本數的控制器) 自動更新工作負載資源 (例如：Deployment 或 StatefulSet)，並由這兩種資源負責更新 Pod 數量，使 Pod 在資源節約和服務性能之間達到平衡。

        <img src="https://github.com/user-attachments/assets/ac44052b-24f3-4020-9be3-dd4d4b2d071b" width="100%" />

        水平擴展運作流程：使用 HPA 架構的 K8s 首先會透過 Metric Server 檢測各項指標，若監測到 CPU/Mermory 的利用率高於目標，HPA 會增加 Pod 的數量，直到平均使用率降低到目標範圍內。

    - 垂直擴展 (Vertical Scaling)：調整單個容器的資源使用 (例如：CPU 和記憶體)。

        和水平擴展不同，垂直擴展的核心概念是根據工作負載的變化來「更新 Pod 的資源請求而非 Pod 數量」。也就是說，當負載增加時可以給 Pod 更多資源，確保服務不會因為超出資源限制而降低性能。負載減少時，也能減少 Pod 的資源請求，確保資源不被浪費。

        Vertical Pod Autoscaler (簡稱：VPA，是一種垂直 Pod 資源擴縮器) 會根據容器的資源使用率自動縮放 Pod 能存取的 CPU 和 Memory 資源，讓 Pod 中的應用程式能夠取得足夠的運算資源，維持應用程式的服務品質。

        <img src="https://github.com/user-attachments/assets/acd809c6-ced9-4198-9b31-3a3a5ce07bc0" width="100%" />

        垂直擴展運作流程：首先使用 VPA 架構的 K8s 會每隔 10 秒檢查各資源的使用指標，若請求資源增加，VPA Operator 會根據資源使用量更動 Pod 的資源配置，並將 Pod 重啟，重啟後的 Pod 就會是新的資源配置。

    ### 水平擴展是關於「增減 Pod 的數量」，而垂直擴展則是關於「調整單個 Pod 的資源」。這兩種機制使能夠在 K8s 中實現有效的負載管理，確保應用程式在不同工作負載下都能保持高性能。

- 自我修復 (Self Healing)

    K8s 能夠即時修復 Cluster 中有問題的 Pod。當一個節點或 Pod 出現故障時， K8s 會自動從 Cluster 中刪除並重新創建，確保應用程式的可用性。

    <img src="https://github.com/user-attachments/assets/ab77443e-32a2-4ea2-b4b5-a6aab7f3f59f" width="100%" />

    K8s 還會確認系統狀態是否與開發人員的需求配置相符。例如：若開發人員向 K8s 提出建立 3 個副本的需求，K8s 除了建立副本之外，也會持續確認這 3 個副本的運行狀態，若發現有第 4 個副本被建立了，K8s 會將第 4 個副本刪除，以維持３個副本的設定。另外，若其中一個副本停止運行，為了維持運行３個副本，K8s 就會重新建立一個副本。

- 滾動更新 (Rolling Update)

    開發團隊能透過 K8s Cluster 中的 ReplicaSet 執行 Rolling Update，從而避免應用程式更新時造成停機。ReplicaSet 主要負責管理 Pod 的數量，確保某個 Pod 在停止運行時，能將其快速重建以確保服務的可用性。

    Rolling Update 會透過同時建立新版 Pod 的 ReplicaSet 以及逐步關閉舊版 Pod 來進行更新。開發人員無須擔心在更新過程中將所有 Pod 同時關閉，進而導致服務中斷。

- 回復舊版 (Rolling Back)

    Rolling Update 會透過建立新版 Pod 的 ReplicaSet 來更新，而 Rolling Back 則是透過舊版的 ReplicaSet 來恢復舊版 Pod。

    通常若沒有設定參數，一個 Deployment 中會保留最多十版的 ReplicaSet 。開發人員若在服務運行時發現錯誤，就可透過 Rolling Back 功能找到想要恢復的舊版本 ReplicaSet 進行無痛 Rollback。

- 服務發現與負載均衡 (Service Discovery and Load Balancing)

    K8s 內建服務發現和負載均衡功能。當服務中有多個副本時，K8s 會自動分配流量到健康的容器上，確保服務的高可用性和穩定性。

    - 服務 (Service)：抽象出應用的一組運行容器，提供統一的存取入口。

    - Ingress：管理外部訪問到服務的 HTTP 和 HTTPS 路由。

- 儲存編排 (Storage Orchestration)

    K8s 支持不同類型的儲存系統，並能自動掛載所需的儲存資源到容器中，使應用程式能夠方便使用儲存空間。

    - 持久化卷 (Persistent Volume，簡稱：PV)：獨立於 Pod 的儲存資源。

    - 持久化卷宣告 (Persistent Volume Claim，簡稱：PVC)：用戶對儲存資源的申請，K8s 根據 PVC 來提供符合要求的 PV。

- 設定管理與密鑰管理 (Configuration Management and Key Management)

    在開發中設定和密鑰的管理一直是個挑戰。K8s 提供了配置管理和密鑰管理的功能，使應用程式可以在不重新編譯的情況下進行配置更改。

    - ConfigMap：用來儲存非機密的設定數據。

    - Secrets：用來儲存和管理敏感訊息，例如：密碼、API 金鑰等。

- 擴展性 (Scalability)

    K8s 的架構設計非常靈活，允許用戶使用自定義資源來擴展功能。此外，K8s 也支持通過 plugin 來增強功能，例如：網路、監控、日誌管理等。

    - 自定義資源定義 (CRD)：用來定義新的 API 擴展 K8s 的功能。

    - Operator：利用 CRD 和控制器來自動管理應用的生命週期。

<br />

## K8s 進行應用程式開發

生產應用程式跨越多個容器，這些容器必須部署到多個伺服器主機。K8s 可以提供所需的編排和管理功能，使其可以針對這些工作負載大規模部署容器。而透過編排功能，可以建立跨多個容器的應用服務、跨叢集調度、擴展這些容器，並長期持續管理這些容器的狀況。

K8s 還需要與聯網、儲存、安全性、遙測和其他服務整合，以提供全面的容器基礎架構。

<img src="https://github.com/user-attachments/assets/1e47e9f6-5d44-4586-967f-f9e4a3f71935" width="100%" />

一旦擴展到生產環境和多個應用，會需要許多託管在相同位置的容器來協同提供各種服務。 

Linux 容器可以為基於微服務的應用提供理想的應用部署單元和獨立的執行環境。將微服務放入容器，就能更輕鬆編排各種服務 (包括儲存、網路和安全防護)。

隨著這些容器的累積，環境中容器的數量會急劇增加，複雜度也隨之增加。K8s 透過將容器分類組成容器集，解決了容器激增帶來的許多常見問題。容器集為分組容器增加了一個抽象層，可幫助調度工作負載，並為這些容器提供所需的服務，例如：連網和儲存等。 

K8s 的其他部分可協助在這些容器集之間平衡負載，同時確保運行正確數量的容器，充分支援工作負載。

<br />

## K8s 的優缺點

### 優點

- 自動化運維

    - 自動部署和 Rolling Back：K8s 支援應用程式的自動部署，並能夠在更新失敗時自動 Rolling Back 到上一版本，確保系統的穩定性。

    - 自動修復：當某個容器出現故障時，K8s 能夠自動重啟或替換，確保應用程式的持續運行。

- 高可用性和擴展性

    - 服務發現與負載均衡：K8s 內建的服務發現和負載均衡功能，可以自動將流量分配到健康的容器中，確保高可用性。

    - 自動擴展：K8s 可以根據負載自動調整應用程式的副本數量，應對流量高峰或資源不足的情況。

- 平台無關性

    K8s 支持跨多種基礎設施運行，包括公有雲、私有雲和 Local 端，讓應用程式部署更加靈活。

- 豐富的生態系統

    K8s 擁有一個龐大的社群和豐富的 plugin 生態系統，提供各種擴展功能，例如：監控、日誌管理和網絡安全等，幫助企業更好運營和管理應用程式。

-  資源高效利用

    K8s 的調度器能夠智能分配資源，根據容器的需求和節點的資源狀態來最佳化工作負載分配，提高整體資源利用效率。

- 靈活的持續交付與部署

    CI/CD 集成：K8s 可以輕鬆集成 CI/CD 工具，支持快速和頻繁的應用程式更新。

### 缺點

- 複雜性

    - 學習曲線陡峭：K8s 的概念和配置較為複雜，初學者需要花費大量時間來學習和掌握。

    - 管理成本高：維護一個運行良好的 K8s Cluster 需要專業知識和經驗，對運維團隊的技術要求較高。

- 資源消耗

    - K8s 本身需要消耗一定的資源來運行，對於小型項目或資源有限的環境可能不太合適。

- 工具鏈和整合的複雜性

    - 雖然 K8s 支援眾多工具和 plugin，但不同工具之間的整合可能需要額外的配置和調整，增加了系統複雜性。

- 網絡和儲存配置複雜

    - K8s 的網絡和儲存配置需要專門的知識，尤其在處理多租戶網絡隔離和持久化儲存方面，可能需要額外的設定和優化。

- 社群支持和資源挑戰

    - 雖然 K8s 社群活躍且資源豐富，但對於特定問題或新版本的更新，可能會出現資源不足或社群支持不足的情況。

- 版本更新頻繁

    K8s 更新頻繁，可能需要定期升級 Cluster 以獲取新功能和安全更新，但這也可能導致版本不兼容或需要大量測試。

<br />

## 總結

K8s 作為一個強大的容器編排工具，提供了許多自動化和管理功能，特別適合大規模和多環境的應用程式部署。但是其複雜性和管理成本也是需要考慮的因素。在選擇 K8s 時，應該根據自身的需求、資源和技術能力來評估其適用性。對於有經驗的技術團隊和需要高可用性和靈活部署的企業，K8s 無疑是一個強大的解決方案。

<br />

## 參考資料

- [K8s 是什麼？基本元件、核心功能、4 大優點一次看！](https://www.omniwaresoft.com.tw/product-news/k8s-introduction/)

- [什麼是 Kubernetes 叢集？](https://aws.amazon.com/tw/what-is/kubernetes-cluster/)

- [什麼是 Kubernetes？](https://cloud.google.com/learn/what-is-kubernetes?hl=zh-TW)

- [什麼是Kubernetes？](https://www.redhat.com/zh/topics/containers/what-is-kubernetes)
