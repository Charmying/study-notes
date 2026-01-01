# 序列化 (Serialization)

序列化是一個在 Computer Science 中非常重要的技術，尤其是在分佈式系統和應用程式的開發。序列化的基本概念是指將資料結構或物件狀態轉換成可取用格式，例如：存成檔案、存於緩衝或經由網路中傳送，使資料可以在不同的環境中被重現。

數據的最小單位是位元，而 1 個位元組 (1 Byte) 即 8 個 Bit (位元)，就像 01010011。在 ASCII 編碼裡「A」這個字母為 65 → 01000001 (二進位)。資料傳送時，傳輸的文字都是 01000001 這種位元 (序列化)，而電腦轉換回對應的文字則稱反序列化 (也稱為解編組，Deserialization、Unmarshalling)。

<img src="https://github.com/user-attachments/assets/aac9058d-ee80-46db-832c-f7c1c16d9dba" width="100%" />

物件會序列化成資料流，且其中不只包含資料，還有物件型別 (版本、文化特性及元件名稱) 的資訊。而該資料流可以儲存在資料庫、檔案或記憶體中。

<br />

## 序列化的用途

- 持久化儲存

    當應用程式需要保存資料狀態以便下次能夠重新載入，序列化是非常重要的技術。例如：當用戶在使用某個應用程式時，可以將用戶設定或狀態序列化到磁碟檔案中，當用戶再開啟時，可以反序列化這些數據來恢復到之前的狀態。

    考慮一個需要儲存設定的程式

    ```python
    import json

    # 用戶設置
    settings = {
    	"theme": "dark",
    	"font_size": 12,
    	"language": "zh-TW"
    }

    # 序列化並保存到 file
    with open("settings.json", "w") as file:
        json.dump(settings, file)

    # 從 file 讀取並反序列化
    with open("settings.json", "r") as file:
        loaded_settings = json.load(file)

    print(loaded_settings)
    ```

- 跨網路傳輸

    序列化使物件可以被轉換為文本或二進制格式，從而能通過網路傳輸。這在分佈式系統中特別重要，因為不同系統之間需要交換資料。通常使用 JSON、XML 或二進制格式傳輸。

    假設有一個簡單的 RESTful API Server，需要將數據返回給 Client 端

    ```javascript
    const user = {
      name: "Charmy",
      email: "charmy@example.com",
      age: 28
    };

    /** 將物件序列化為 JSON */
    const jsonString = JSON.stringify(user);
    console.log("Sending JSON:", jsonString);

    // 通過 HTTP 發送給 Client 端
    ```

- 遠端方法調用 (RPC)

    在分佈式系統中，遠端方法調用 (Remote Procedure Call，簡稱：RPC) 允許一個程式調用位於不同地址空間中的函數或方法。通常需要將方法的參數序列化，以便通過網路傳輸。

    假設使用 gRPC 進行遠端方法調用

    ```proto
    // proto (protobuf)

    syntax = "proto3";

    service UserService {
      rpc GetUser (UserRequest) returns (UserResponse);
    }

    message UserRequest {
      int32 user_id = 1;
    }

    message UserResponse {
      string name = 1;
      string email = 2;
    }
    ```

    以上例子中，`UserRequest` 和 `UserResponse` 需要序列化以便在 Client 端和 Server 之間傳輸。

- 暫存與緩存

    序列化可以用於將資料暫存到緩存系統中 (例如：Redis、Memcached) 來提高應用程式性能。這樣可以避免每次都從資料庫讀取資料。

    使用 Python 和 Redis 將物件序列化後緩存

    ```python
    import redis
    import json

    # 連接到 Redis
    r = redis.Redis(host='localhost', port=6379, db=0)

    # 用戶資料
    user = {"name": "Charmy", "email": "charmy@example.com"}

    # 將資料序列化並存入 Redis
    r.set('user:1001', json.dumps(user))

    # 從 Redis 獲取資料並反序列化
    cached_user = json.loads(r.get('user:1001'))

    print(cached_user)
    ```

<br />

## 序列化的常見格式

- JSON (JavaScript Object Notation)

    JSON 是一種輕量級的資料交換格式，易於讀寫且易於機器解析和生成，是網路傳輸中常用的格式之一，特別是在 Web 開發中。

    - 優點

        - 可讀性好： JSON 是文本格式，人類可讀。

        - 廣泛支持： 幾乎所有的程式語言和平台都支持。

    - 缺點

        - 效率較低： 由於 JSON 是文本格式，處理大型數據時效率不如二進制格式。

        - 數據類型有限： JSON 不支持某些資料類型，例如：二進制資料。

    - 範例

    ```json
    {
      "name": "Charmy",
      "age": 28,
      "email": "charmy@example.com"
    }
    ```

- XML (eXtensible Markup Language)

    XML 是一種可擴展的標記語言，具有良好的結構性和可擴展性，常用於需要數據驗證的應用程式中。

    - 優點

        - 可擴展性： 可以定義自己的標記和屬性。

        - 結構性好： 支持複雜的資料結構和層次。

    - 缺點

        - 冗長： XML 的標記使得文件通常較大。

        - 解析性能： XML 的解析和生成性能不如 JSON 和二進制格式。

    - 範例

    ```xml
    <user>
      <name>Charmy</name>
      <age>28</age>
      <email>charmy@example.com</email>
    </user>
    ```

- 二進制格式

    二進制格式通常比文本格式更高效，適合性能要求高的應用程式。常見的二進制序列化格式包括 Protocol Buffers、Avro 和 MessagePack。

    - 優點

        - 效率高： 二進制格式通常比文本格式更小，序列化/反序列化性能更高。

        - 支持多種數據類型： 可以支持多種複雜的數據類型。

    - 缺點

        - 可讀性差： 二進制格式對人類不可讀。

        - 不夠靈活： 與文本格式相比，修改結構更困難。

    - 範例 (以 Protocol Buffers 為例)

    ```proto
    message User {
      string name = 1;
      int32 age = 2;
      string email = 3;
    }
    ```

    這種格式在傳輸時會被編碼成緊湊的二進制形式。

<br />

## 序列化的優缺點

### 優點

- 資料持久化

    序列化允許將物件的狀態保存到文件或資料庫中，以便在之後可以重新載入和使用。這對於需要保存應用程式狀態或用戶設置的系統特別重要。

    - 優點：能夠保存應用狀態，例如：遊戲進度、用戶設定等。

    - 例如：電商應用中，購物車狀態可以序列化並保存在 Server 中。

- 資料傳輸

    序列化使物件可以在不同的系統或網路節點之間傳輸，在分佈式系統和網路通訊中至關重要。

    - 優點：支持跨平台和跨語言的數據交換。

    - 例如：在 RESTful API 中，Server 可以將資料序列化為 JSON 回應 Client 端請求。

- 遠端方法調用 (RPC)

    序列化允許遠端方法調用的參數和返回值在不同的機器之間傳輸。

    - 優點：支持分佈式計算，使得系統可以進行遠端操作。

    - 例如：gRPC 使用 Protocol Buffers 序列化數據以實現高效的遠程方法調用。

- 暫存與緩存

    序列化可以用於將數據暫存到緩存系統中，提高應用程序的性能和響應速度。

    - 優點：減少數據庫的讀取負擔，提高系統性能。

    - 例如：將計算結果序列化並儲存在 Redis 緩存中，以便重複使用。

- 數據交換格式的標準化

    使用標準化的序列化格式 (例如：JSON、XML) 可以使得不同系統間的數據交換更加一致和規範。

    - 優點：支持多種語言和平台，方便集成。

    - 例如：在微服務架構中，各個服務之間可以使用 JSON 作為標準交換格式。

### 缺點

- 效率問題

    序列化和反序列化的過程可能會導致性能瓶頸，特別是當資料量較大時。

    - 缺點：序列化過程可能耗時，特別是對於大型數據結構。

    - 例如：大量的資料序列化後可能導致網路延遲和響應變慢。

- 兼容性問題

    隨著系統的演化，序列化格式和資料結構可能會發生變化，導致兼容性問題。

    - 缺點：不同版本之間的數據可能不兼容，需要額外的處理。

    - 例如：更新的應用程式版本可能無法解析舊版本序列化的數據。

- 安全性問題

    反序列化不受信任的數據可能會導致安全漏洞，例如：程式碼注入或遠程程式碼執行。

    - 缺點：需要小心處理反序列化操作，避免安全風險。

    - 例如：Java 中的反序列化漏洞曾被利用來進行攻擊。

- 可讀性和調試困難

    某些序列化格式 (特別是二進制格式) 對人來說不可讀，使得調試和錯誤排查更困難。

    - 缺點：二進制格式難以查看和修改，降低了可調試性。

    - 例如：開發人員在排查二進制數據格式錯誤時需要工具。

- 數據冗長

    某些序列化格式 (例如：XML) 會導致資料變得冗長，特別是資料結構複雜時。

    - 缺點：增加了網路傳輸的開銷和儲存空間。

    - 例如：XML 文件可能比 JSON 或二進制佔用更多儲存空間。

<br />

## 參考資料

- [序列化](https://zh.wikipedia.org/zh-tw/%E5%BA%8F%E5%88%97%E5%8C%96)

- [Java Serializable的序列化與反序列化](https://medium.com/appxtech/java-serializable%E7%9A%84%E5%BA%8F%E5%88%97%E5%8C%96%E8%88%87%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96-cc30126c5afd)

- [Java反序列化漏洞及其检测](https://www.huaweicloud.com/zhishi/vss-002.html)
