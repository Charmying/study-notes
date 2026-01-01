# CCCrypt GCM

CCCrypt GCM 是 CCCrypt 庫中支援的一種加密模式，即 Galois/Counter Mode (GCM)。

CCCrypt 是 Apple 在操作系統 (macOS、iOS 等) 中提供的一個加密服務接口 (Crypto API)，主要用於數據加密和解密。

CCCrypt 屬於 Common Crypto 庫的一部分，提供了對稱密鑰加密、雜湊算法 (例如：SHA-1、SHA-2)、訊息認證碼 (HMAC) 等多種加密功能。

GCM 是一種被廣泛使用的加密模式，因高效且同時提供加密與驗證的特性，常用在於網路通訊及資料保護。

<br />

## CCCrypt 的用途

- 資料加密和解密：使用對稱密鑰加密算法 (例如：AES、DES 等) 來保護敏感資料。

- 資料完整性檢查：通過 HMAC 等算法檢查資料在傳輸或存儲過程中的完整性。

- 雜湊運算：使用 SHA-1 或 SHA-2 生成資料的雜湊值，用於資料完整性驗證或密碼存儲。

<br />

## CCCrypt 的基本步驟

1. 設定加密參數

    - 算法 (Algorithm)：選擇加密算法，例如：kCCAlgorithmAES128。

    - 操作模式 (Operation)：選擇加密或解密操作，例如：kCCEncrypt 或 kCCDecrypt。

    - 填充方式 (Padding)：選擇填充方式，例如：kCCOptionPKCS7Padding。

    - 密鑰 (Key)：提供加密或解密的密鑰。

    - 初始向量 (IV)：提供初始向量 (視加密模式而定，例如：CBC 模式)。

2. 呼叫 CCCrypt 函數

    使用 CCCrypt 函數進行加密或解密操作。函數原型如下

    ```c
    CCCryptorStatus CCCrypt(
        CCOperation op,          // kCCEncrypt or kCCDecrypt
        CCAlgorithm alg,         // 加密算法
        CCOptions options,       // 填充選項
        const void *key,         // 密鑰資料
        size_t keyLength,        // 密鑰長度
        const void *iv,          // 初始向量
        const void *dataIn,      // 輸入資料
        size_t dataInLength,     // 輸入資料長度
        void *dataOut,           // 輸出資料緩衝區
        size_t dataOutAvailable, // 輸出緩衝區的可用大小
        size_t *dataOutMoved     // 實際寫入輸出緩衝區的資料量
    );
    ```

3. 處理加密結果

    - 檢查返回狀態：CCCrypt 函數會返回一個狀態碼，表示操作是否成功。

    - 讀取輸出資料：若操作成功，從 `dataOut` 緩衝區讀取加密或解密後的資料。

<br />

## CCCrypt 的範例

以下是使用 CCCrypt 進行 AES-128 CBC 模式加密的簡單範例

```objc
#import <CommonCrypto/CommonCryptor.h>

- (NSData *)encryptData:(NSData *)data withKey:(NSData *)key andIV:(NSData *)iv {
    size_t outLength;
    NSMutableData *cipherData = [NSMutableData dataWithLength:data.length + kCCBlockSizeAES128];

    CCCryptorStatus result = CCCrypt(
        kCCEncrypt,              // Operation
        kCCAlgorithmAES128,      // Algorithm
        kCCOptionPKCS7Padding,   // Options
        key.bytes,               // Key pointer
        key.length,              // Key length
        iv.bytes,                // IV pointer
        data.bytes,              // Input data pointer
        data.length,             // Input data length
        cipherData.mutableBytes, // Output buffer pointer
        cipherData.length,       // Output buffer length
        &outLength               // Output length pointer
    );

    if (result == kCCSuccess) {
        cipherData.length = outLength;
        return cipherData;
    } else {
        return nil;
    }
}
```

### 注意事項

- 密鑰管理：確保加密密鑰的安全存儲和管理，避免密鑰洩露。

- 初始向量 (IV)：使用隨機生成的 IV，可以增加加密的安全性。

- 錯誤處理：適當處理 CCCrypt 函數的返回狀態，確保加密操作的可靠性。

<br />

## GCM 加密模式

Galois/Counter Mode (GCM) 是一種能夠提供數據保密性和完整性的加密模式。GCM 是基於計數器模式 (Counter Mode，簡稱：CTR) 的變體，但還包含了使用 Galois 鍵盤驗證 (Galois Message Authentication Code，簡稱：GMAC) 的數據完整性驗證功能。也就是說，說在加密的同時，GCM 還能生成一個消息驗證碼 (MAC) 來確保數據未被篡改。

<br />

## 使用範例

在使用 CCCrypt 實現 GCM 加密時，一般需要設定密鑰、初始向量 (Initialization Vector，簡稱：IV)、和加密數據。

```swift
import CommonCrypto

/** 設定密鑰、初始向量、和數據 */
let key = "密鑰".data(using: .utf8)!
let iv = "初始向量".data(using: .utf8)!
let plaintext = "需要加密的數據".data(using: .utf8)!

/** 定義加密後的緩衝區 */
var ciphertext = Data(count: plaintext.count + kCCBlockSizeAES128)

/** 執行加密操作 */
var numBytesEncrypted: size_t = 0
let cryptStatus = CCCrypt(
    CCCryptorOperation(kCCEncrypt),
    CCAlgorithm(kCCAlgorithmAES128),
    CCOptions(kCCOptionPKCS7Padding | kCCModeGCM),
    key.bytes, key.count,
    iv.bytes,
    plaintext.bytes, plaintext.count,
    &ciphertext, ciphertext.count,
    &numBytesEncrypted
)

if cryptStatus == kCCSuccess {
    ciphertext.removeSubrange(numBytesEncrypted..<ciphertext.count)
    print("加密成功: \(ciphertext.base64EncodedString())")
} else {
    print("加密失敗")
}
```

<br />

## CCCrypt GCM 的應用範圍

CCCrypt GCM 常用於需要高效加密和強完整性驗證的場景。

- 網路通訊：HTTPS、VPN 等需要確保通訊過程中數據的安全和完整。

- 資料保護：保護存儲在設備上的敏感數據，例如：文件加密和資料庫加密。

<br />

## CCCrypt GCM 的優缺點

### 優點

- 高效能：GCM 利用了並行計算技術，特別適合多核心處理器，能夠在硬體加速下達到很高的加密速度，而且許多現代處理器和加密設備支援對 GCM 模式的硬體加速。

- 保密性和完整性：GCM 同時提供加密和消息驗證碼，確保數據的保密性和完整性。就算數據在傳輸過程中若被篡改，解密時會檢測到並報錯。而且 GCM 使用 Galois 鍵盤進行數據認證，提供了強大的數據完整性保護。

- 非操作依賴性：GCM 模式的操作過程不依賴於前面的操作結果，這特別適合並行處理。

- 附加認證數據 (AAD)：GCM 支援附加認證數據，允許加密過程中加入未加密但需要認證的數據。

- 高度支援：GCM 是 NIST 批准的加密模式，並且在許多標準和協議中被廣泛使用。例如：TLS、IPsec 和 IEEE 802.1AE (MACsec)。

### 缺點

- 實現難度：相比較其他加密模式，GCM 的實現較為複雜，需要精確的計算和處理，特別是在消息認證部分。

- 效能瓶頸：雖然 GCM 支援並行計算，但在某些應用中仍需要序列處理。而且 GCM 對初始向量 (IV) 非常敏感，必須確保每次加密使用唯一的 IV，否則會嚴重影響安全性。

- 安全性風險：若重複使用 IV 就會嚴重削弱加密強度，所以在實際應用中需要特別注意 IV 的管理。而且除了 IV 管理，消息認證碼的安全性依賴於密鑰的管理和使用，若密鑰管理不當，也會影響整體的安全性。

- 硬體依賴：雖然 GCM 可以通過硬體加速提高效能，但在某些硬體不支援的環境，性能可能不如預期，需要依賴於軟體實現。

<br />

## 總結

CCCrypt GCM 是一種結合高效能和強保護性的加密模式，適用於各種需要高安全性和高效能的應用場景。
