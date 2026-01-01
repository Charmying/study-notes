# 公鑰與私鑰

在現代密碼學中，公鑰和私鑰是用來加密和解密訊息的一組密鑰。這種加密被稱為非對稱加密，因為是使用一對不同的密鑰進行加密和解密，若是使用相同的密鑰進行加密則稱為對稱加密。

<br />

## 公鑰 (Public Key)

- 公鑰是公開的，可以與任何人共享。

- 用於加密訊息或者驗證數字簽名。

- 當想要安全傳送訊息時，會使用對方的公鑰來加密訊息。

<br />

## 私鑰 (Private Key)

- 私鑰是保密的，只有擁有者自己知道。

- 用於解密用公鑰加密的訊息或者生成數字簽名。

- 當收到一個加密的訊息時，使用自己的私鑰來解密這個訊息。

<br />

## 公鑰與私鑰的應用範圍

- SSL/TLS：SSL/TLS 協議使用公鑰和私鑰來保護網站和使用者之間的通訊，確保數據在傳輸過程中不被竊聽或篡改。

- 加密郵件：PGP (Pretty Good Privacy) 是一種常見的郵件加密技術，使用公鑰和私鑰來加密和解密電子郵件，確保郵件內容的隱私性和完整性。

- 加密貨幣：比特幣等加密貨幣使用公鑰和私鑰來管理使用者的錢包地址和交易，確保資產安全性。

### 這種技術廣泛應用於網路安全、數據傳輸和金融交易等各個領域。

<br />

## 公鑰與私鑰的創建過程

創建公鑰和私鑰的過程涉及使用的密碼學算法，最常見的包括 RSA (Rivest-Shamir-Adleman)、DSA (Digital Signature Algorithm) 和 ECC (Elliptic Curve Cryptography) 等。

1. 選擇算法：選擇適合需求的密碼學算法。常見的選擇有 RSA、DSA 和 ECC 等。

2. 生成密鑰對：使用選定的算法生成一對密鑰，即公鑰和私鑰。

3. 保存密鑰：將生成的密鑰對保存到安全的位置，公鑰可以公開，而私鑰則要妥善保管，不可泄露。

<br />

## 使用 OpenSSL 創建公鑰和私鑰 (以 RSA 為例)

OpenSSL 是一個常用的開源工具，可以用來生成公鑰和私鑰。

1. 安裝 OpenSSL：在大多數 Linux 發行版上，可以通過管理器安裝，例如：`apt-get install openssl` (Debian/Ubuntu) 或 `yum install openssl` (CentOS)。

2. 生成私鑰：使用以下命令生成一個 2048 位的 RSA 私鑰 (會在當前目錄下生成一個名為 `private_key.pem` 的私鑰文件)

```text
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
```

3. 生成公鑰：使用私鑰生成對應的公鑰 (會在當前目錄下生成一個名為 `public_key.pem` 的公鑰文件)

```text
openssl rsa -pubout -in private_key.pem -out public_key.pem
```

<br />

## 使用 Python 和 cryptography 庫生成公鑰和私鑰 (以 RSA 為例)

1. 使用 pip 安裝 cryptography 庫

```text
pip install cryptography
```

2. 生成密鑰對

```python
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# 生成私鑰
private_key = rsa.generate_private_key(
	public_exponent=65537,
	key_size=2048
)

# 將私鑰保存到文件
with open("private_key.pem", "wb") as f:
    f.write(
		private_key.private_bytes(
		encoding = serialization.Encoding.PEM,
		format = serialization.PrivateFormat.TraditionalOpenSSL,
		encryption_algorithm = serialization.NoEncryption()
    )
 )

# 生成公鑰
public_key = private_key.public_key()

# 將公鑰保存到文件
with open("public_key.pem", "wb") as f:
    f.write(
		public_key.public_bytes(
		encoding = serialization.Encoding.PEM,
		format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
)
```

以上使用了 RSA 演算法來生成公鑰和私鑰。其他演算法 (例如：DSA 和 ECC) 也有類似的步驟。
