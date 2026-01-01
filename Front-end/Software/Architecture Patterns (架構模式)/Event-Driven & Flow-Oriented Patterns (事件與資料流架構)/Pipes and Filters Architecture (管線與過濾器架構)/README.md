# Pipes and Filters Architecture (管線與過濾器架構)

Pipes and Filters Architecture (管線與過濾器架構) 是一種資料流導向的軟體架構模式，將複雜的處理任務分解為一系列獨立的過濾器 (Filters)，透過管線 (Pipes) 連接，形成資料處理流水線。

這種架構強調資料的順序處理和轉換，每個過濾器專注於單一職責，透過標準化的介面進行資料傳遞，使系統具備高度的模組化和可重用性。

<br />

## 動機

在資料處理系統中，常見的問題包括

- 複雜的資料處理流程難以理解和維護

- 處理步驟緊密耦合，難以獨立測試和重用

- 資料格式轉換和驗證散布在各處

- 處理流程變更時需要修改大量程式碼

Pipes and Filters Architecture 通過將處理流程分解為獨立的過濾器，解決這些問題，讓系統具備

- 模組化：每個過濾器專注於單一功能

- 可重用性：過濾器可以在不同流程中重複使用

- 可測試性：每個過濾器可以獨立測試

- 可擴展性：容易添加、移除或重新排列過濾器

<br />

## 結構

Pipes and Filters Architecture 由兩個主要元件組成

### 1. Filters (過濾器)

獨立的處理單元，負責特定的資料轉換或處理功能。

- 接收輸入資料

- 執行特定的處理功能

- 產生輸出資料

- 不依賴其他過濾器的內部實作

### 2. Pipes (管線)

連接過濾器的資料傳輸通道。

- 傳遞資料從一個過濾器到另一個

- 提供緩衝機制

- 處理資料同步或非同步傳輸

- 可能包含資料格式轉換

以下是 Pipes and Filters Architecture 的結構圖

```text
┌─────────┐    ┌──────┐    ┌─────────┐    ┌──────┐    ┌─────────┐
│ Input   │───>│ Pipe │───>│ Filter  │───>│ Pipe │───>│ Filter  │
│ Source  │    │  1   │    │    A    │    │  2   │    │    B    │
└─────────┘    └──────┘    └─────────┘    └──────┘    └─────────┘
                                                            │
                                                            ▼
┌─────────┐    ┌──────┐    ┌─────────┐    ┌──────┐    ┌─────────┐
│ Output  │<───│ Pipe │<───│ Filter  │<───│ Pipe │    │ Filter  │
│  Sink   │    │  4   │    │    D    │    │  3   │    │    C    │
└─────────┘    └──────┘    └─────────┘    └──────┘    └─────────┘
```

<br />

## 核心原則

### 單一職責原則 (Single Responsibility Principle)

每個過濾器只負責一個特定的處理功能。

### 資料流導向 (Data Flow Oriented)

系統的行為由資料在過濾器之間的流動決定。

### 介面標準化 (Interface Standardization)

所有過濾器使用統一的輸入輸出介面。

### 獨立性 (Independence)

過濾器之間不直接依賴，只透過管線進行通訊。

<br />

## 實現方式

### Java 實現範例

以日誌處理系統為例

- Filter 介面定義

    ```java
    /** 過濾器介面 */
    public interface Filter<T, R> {
        R process(T input);
    }

    /** 管線介面 */
    public interface Pipe<T> {
        void write(T data);
        T read();
        boolean hasData();
    }
    ```

- 具體過濾器實作

    ```java
    /** 日誌解析過濾器 */
    public class LogParserFilter implements Filter<String, LogEntry> {
        private final Pattern logPattern = Pattern.compile(
            "(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}) \\[(\\w+)\\](.+)"
        );

        @Override
        public LogEntry process(String rawLog) {
            Matcher matcher = logPattern.matcher(rawLog);
            if (matcher.matches()) {
                return new LogEntry(
                    LocalDateTime.parse(matcher.group(1), 
                        DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")),
                    LogLevel.valueOf(matcher.group(2)),
                    matcher.group(3)
                );
            }
            throw new IllegalArgumentException("無效的日誌格式: " + rawLog);
        }
    }

    /** 日誌過濾器 */
    public class LogLevelFilter implements Filter<LogEntry, LogEntry> {
        private final Set<LogLevel> allowedLevels;

        public LogLevelFilter(LogLevel... levels) {
            this.allowedLevels = EnumSet.of(levels[0], levels);
        }

        @Override
        public LogEntry process(LogEntry logEntry) {
            if (allowedLevels.contains(logEntry.getLevel())) {
                return logEntry;
            }
            return null; /** 過濾掉不符合條件的日誌 */
        }
    }

    /** 日誌格式化過濾器 */
    public class LogFormatterFilter implements Filter<LogEntry, String> {
        @Override
        public String process(LogEntry logEntry) {
            return String.format("[%s] %s - %s",
                logEntry.getTimestamp().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME),
                logEntry.getLevel(),
                logEntry.getMessage()
            );
        }
    }
    ```

- 管線實作

    ```java
    /** 記憶體管線實作 */
    public class MemoryPipe<T> implements Pipe<T> {
        private final Queue<T> buffer = new ConcurrentLinkedQueue<>();
        private final int maxSize;

        public MemoryPipe(int maxSize) {
            this.maxSize = maxSize;
        }

        @Override
        public void write(T data) {
            if (buffer.size() >= maxSize) {
                throw new IllegalStateException("管線緩衝區已滿");
            }
            buffer.offer(data);
        }

        @Override
        public T read() {
            return buffer.poll();
        }

        @Override
        public boolean hasData() {
            return !buffer.isEmpty();
        }
    }
    ```

- 管線系統組裝

    ```java
    /** 管線系統 */
    public class LogProcessingPipeline {
        private final LogParserFilter parserFilter;
        private final LogLevelFilter levelFilter;
        private final LogFormatterFilter formatterFilter;

        private final Pipe<String> rawLogPipe;
        private final Pipe<LogEntry> parsedLogPipe;
        private final Pipe<LogEntry> filteredLogPipe;
        private final Pipe<String> formattedLogPipe;

        public LogProcessingPipeline() {
            this.parserFilter = new LogParserFilter();
            this.levelFilter = new LogLevelFilter(LogLevel.ERROR, LogLevel.WARN);
            this.formatterFilter = new LogFormatterFilter();

            this.rawLogPipe = new MemoryPipe<>(1000);
            this.parsedLogPipe = new MemoryPipe<>(1000);
            this.filteredLogPipe = new MemoryPipe<>(1000);
            this.formattedLogPipe = new MemoryPipe<>(1000);
        }

        public void processLogs(List<String> rawLogs) {
            /** 階段 1: 解析原始日誌 */
            for (String rawLog : rawLogs) {
                try {
                    LogEntry parsed = parserFilter.process(rawLog);
                    parsedLogPipe.write(parsed);
                } catch (Exception e) {
                    System.err.println("解析失敗: " + rawLog);
                }
            }

            /** 階段 2: 過濾日誌等級 */
            while (parsedLogPipe.hasData()) {
                LogEntry logEntry = parsedLogPipe.read();
                LogEntry filtered = levelFilter.process(logEntry);
                if (filtered != null) {
                    filteredLogPipe.write(filtered);
                }
            }

            /** 階段 3: 格式化輸出 */
            while (filteredLogPipe.hasData()) {
                LogEntry logEntry = filteredLogPipe.read();
                String formatted = formatterFilter.process(logEntry);
                formattedLogPipe.write(formatted);
            }
        }

        public List<String> getProcessedLogs() {
            List<String> results = new ArrayList<>();
            while (formattedLogPipe.hasData()) {
                results.add(formattedLogPipe.read());
            }
            return results;
        }
    }
    ```

### TypeScript 與 Node.js 實現範例

- Filter 和 Pipe 介面定義

    ```typescript
    /** 過濾器介面 */
    export interface Filter<T, R> {
      process(input: T): R | Promise<R>;
    }

    /** 管線介面 */
    export interface Pipe<T> {
      write(data: T): void;
      read(): T | undefined;
      hasData(): boolean;
    }

    /** 非同步管線介面 */
    export interface AsyncPipe<T> {
      write(data: T): Promise<void>;
      read(): Promise<T | undefined>;
      hasData(): Promise<boolean>;
    }
    ```

- 資料處理過濾器實作

    ```typescript
    /** CSV 解析過濾器 */
    export class CsvParserFilter implements Filter<string, Record<string, string>[]> {
      constructor(private readonly delimiter: string = ',') {}

      process(csvContent: string): Record<string, string>[] {
        const lines = csvContent.trim().split('\n');
        if (lines.length === 0) return [];

        const headers = lines[0].split(this.delimiter);
        const records: Record<string, string>[] = [];

        for (let i = 1; i < lines.length; i++) {
          const values = lines[i].split(this.delimiter);
          const record: Record<string, string> = {};

          headers.forEach((header, index) => {
            record[header.trim()] = values[index]?.trim() || '';
          });

          records.push(record);
        }

        return records;
      }
    }

    /** 資料驗證過濾器 */
    export class DataValidationFilter implements Filter<Record<string, string>[], Record<string, string>[]> {
      constructor(private readonly requiredFields: string[]) {}

      process(records: Record<string, string>[]): Record<string, string>[] {
        return records.filter(record => {
          return this.requiredFields.every(field => {
            const value = record[field];
            return value !== undefined && value !== null && value.trim() !== '';
          });
        });
      }
    }

    /** 資料轉換過濾器 */
    export class DataTransformFilter implements Filter<Record<string, string>[], any[]> {
      constructor(private readonly transformFn: (record: Record<string, string>) => any) {}

      process(records: Record<string, string>[]): any[] {
        return records.map(this.transformFn);
      }
    }

    /** JSON 序列化過濾器 */
    export class JsonSerializerFilter implements Filter<any[], string> {
      process(data: any[]): string {
        return JSON.stringify(data, null, 2);
      }
    }
    ```

- 管線實作

    ```typescript
    /** 記憶體管線實作 */
    export class MemoryPipe<T> implements Pipe<T> {
      private buffer: T[] = [];

      constructor(private readonly maxSize: number = 1000) {}

      write(data: T): void {
        if (this.buffer.length >= this.maxSize) {
          throw new Error('管線緩衝區已滿');
        }
        this.buffer.push(data);
      }

      read(): T | undefined {
        return this.buffer.shift();
      }

      hasData(): boolean {
        return this.buffer.length > 0;
      }
    }

    /** 檔案管線實作 */
    export class FilePipe implements AsyncPipe<string> {
      constructor(
        private readonly filePath: string,
        private readonly fs: any /** Node.js fs module */
      ) {}

      async write(data: string): Promise<void> {
        await this.fs.promises.appendFile(this.filePath, data + '\n');
      }

      async read(): Promise<string | undefined> {
        try {
          const content = await this.fs.promises.readFile(this.filePath, 'utf-8');
          const lines = content.trim().split('\n');
          return lines.length > 0 ? lines[0] : undefined;
        } catch (error) {
          return undefined;
        }
      }

      async hasData(): Promise<boolean> {
        try {
          const stats = await this.fs.promises.stat(this.filePath);
          return stats.size > 0;
        } catch (error) {
          return false;
        }
      }
    }
    ```

- 管線系統組裝

    ```typescript
    /** 資料處理管線系統 */
    export class DataProcessingPipeline {
      private readonly csvParser: CsvParserFilter;
      private readonly validator: DataValidationFilter;
      private readonly transformer: DataTransformFilter;
      private readonly serializer: JsonSerializerFilter;

      private readonly rawDataPipe: Pipe<string>;
      private readonly parsedDataPipe: Pipe<Record<string, string>[]>;
      private readonly validatedDataPipe: Pipe<Record<string, string>[]>;
      private readonly transformedDataPipe: Pipe<any[]>;
      private readonly outputPipe: Pipe<string>;

      constructor() {
        this.csvParser = new CsvParserFilter();
        this.validator = new DataValidationFilter(['name', 'email']);
        this.transformer = new DataTransformFilter(record => ({
          fullName: record.name,
          emailAddress: record.email,
          processedAt: new Date().toISOString()
        }));
        this.serializer = new JsonSerializerFilter();

        this.rawDataPipe = new MemoryPipe<string>(100);
        this.parsedDataPipe = new MemoryPipe<Record<string, string>[]>(100);
        this.validatedDataPipe = new MemoryPipe<Record<string, string>[]>(100);
        this.transformedDataPipe = new MemoryPipe<any[]>(100);
        this.outputPipe = new MemoryPipe<string>(100);
      }

      async processData(csvData: string): Promise<string[]> {
        /** 階段 1: 解析 CSV */
        const parsed = this.csvParser.process(csvData);
        this.parsedDataPipe.write(parsed);

        /** 階段 2: 驗證資料 */
        while (this.parsedDataPipe.hasData()) {
          const data = this.parsedDataPipe.read()!;
          const validated = this.validator.process(data);
          if (validated.length > 0) {
            this.validatedDataPipe.write(validated);
          }
        }

        /** 階段 3: 轉換資料 */
        while (this.validatedDataPipe.hasData()) {
          const data = this.validatedDataPipe.read()!;
          const transformed = this.transformer.process(data);
          this.transformedDataPipe.write(transformed);
        }

        /** 階段 4: 序列化輸出 */
        const results: string[] = [];
        while (this.transformedDataPipe.hasData()) {
          const data = this.transformedDataPipe.read()!;
          const serialized = this.serializer.process(data);
          results.push(serialized);
        }

        return results;
      }
    }
    ```

### Python 實現範例

- 影像處理管線系統

    ```python
    from abc import ABC, abstractmethod
    from typing import Any, Optional, List
    from queue import Queue
    import cv2
    import numpy as np

    class Filter(ABC):
        """過濾器抽象基類"""

        @abstractmethod
        def process(self, input_data: Any) -> Any:
            pass

    class Pipe:
        """管線實作"""

        def __init__(self, max_size: int = 100):
            self._queue = Queue(maxsize=max_size)

        def write(self, data: Any) -> None:
            if self._queue.full():
                raise Exception("管線緩衝區已滿")
            self._queue.put(data)

        def read(self) -> Optional[Any]:
            if self._queue.empty():
                return None
            return self._queue.get()

        def has_data(self) -> bool:
            return not self._queue.empty()

    class ImageLoaderFilter(Filter):
        """影像載入過濾器"""

        def process(self, image_path: str) -> np.ndarray:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"無法載入影像: {image_path}")
            return image

    class GrayscaleFilter(Filter):
        """灰階轉換過濾器"""

        def process(self, image: np.ndarray) -> np.ndarray:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    class BlurFilter(Filter):
        """模糊過濾器"""

        def __init__(self, kernel_size: int = 5):
            self.kernel_size = kernel_size

        def process(self, image: np.ndarray) -> np.ndarray:
            return cv2.GaussianBlur(image, (self.kernel_size, self.kernel_size), 0)

    class EdgeDetectionFilter(Filter):
        """邊緣檢測過濾器"""

        def __init__(self, threshold1: int = 100, threshold2: int = 200):
            self.threshold1 = threshold1
            self.threshold2 = threshold2

        def process(self, image: np.ndarray) -> np.ndarray:
            return cv2.Canny(image, self.threshold1, self.threshold2)

    class ImageSaverFilter(Filter):
        """影像儲存過濾器"""

        def __init__(self, output_dir: str):
            self.output_dir = output_dir

        def process(self, data: tuple) -> str:
            image, filename = data
            output_path = f"{self.output_dir}/{filename}"
            cv2.imwrite(output_path, image)
            return output_path

    class ImageProcessingPipeline:
        """影像處理管線系統"""

        def __init__(self, output_dir: str):
            # 初始化過濾器
            self.loader = ImageLoaderFilter()
            self.grayscale = GrayscaleFilter()
            self.blur = BlurFilter(kernel_size=3)
            self.edge_detection = EdgeDetectionFilter()
            self.saver = ImageSaverFilter(output_dir)

            # 初始化管線
            self.loaded_pipe = Pipe()
            self.grayscale_pipe = Pipe()
            self.blurred_pipe = Pipe()
            self.edges_pipe = Pipe()
            self.output_pipe = Pipe()

        def process_images(self, image_paths: List[str]) -> List[str]:
            results = []

            for image_path in image_paths:
                try:
                    # 階段 1: 載入影像
                    loaded_image = self.loader.process(image_path)
                    self.loaded_pipe.write((loaded_image, image_path))

                    # 階段 2: 轉換為灰階
                    while self.loaded_pipe.has_data():
                        image, path = self.loaded_pipe.read()
                        gray_image = self.grayscale.process(image)
                        self.grayscale_pipe.write((gray_image, path))

                    # 階段 3: 模糊處理
                    while self.grayscale_pipe.has_data():
                        image, path = self.grayscale_pipe.read()
                        blurred_image = self.blur.process(image)
                        self.blurred_pipe.write((blurred_image, path))

                    # 階段 4: 邊緣檢測
                    while self.blurred_pipe.has_data():
                        image, path = self.blurred_pipe.read()
                        edges_image = self.edge_detection.process(image)
                        filename = f"edges_{path.split('/')[-1]}"
                        self.edges_pipe.write((edges_image, filename))

                    # 階段 5: 儲存結果
                    while self.edges_pipe.has_data():
                        image, filename = self.edges_pipe.read()
                        output_path = self.saver.process((image, filename))
                        results.append(output_path)

                except Exception as e:
                    print(f"處理影像失敗 {image_path}: {e}")

            return results
    ```

<br />

## 優點

### 模組化

每個過濾器都是獨立的模組，可以單獨開發、測試和維護。

### 可重用性

過濾器可以在不同的管線中重複使用，提高程式碼重用率。

### 可擴展性

容易添加新的過濾器或修改現有的處理流程。

### 並行處理

不同的過濾器可以並行執行，提高系統效能。

### 容錯性

單一過濾器的失敗不會影響整個系統的運作。

### 可測試性

每個過濾器可以獨立進行單元測試。

<br />

## 缺點

### 效能開銷

資料在過濾器之間的傳遞可能產生額外的效能開銷。

### 複雜性

對於簡單的處理任務可能過於複雜。

### 資料格式依賴

過濾器之間需要統一的資料格式，限制了靈活性。

### 除錯困難

當管線很長時，除錯和追蹤問題可能變得困難。

### 記憶體使用

管線緩衝區可能消耗大量記憶體。

<br />

## 適用場景

### 適合使用

- 資料處理系統：ETL、資料清理、格式轉換

- 影像處理：影像濾鏡、格式轉換、特效處理

- 音訊處理：音效處理、格式轉換、降噪

- 編譯器：詞法分析、語法分析、程式碼生成

- 網路處理：封包處理、協定轉換、資料壓縮

- 批次處理：大量資料的順序處理

### 不適合使用

- 互動式應用：需要即時回應的使用者介面

- 複雜控制流程：包含大量條件分支和迴圈

- 狀態相依處理：需要維護複雜狀態的系統

- 即時系統：對延遲要求極高的系統

<br />

## 變體模式

### 1. Pipeline Pattern (管線模式)

強調順序處理，每個階段的輸出成為下一個階段的輸入。

### 2. Producer-Consumer Pattern (生產者-消費者模式)

使用佇列作為緩衝區，支援非同步處理。

### 3. Stream Processing (串流處理)

處理連續的資料流，支援即時處理。

### 4. MapReduce Pattern

結合 Map 和 Reduce 操作，適用於大資料處理。

<br />

## 實施建議

### 介面設計

定義清晰的過濾器介面，確保所有過濾器遵循相同的契約。

### 錯誤處理

建立完善的錯誤處理機制，避免單一過濾器的失敗影響整個管線。

### 效能監控

監控每個過濾器的效能，識別瓶頸並進行最佳化。

### 資料格式標準化

建立統一的資料格式標準，確保過濾器之間的相容性。

### 測試策略

為每個過濾器建立獨立的測試，並進行整合測試驗證整個管線。

### 文件化

詳細記錄每個過濾器的功能、輸入輸出格式和使用方式。

<br />

## 總結

Pipes and Filters Architecture 是一種強大的資料處理架構模式，特別適合需要順序處理和轉換資料的系統。透過將複雜的處理流程分解為獨立的過濾器，這種架構提供了良好的模組化、可重用性和可擴展性。

雖然這種架構可能會帶來一些效能開銷和複雜性，但對於資料處理、影像處理、編譯器等領域的應用來說，其優點遠大於缺點。關鍵在於根據具體需求選擇合適的實作方式，並建立完善的錯誤處理和監控機制。
