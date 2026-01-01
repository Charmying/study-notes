# 介面隔離原則 (Interface Segregation Principle)

在現代軟體開發中，介面設計的品質直接影響系統的可維護性與可擴充性。

隨著專案規模增加、功能逐漸複雜，若缺乏良好的介面設計原則，類別容易被迫依賴不需要的功能，導致程式結構混亂、維護困難。

為了應對這個問題，物件導向設計提出了介面隔離原則 (Interface Segregation Principle，簡稱：ISP)。

<br />

## ISP 的核心理念

### ISP 的定義是：客戶端不應該被迫依賴不使用的介面。

也就是說，應該將大型介面拆分成多個小型、專門的介面，讓客戶端只需要依賴實際使用的介面。當某個類別實作介面時，不應該被迫實作不需要的方法。若一個介面包含太多不相關的方法，那麼實作這個介面的類別就會被迫實作所有方法，即使某些方法對該類別來說毫無意義。

簡單來說，多個專門的介面比一個通用的介面更好。

<br />

## ISP 的核心概念

- 介面分離：將大型介面拆分成多個小型、專門的介面

- 客戶端導向：根據客戶端的需求設計介面

- 最小依賴：客戶端只依賴實際需要的功能

- 高內聚：每個介面內的方法應該緊密相關

<br />

## ISP 的優缺點

### 優點

- 降低耦合度：客戶端只依賴需要的介面，減少不必要的依賴

- 提高靈活性：可以獨立修改和擴展不同的介面

- 增強可測試性：小型介面更容易進行單元測試

- 提升程式碼重用性：專門的介面更容易在不同場景中重複使用

- 符合單一職責原則：每個介面專注於特定功能

- 便於維護：介面變更時影響範圍有限

### 缺點

- 增加介面數量：可能導致專案中介面數量大幅增加

- 提高複雜度：需要管理更多的介面和實作類別

- 設計困難：需要仔細分析客戶端需求來設計合適的介面

- 學習成本：新團隊成員需要時間理解介面間的關係

- 過度設計風險：可能導致不必要的抽象

<br />

## 違反 ISP 的問題

- 強制依賴：客戶端被迫依賴不需要的功能

- 介面污染：介面包含過多不相關的方法

- 實作負擔：類別需要實作不需要的方法

- 維護困難：介面變更影響所有實作類別

<br />

## 實作範例

依 TypeScript 為例

### 違反 ISP 的範例

```typescript
/** 違反 ISP：包含過多不相關功能的大型介面 */
interface Worker {
  /** 工作相關 */
  work(): void;
  takeBreak(): void;

  /** 管理相關 */
  manage(): void;
  hire(): void;
  fire(): void;

  /** 技術相關 */
  code(): void;
  debug(): void;
  deploy(): void;

  /** 設計相關 */
  design(): void;
  prototype(): void;
}

/** 一般員工被迫實作不需要的管理方法 */
class Developer implements Worker {
  work(): void {
    console.log("Writing code");
  }

  takeBreak(): void {
    console.log("Taking a break");
  }

  code(): void {
    console.log("Coding");
  }

  debug(): void {
    console.log("Debugging");
  }

  deploy(): void {
    console.log("Deploying");
  }

  /** 被迫實作不需要的方法 */
  manage(): void {
    throw new Error("Developer cannot manage");
  }

  hire(): void {
    throw new Error("Developer cannot hire");
  }

  fire(): void {
    throw new Error("Developer cannot fire");
  }

  design(): void {
    throw new Error("Developer is not a designer");
  }

  prototype(): void {
    throw new Error("Developer cannot prototype");
  }
}
```

### 遵循 ISP 的範例

```typescript
/** 基本工作者介面 */
interface Workable {
  work(): void;
  takeBreak(): void;
}

/** 管理者介面 */
interface Manageable {
  manage(): void;
  hire(): void;
  fire(): void;
}

/** 程式設計師介面 */
interface Codeable {
  code(): void;
  debug(): void;
  deploy(): void;
}

/** 設計師介面 */
interface Designable {
  design(): void;
  prototype(): void;
}

/** 開發者只實作需要的介面 */
class Developer implements Workable, Codeable {
  work(): void {
    console.log("Writing code");
  }

  takeBreak(): void {
    console.log("Taking a break");
  }

  code(): void {
    console.log("Coding");
  }

  debug(): void {
    console.log("Debugging");
  }

  deploy(): void {
    console.log("Deploying");
  }
}

/** 設計師只實作需要的介面 */
class Designer implements Workable, Designable {
  work(): void {
    console.log("Creating designs");
  }

  takeBreak(): void {
    console.log("Taking a break");
  }

  design(): void {
    console.log("Designing UI/UX");
  }

  prototype(): void {
    console.log("Creating prototypes");
  }
}

/** 技術主管實作多個介面 */
class TechLead implements Workable, Codeable, Manageable {
  work(): void {
    console.log("Leading technical decisions");
  }

  takeBreak(): void {
    console.log("Taking a break");
  }

  code(): void {
    console.log("Code review and architecture");
  }

  debug(): void {
    console.log("Debugging complex issues");
  }

  deploy(): void {
    console.log("Overseeing deployments");
  }

  manage(): void {
    console.log("Managing team");
  }

  hire(): void {
    console.log("Interviewing candidates");
  }

  fire(): void {
    console.log("Making difficult decisions");
  }
}
```

<br />

## 其他語言範例

### Java 範例

```java
// 基本工作者介面
interface Workable {
    void work();
    void takeBreak();
}

// 程式設計師介面
interface Codeable {
    void code();
    void debug();
    void deploy();
}

// 管理者介面
interface Manageable {
    void manage();
    void hire();
    void fire();
}

// 開發者實作
public class Developer implements Workable, Codeable {
    @Override
    public void work() {
        System.out.println("Writing code");
    }

    @Override
    public void takeBreak() {
        System.out.println("Taking a break");
    }

    @Override
    public void code() {
        System.out.println("Coding");
    }

    @Override
    public void debug() {
        System.out.println("Debugging");
    }

    @Override
    public void deploy() {
        System.out.println("Deploying");
    }
}

// 技術主管實作
public class TechLead implements Workable, Codeable, Manageable {
    @Override
    public void work() {
        System.out.println("Leading technical decisions");
    }

    @Override
    public void takeBreak() {
        System.out.println("Taking a break");
    }

    @Override
    public void code() {
        System.out.println("Code review and architecture");
    }

    @Override
    public void debug() {
        System.out.println("Debugging complex issues");
    }

    @Override
    public void deploy() {
        System.out.println("Overseeing deployments");
    }

    @Override
    public void manage() {
        System.out.println("Managing team");
    }

    @Override
    public void hire() {
        System.out.println("Interviewing candidates");
    }

    @Override
    public void fire() {
        System.out.println("Making difficult decisions");
    }
}
```

### Python 範例

```python
from abc import ABC, abstractmethod

class Workable(ABC):
    @abstractmethod
    def work(self) -> None:
        pass

    @abstractmethod
    def take_break(self) -> None:
        pass

class Codeable(ABC):
    @abstractmethod
    def code(self) -> None:
        pass

    @abstractmethod
    def debug(self) -> None:
        pass

    @abstractmethod
    def deploy(self) -> None:
        pass

class Manageable(ABC):
    @abstractmethod
    def manage(self) -> None:
        pass

    @abstractmethod
    def hire(self) -> None:
        pass

    @abstractmethod
    def fire(self) -> None:
        pass

class Developer(Workable, Codeable):
    def work(self) -> None:
        print("Writing code")

    def take_break(self) -> None:
        print("Taking a break")

    def code(self) -> None:
        print("Coding")

    def debug(self) -> None:
        print("Debugging")

    def deploy(self) -> None:
        print("Deploying")

class TechLead(Workable, Codeable, Manageable):
    def work(self) -> None:
        print("Leading technical decisions")

    def take_break(self) -> None:
        print("Taking a break")

    def code(self) -> None:
        print("Code review and architecture")

    def debug(self) -> None:
        print("Debugging complex issues")

    def deploy(self) -> None:
        print("Overseeing deployments")

    def manage(self) -> None:
        print("Managing team")

    def hire(self) -> None:
        print("Interviewing candidates")

    def fire(self) -> None:
        print("Making difficult decisions")
```

<br />

## 實際應用場景

### 檔案處理系統

```typescript
/** 違反 ISP */
interface FileProcessor {
  read(): string;
  write(content: string): void;
  compress(): void;
  encrypt(): void;
  backup(): void;
  validate(): boolean;
}

/** 遵循 ISP */
interface Readable {
  read(): string;
}

interface Writable {
  write(content: string): void;
}

interface Compressible {
  compress(): void;
}

interface Encryptable {
  encrypt(): void;
}

interface Backupable {
  backup(): void;
}

interface Validatable {
  validate(): boolean;
}

/** 簡單文字檔案只需要讀寫功能 */
class TextFile implements Readable, Writable {
  read(): string {
    return "text content";
  }

  write(content: string): void {
    console.log(`Writing: ${content}`);
  }
}

/** 安全檔案需要加密和備份功能 */
class SecureFile implements Readable, Writable, Encryptable, Backupable {
  read(): string {
    return "encrypted content";
  }

  write(content: string): void {
    console.log(`Writing encrypted: ${content}`);
  }

  encrypt(): void {
    console.log("Encrypting file");
  }

  backup(): void {
    console.log("Creating backup");
  }
}
```

### 媒體播放器系統

```typescript
/** 遵循 ISP 的媒體播放器 */
interface Playable {
  play(): void;
  pause(): void;
  stop(): void;
}

interface VolumeControllable {
  setVolume(level: number): void;
  mute(): void;
  unmute(): void;
}

interface Seekable {
  seek(position: number): void;
  getCurrentPosition(): number;
  getDuration(): number;
}

interface Recordable {
  startRecording(): void;
  stopRecording(): void;
  saveRecording(filename: string): void;
}

/** 簡單音樂播放器 */
class MusicPlayer implements Playable, VolumeControllable, Seekable {
  play(): void {
    console.log("Playing music");
  }

  pause(): void {
    console.log("Pausing music");
  }

  stop(): void {
    console.log("Stopping music");
  }

  setVolume(level: number): void {
    console.log(`Setting volume to ${level}`);
  }

  mute(): void {
    console.log("Muting audio");
  }

  unmute(): void {
    console.log("Unmuting audio");
  }

  seek(position: number): void {
    console.log(`Seeking to ${position}`);
  }

  getCurrentPosition(): number {
    return 0;
  }

  getDuration(): number {
    return 180;
  }
}

/** 錄音機 */
class AudioRecorder implements Playable, VolumeControllable, Recordable {
  play(): void {
    console.log("Playing recording");
  }

  pause(): void {
    console.log("Pausing playback");
  }

  stop(): void {
    console.log("Stopping playback");
  }

  setVolume(level: number): void {
    console.log(`Setting volume to ${level}`);
  }

  mute(): void {
    console.log("Muting audio");
  }

  unmute(): void {
    console.log("Unmuting audio");
  }

  startRecording(): void {
    console.log("Starting recording");
  }

  stopRecording(): void {
    console.log("Stopping recording");
  }

  saveRecording(filename: string): void {
    console.log(`Saving recording as ${filename}`);
  }
}
```

<br />

## 識別介面職責的方法

### 客戶端分析法

分析不同客戶端的需求

- 哪些客戶端會使用這個介面？

- 不同客戶端需要哪些方法？

- 是否有客戶端只使用部分方法？

### 功能分組法

將相關功能分組

- 哪些方法屬於同一個功能領域？

- 方法之間是否有強烈的關聯性？

- 是否可以獨立使用某組方法？

### 變化頻率分析法

分析方法的變化頻率

- 哪些方法經常一起變化？

- 哪些方法變化頻率不同？

- 變化原因是否相同？

<br />

## 最佳實踐

### 保持介面小而專注
```typescript
/** 好的做法：小而專注的介面 */
interface Drawable {
  draw(): void;
}

interface Movable {
  move(x: number, y: number): void;
}

interface Resizable {
  resize(width: number, height: number): void;
}

/** 避免：包含過多功能的大型介面 */
interface Shape {
  draw(): void;
  move(x: number, y: number): void;
  resize(width: number, height: number): void;
  rotate(angle: number): void;
  animate(): void;
  serialize(): string;
  validate(): boolean;
}
```

### 根據客戶端需求設計介面
```typescript
/** 根據不同客戶端需求設計 */
interface DatabaseReader {
  findById(id: string): any;
  findAll(): any[];
}

interface DatabaseWriter {
  save(entity: any): void;
  update(entity: any): void;
  delete(id: string): void;
}

/** 只讀客戶端 */
class ReportService {
  constructor(private reader: DatabaseReader) {}

  generateReport(): void {
    const data = this.reader.findAll();
    // 產生報表
  }
}

/** 讀寫客戶端 */
class UserService {
  constructor(
    private reader: DatabaseReader,
    private writer: DatabaseWriter
  ) {}

  createUser(userData: any): void {
    this.writer.save(userData);
  }

  getUser(id: string): any {
    return this.reader.findById(id);
  }
}
```

### 使用介面組合
```typescript
/** 組合多個小介面 */
interface FullFeaturedService extends 
  DatabaseReader, 
  DatabaseWriter, 
  Validatable {
}

class AdminService implements FullFeaturedService {
  findById(id: string): any {
    return {};
  }

  findAll(): any[] {
    return [];
  }

  save(entity: any): void {
    console.log("Saving entity");
  }

  update(entity: any): void {
    console.log("Updating entity");
  }

  delete(id: string): void {
    console.log("Deleting entity");
  }

  validate(): boolean {
    return true;
  }
}
```

<br />

## 常見誤區

### 過度分割介面
```typescript
/** 過度分割的例子 */
interface Getter {
  get(): any;
}

interface Setter {
  set(value: any): void;
}

/** 合理的做法 */
interface Property {
  get(): any;
  set(value: any): void;
}
```

### 忽略介面內聚性
```typescript
/** 錯誤：將相關方法分離 */
interface FileOpener {
  open(filename: string): void;
}

interface FileCloser {
  close(): void;
}

/** 正確：保持相關方法的內聚性 */
interface FileHandler {
  open(filename: string): void;
  close(): void;
  isOpen(): boolean;
}
```

### 介面設計過於抽象
```typescript
/** 過於抽象 */
interface Processor {
  process(input: any): any;
}

/** 更具體和有意義 */
interface ImageProcessor {
  resize(width: number, height: number): void;
  applyFilter(filter: string): void;
  convertFormat(format: string): void;
}
```

<br />

## 與其他 SOLID 原則的關係

- 單一職責原則 (SRP)：ISP 確保介面也遵循單一職責

- 開放封閉原則 (OCP)：小型介面更容易擴展而不影響現有程式碼

- 里氏替換原則 (LSP)：專門的介面使得替換更加安全

- 依賴反轉原則 (DIP)：ISP 有助於設計更好的抽象層

<br />

## 總結

ISP 強調介面設計應該以客戶端需求為導向，遵循 ISP 能夠

- 降低耦合度：客戶端只依賴需要的功能

- 提高靈活性：可以獨立修改不同的介面

- 增強可維護性：介面變更影響範圍有限

- 提升程式碼品質：避免介面污染和強制依賴

- 符合最小知識原則：客戶端只知道需要知道的內容

### 注意：多個專門的介面比一個通用的介面更好。

當發現客戶端被迫依賴不需要的方法時，就應該考慮將大型介面拆分成多個小型、專門的介面。
