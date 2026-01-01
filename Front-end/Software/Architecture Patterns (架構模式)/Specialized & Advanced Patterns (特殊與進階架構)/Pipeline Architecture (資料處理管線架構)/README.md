# Pipeline Architecture (資料處理管線架構)

Pipeline Architecture (資料處理管線架構) 是一種將複雜的資料處理任務分解為一系列連續步驟的架構模式，每個步驟都是獨立的處理單元，資料按順序流經這些步驟進行轉換和處理。

這種架構模式特別適合需要對資料進行多階段處理的系統，例如：資料分析、圖像處理、編譯器、ETL (Extract, Transform, Load) 系統等。

<br />

## 動機

在資料處理系統中，常見的問題包括

- 複雜的處理流程難以理解和維護

- 處理步驟緊密耦合，難以獨立測試和修改

- 無法有效利用多核心或分散式處理能力

- 錯誤處理和監控困難

- 處理流程缺乏彈性，難以重組或擴展

Pipeline Architecture 通過將處理流程分解為獨立的階段，解決這些問題，讓系統具備

- 模組化：每個處理步驟都是獨立的模組

- 可重用性：處理步驟可以在不同管線中重複使用

- 可擴展性：可以輕鬆添加、移除或重組處理步驟

- 並行處理：不同步驟可以同時處理不同的資料

<br />

## 結構

Pipeline Architecture 由以下核心元件組成

### 1. Filter (過濾器)

處理資料的獨立元件，負責特定的轉換或處理任務。

- 接收輸入資料

- 執行特定的處理功能

- 產生輸出資料

- 不依賴其他過濾器的內部狀態

### 2. Pipe (管道)

連接過濾器的資料傳輸通道。

- 傳遞資料從一個過濾器到下一個

- 可以是同步或非同步

- 可以包含緩衝機制

### 3. Data Source (資料源)

管線的起始點，提供原始資料。

### 4. Data Sink (資料接收器)

管線的終點，接收處理完成的資料。

以下是 Pipeline Architecture 的結構圖

```text
┌─────────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌─────────────┐
│ Data Source │───>│ Filter 1 │───>│ Filter 2 │───>│ Filter 3 │───>│  Data Sink  │
└─────────────┘    └──────────┘    └──────────┘    └──────────┘    └─────────────┘
                        │               │               │
                        ▼               ▼               ▼
                   Processing       Processing      Processing
                     Step 1           Step 2          Step 3
```

<br />

## 核心原則

### 單一職責原則

每個過濾器只負責一個特定的處理任務。

### 資料流導向

資料按照預定義的順序流經各個處理步驟。

### 無狀態處理

過濾器之間不共享狀態，每個過濾器獨立處理資料。

### 可組合性

過濾器可以靈活組合成不同的處理管線。

<br />

## 實現方式

### Java 實現範例

以圖像處理管線為例

- Filter 介面定義

    ```java
    /** 過濾器介面 */
    public interface Filter<T, R> {
        R process(T input) throws ProcessingException;
    }

    /** 圖像處理過濾器基類 */
    public abstract class ImageFilter implements Filter<BufferedImage, BufferedImage> {
        protected String name;

        public ImageFilter(String name) {
            this.name = name;
        }

        public String getName() {
            return name;
        }
    }
    ```

- 具體過濾器實現

    ```java
    /** 調整亮度過濾器 */
    public class BrightnessFilter extends ImageFilter {
        private final float brightness;

        public BrightnessFilter(float brightness) {
            super("Brightness Filter");
            this.brightness = brightness;
        }

        @Override
        public BufferedImage process(BufferedImage input) {
            BufferedImage output = new BufferedImage(
                input.getWidth(), input.getHeight(), input.getType());

            Graphics2D g2d = output.createGraphics();
            g2d.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER, brightness));
            g2d.drawImage(input, 0, 0, null);
            g2d.dispose();

            return output;
        }
    }

    /** 模糊過濾器 */
    public class BlurFilter extends ImageFilter {
        private final int radius;

        public BlurFilter(int radius) {
            super("Blur Filter");
            this.radius = radius;
        }

        @Override
        public BufferedImage process(BufferedImage input) {
            float[] matrix = new float[radius * radius];
            Arrays.fill(matrix, 1.0f / (radius * radius));

            BufferedImageOp op = new ConvolveOp(
                new Kernel(radius, radius, matrix),
                ConvolveOp.EDGE_NO_OP,
                null
            );

            return op.filter(input, null);
        }
    }

    /** 縮放過濾器 */
    public class ResizeFilter extends ImageFilter {
        private final int width;
        private final int height;

        public ResizeFilter(int width, int height) {
            super("Resize Filter");
            this.width = width;
            this.height = height;
        }

        @Override
        public BufferedImage process(BufferedImage input) {
            BufferedImage output = new BufferedImage(width, height, input.getType());
            Graphics2D g2d = output.createGraphics();
            g2d.setRenderingHint(RenderingHints.KEY_INTERPOLATION,
                RenderingHints.VALUE_INTERPOLATION_BILINEAR);
            g2d.drawImage(input, 0, 0, width, height, null);
            g2d.dispose();
            return output;
        }
    }
    ```

- Pipeline 實現

    ```java
    /** 圖像處理管線 */
    public class ImageProcessingPipeline {
        private final List<ImageFilter> filters;
        private final ExecutorService executor;

        public ImageProcessingPipeline() {
            this.filters = new ArrayList<>();
            this.executor = Executors.newFixedThreadPool(4);
        }

        public ImageProcessingPipeline addFilter(ImageFilter filter) {
            filters.add(filter);
            return this;
        }

        public BufferedImage process(BufferedImage input) throws ProcessingException {
            BufferedImage current = input;

            for (ImageFilter filter : filters) {
                try {
                    current = filter.process(current);
                } catch (Exception e) {
                    throw new ProcessingException(
                        "處理失敗於過濾器: " + filter.getName(), e);
                }
            }

            return current;
        }

        public CompletableFuture<BufferedImage> processAsync(BufferedImage input) {
            return CompletableFuture.supplyAsync(() -> {
                try {
                    return process(input);
                } catch (ProcessingException e) {
                    throw new RuntimeException(e);
                }
            }, executor);
        }

        public void shutdown() {
            executor.shutdown();
        }
    }

    /** 使用範例 */
    public class ImageProcessorExample {
        public static void main(String[] args) {
            ImageProcessingPipeline pipeline = new ImageProcessingPipeline()
                .addFilter(new ResizeFilter(800, 600))
                .addFilter(new BrightnessFilter(0.8f))
                .addFilter(new BlurFilter(3));

            try {
                BufferedImage input = ImageIO.read(new File("input.jpg"));
                BufferedImage output = pipeline.process(input);
                ImageIO.write(output, "jpg", new File("output.jpg"));
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                pipeline.shutdown();
            }
        }
    }
    ```

### TypeScript 與 Node.js 實現範例

以資料處理管線為例

- Filter 介面定義

    ```typescript
    /** 過濾器介面 */
    export interface Filter<T, R> {
      process(input: T): Promise<R>;
      getName(): string;
    }

    /** 抽象過濾器基類 */
    export abstract class BaseFilter<T, R> implements Filter<T, R> {
      constructor(protected readonly name: string) {}

      abstract process(input: T): Promise<R>;

      getName(): string {
        return this.name;
      }
    }
    ```

- 具體過濾器實現

    ```typescript
    /** 資料驗證過濾器 */
    export class ValidationFilter extends BaseFilter<any, any> {
      constructor(private readonly schema: any) {
        super('Validation Filter');
      }

      async process(input: any): Promise<any> {
        const { error, value } = this.schema.validate(input);
        if (error) {
          throw new Error(`驗證失敗: ${error.message}`);
        }
        return value;
      }
    }

    /** 資料轉換過濾器 */
    export class TransformFilter extends BaseFilter<any, any> {
      constructor(private readonly transformer: (data: any) => any) {
        super('Transform Filter');
      }

      async process(input: any): Promise<any> {
        return this.transformer(input);
      }
    }

    /** 資料豐富化過濾器 */
    export class EnrichmentFilter extends BaseFilter<any, any> {
      constructor(
        private readonly enricher: (data: any) => Promise<any>
      ) {
        super('Enrichment Filter');
      }

      async process(input: any): Promise<any> {
        const enrichedData = await this.enricher(input);
        return { ...input, ...enrichedData };
      }
    }

    /** 資料儲存過濾器 */
    export class PersistenceFilter extends BaseFilter<any, any> {
      constructor(
        private readonly repository: Repository
      ) {
        super('Persistence Filter');
      }

      async process(input: any): Promise<any> {
        const saved = await this.repository.save(input);
        return saved;
      }
    }
    ```

- Pipeline 實現

    ```typescript
    /** 資料處理管線 */
    export class DataProcessingPipeline<T, R> {
      private filters: Filter<any, any>[] = [];

      addFilter<U>(filter: Filter<any, U>): DataProcessingPipeline<T, R> {
        this.filters.push(filter);
        return this;
      }

      async process(input: T): Promise<R> {
        let current: any = input;

        for (const filter of this.filters) {
          try {
            current = await filter.process(current);
          } catch (error) {
            throw new Error(
              `處理失敗於過濾器 ${filter.getName()}: ${error.message}`
            );
          }
        }

        return current as R;
      }

      async processMany(inputs: T[]): Promise<R[]> {
        return Promise.all(inputs.map(input => this.process(input)));
      }

      async processStream(inputStream: AsyncIterable<T>): AsyncGenerator<R> {
        for await (const input of inputStream) {
          yield await this.process(input);
        }
      }
    }

    /** 使用範例 */
    interface UserData {
      id: string;
      email: string;
      name: string;
    }

    interface ProcessedUser extends UserData {
      normalizedEmail: string;
      profile?: UserProfile;
      createdAt: Date;
    }

    const userProcessingPipeline = new DataProcessingPipeline<UserData, ProcessedUser>()
      .addFilter(new ValidationFilter(userSchema))
      .addFilter(new TransformFilter((user: UserData) => ({
        ...user,
        normalizedEmail: user.email.toLowerCase().trim()
      })))
      .addFilter(new EnrichmentFilter(async (user: UserData) => {
        const profile = await profileService.getProfile(user.id);
        return { profile };
      }))
      .addFilter(new TransformFilter((user: any) => ({
        ...user,
        createdAt: new Date()
      })))
      .addFilter(new PersistenceFilter(userRepository));

    /** 處理單個使用者 */
    const processedUser = await userProcessingPipeline.process(userData);

    /** 批次處理 */
    const processedUsers = await userProcessingPipeline.processMany(userDataList);
    ```

### Python 實現範例

以文字處理管線為例

- Filter 基類定義

    ```python
    from abc import ABC, abstractmethod
    from typing import Any, List, AsyncGenerator
    import asyncio

    class Filter(ABC):
        def __init__(self, name: str):
            self.name = name

        @abstractmethod
        async def process(self, input_data: Any) -> Any:
            pass

        def get_name(self) -> str:
            return self.name
    ```

- 具體過濾器實現

    ```python
    import re
    from typing import List

    class TextCleaningFilter(Filter):
        def __init__(self):
            super().__init__("Text Cleaning Filter")

        async def process(self, text: str) -> str:
            # 移除多餘空白
            text = re.sub(r'\s+', ' ', text)
            # 移除特殊字符
            text = re.sub(r'[^\w\s]', '', text)
            return text.strip()

    class TokenizationFilter(Filter):
        def __init__(self):
            super().__init__("Tokenization Filter")

        async def process(self, text: str) -> List[str]:
            return text.lower().split()

    class StopWordsFilter(Filter):
        def __init__(self, stop_words: set):
            super().__init__("Stop Words Filter")
            self.stop_words = stop_words

        async def process(self, tokens: List[str]) -> List[str]:
            return [token for token in tokens if token not in self.stop_words]

    class StemmerFilter(Filter):
        def __init__(self):
            super().__init__("Stemmer Filter")

        async def process(self, tokens: List[str]) -> List[str]:
            # 簡單的詞幹提取
            stemmed = []
            for token in tokens:
                if token.endswith('ing'):
                    stemmed.append(token[:-3])
                elif token.endswith('ed'):
                    stemmed.append(token[:-2])
                else:
                    stemmed.append(token)
            return stemmed
    ```

- Pipeline 實現

    ```python
    class TextProcessingPipeline:
        def __init__(self):
            self.filters: List[Filter] = []

        def add_filter(self, filter_instance: Filter) -> 'TextProcessingPipeline':
            self.filters.append(filter_instance)
            return self

        async def process(self, input_data: Any) -> Any:
            current = input_data

            for filter_instance in self.filters:
                try:
                    current = await filter_instance.process(current)
                except Exception as e:
                    raise Exception(
                        f"處理失敗於過濾器 {filter_instance.get_name()}: {str(e)}"
                    )

            return current

        async def process_batch(self, inputs: List[Any]) -> List[Any]:
            tasks = [self.process(input_data) for input_data in inputs]
            return await asyncio.gather(*tasks)

        async def process_stream(self, input_stream: AsyncGenerator[Any, None]) -> AsyncGenerator[Any, None]:
            async for input_data in input_stream:
                yield await self.process(input_data)

    # 使用範例
    async def main():
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}

        pipeline = TextProcessingPipeline() \
            .add_filter(TextCleaningFilter()) \
            .add_filter(TokenizationFilter()) \
            .add_filter(StopWordsFilter(stop_words)) \
            .add_filter(StemmerFilter())

        text = "The quick brown fox is jumping over the lazy dog!"
        result = await pipeline.process(text)
        print(f"處理結果: {result}")

        # 批次處理
        texts = [
            "Hello world! This is a test.",
            "Another example text for processing.",
            "The final text in our batch."
        ]
        results = await pipeline.process_batch(texts)
        for i, result in enumerate(results):
            print(f"文本 {i+1} 處理結果: {result}")

    if __name__ == "__main__":
        asyncio.run(main())
    ```

### React 前端實現範例

以表單資料處理管線為例

- Filter 定義

    ```typescript
    /** 表單過濾器介面 */
    export interface FormFilter<T = any> {
      process(data: T): Promise<T>;
      getName(): string;
    }

    /** 驗證過濾器 */
    export class ValidationFilter implements FormFilter {
      constructor(
        private readonly validator: (data: any) => string | null,
        private readonly fieldName: string
      ) {}

      async process(data: any): Promise<any> {
        const error = this.validator(data[this.fieldName]);
        if (error) {
          throw new Error(`${this.fieldName}: ${error}`);
        }
        return data;
      }

      getName(): string {
        return `Validation Filter (${this.fieldName})`;
      }
    }

    /** 格式化過濾器 */
    export class FormatFilter implements FormFilter {
      constructor(
        private readonly formatter: (value: any) => any,
        private readonly fieldName: string
      ) {}

      async process(data: any): Promise<any> {
        return {
          ...data,
          [this.fieldName]: this.formatter(data[this.fieldName])
        };
      }

      getName(): string {
        return `Format Filter (${this.fieldName})`;
      }
    }

    /** 清理過濾器 */
    export class SanitizeFilter implements FormFilter {
      constructor(
        private readonly sanitizer: (value: any) => any,
        private readonly fieldName: string
      ) {}

      async process(data: any): Promise<any> {
        return {
          ...data,
          [this.fieldName]: this.sanitizer(data[this.fieldName])
        };
      }

      getName(): string {
        return `Sanitize Filter (${this.fieldName})`;
      }
    }
    ```

- Pipeline 實現

    ```typescript
    /** 表單處理管線 */
    export class FormProcessingPipeline {
      private filters: FormFilter[] = [];

      addFilter(filter: FormFilter): FormProcessingPipeline {
        this.filters.push(filter);
        return this;
      }

      async process(formData: any): Promise<any> {
        let current = { ...formData };

        for (const filter of this.filters) {
          try {
            current = await filter.process(current);
          } catch (error) {
            throw new Error(
              `處理失敗於 ${filter.getName()}: ${error.message}`
            );
          }
        }

        return current;
      }
    }

    /** 驗證函數 */
    const validateEmail = (email: string): string | null => {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email) ? null : '請輸入有效的電子郵件地址';
    };

    const validateRequired = (value: any): string | null => {
      return value && value.toString().trim() ? null : '此欄位為必填';
    };

    /** 格式化函數 */
    const formatPhone = (phone: string): string => {
      return phone.replace(/\D/g, '').replace(/(\d{4})(\d{3})(\d{3})/, '$1-$2-$3');
    };

    const formatName = (name: string): string => {
      return name.trim().replace(/\s+/g, ' ');
    };

    /** 清理函數 */
    const sanitizeHtml = (text: string): string => {
      return text.replace(/<[^>]*>/g, '');
    };
    ```

- React 元件使用

    ```typescript
    /** 使用者註冊表單 */
    export const UserRegistrationForm: React.FC = () => {
      const [formData, setFormData] = useState({
        name: '',
        email: '',
        phone: '',
        bio: ''
      });
      const [errors, setErrors] = useState<string[]>([]);
      const [isProcessing, setIsProcessing] = useState(false);

      const pipeline = useMemo(() => {
        return new FormProcessingPipeline()
          .addFilter(new ValidationFilter(validateRequired, 'name'))
          .addFilter(new ValidationFilter(validateRequired, 'email'))
          .addFilter(new ValidationFilter(validateEmail, 'email'))
          .addFilter(new ValidationFilter(validateRequired, 'phone'))
          .addFilter(new SanitizeFilter(sanitizeHtml, 'name'))
          .addFilter(new SanitizeFilter(sanitizeHtml, 'bio'))
          .addFilter(new FormatFilter(formatName, 'name'))
          .addFilter(new FormatFilter(formatPhone, 'phone'));
      }, []);

      const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsProcessing(true);
        setErrors([]);

        try {
          const processedData = await pipeline.process(formData);
          console.log('處理後的資料:', processedData);
          /** 提交到伺服器 */
          await submitUserRegistration(processedData);
          alert('註冊成功！');
        } catch (error) {
          setErrors([error.message]);
        } finally {
          setIsProcessing(false);
        }
      };

      const handleInputChange = (field: string, value: string) => {
        setFormData(prev => ({ ...prev, [field]: value }));
      };

      return (
        <form onSubmit={handleSubmit} className="registration-form">
          <div className="form-group">
            <label htmlFor="name">姓名</label>
            <input
              id="name"
              type="text"
              value={formData.name}
              onChange={(e) => handleInputChange('name', e.target.value)}
              disabled={isProcessing}
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">電子郵件</label>
            <input
              id="email"
              type="email"
              value={formData.email}
              onChange={(e) => handleInputChange('email', e.target.value)}
              disabled={isProcessing}
            />
          </div>

          <div className="form-group">
            <label htmlFor="phone">電話號碼</label>
            <input
              id="phone"
              type="tel"
              value={formData.phone}
              onChange={(e) => handleInputChange('phone', e.target.value)}
              disabled={isProcessing}
            />
          </div>

          <div className="form-group">
            <label htmlFor="bio">個人簡介</label>
            <textarea
              id="bio"
              value={formData.bio}
              onChange={(e) => handleInputChange('bio', e.target.value)}
              disabled={isProcessing}
            />
          </div>

          {errors.length > 0 && (
            <div className="error-messages">
              {errors.map((error, index) => (
                <div key={index} className="error-message">{error}</div>
              ))}
            </div>
          )}

          <button type="submit" disabled={isProcessing}>
            {isProcessing ? '處理中...' : '註冊'}
          </button>
        </form>
      );
    };
    ```

<br />

## 變體模式

### 1. Parallel Pipeline (並行管線)

多個過濾器可以並行處理資料。

```typescript
class ParallelPipeline<T, R> {
  private parallelFilters: Filter<T, any>[][] = [];

  addParallelStage(filters: Filter<T, any>[]): ParallelPipeline<T, R> {
    this.parallelFilters.push(filters);
    return this;
  }

  async process(input: T): Promise<R> {
    let current: any = input;

    for (const stage of this.parallelFilters) {
      const results = await Promise.all(
        stage.map(filter => filter.process(current))
      );
      current = this.mergeResults(results);
    }

    return current as R;
  }

  private mergeResults(results: any[]): any {
    return Object.assign({}, ...results);
  }
}
```

### 2. Conditional Pipeline (條件管線)

根據條件決定執行哪些過濾器。

```typescript
interface ConditionalFilter<T> extends Filter<T, T> {
  shouldProcess(input: T): boolean;
}

class ConditionalPipeline<T> {
  private filters: ConditionalFilter<T>[] = [];

  addFilter(filter: ConditionalFilter<T>): ConditionalPipeline<T> {
    this.filters.push(filter);
    return this;
  }

  async process(input: T): Promise<T> {
    let current = input;

    for (const filter of this.filters) {
      if (filter.shouldProcess(current)) {
        current = await filter.process(current);
      }
    }

    return current;
  }
}
```

### 3. Branching Pipeline (分支管線)

資料可以分流到不同的處理路徑。

```typescript
class BranchingPipeline<T> {
  private branches: Map<string, Filter<T, any>[]> = new Map();
  private router: (input: T) => string;

  constructor(router: (input: T) => string) {
    this.router = router;
  }

  addBranch(name: string, filters: Filter<T, any>[]): BranchingPipeline<T> {
    this.branches.set(name, filters);
    return this;
  }

  async process(input: T): Promise<any> {
    const branchName = this.router(input);
    const filters = this.branches.get(branchName);

    if (!filters) {
      throw new Error(`找不到分支: ${branchName}`);
    }

    let current: any = input;
    for (const filter of filters) {
      current = await filter.process(current);
    }

    return current;
  }
}
```

<br />

## 優點

### 模組化設計

每個處理步驟都是獨立的模組，易於理解和維護。

### 可重用性

過濾器可以在不同的管線中重複使用。

### 可擴展性

可以輕鬆添加、移除或重新排列處理步驟。

### 並行處理

不同的資料可以同時在管線的不同階段進行處理。

### 易於測試

每個過濾器都可以獨立測試。

### 錯誤隔離

錯誤可以被隔離在特定的處理步驟中。

<br />

## 缺點

### 效能開銷

資料在過濾器之間的傳遞可能產生額外的開銷。

### 複雜性

對於簡單的處理任務可能過於複雜。

### 除錯困難

當管線很長時，追蹤資料流和除錯可能變得困難。

### 記憶體使用

若處理大量資料，可能需要大量記憶體來儲存中間結果。

<br />

## 適用場景

### 適合使用

- 資料處理系統：ETL、資料清理、資料轉換

- 圖像處理：濾鏡應用、格式轉換

- 文字處理：自然語言處理、文件轉換

- 編譯器：詞法分析、語法分析、程式碼生成

- 音訊處理：音效處理、格式轉換

- 批次處理：大量資料的批次處理

### 不適合使用

- 互動式應用：需要即時回應的應用

- 簡單處理：只需要一兩個處理步驟的情況

- 狀態相關處理：處理步驟之間需要共享複雜狀態

- 即時系統：對延遲要求極低的系統

<br />

## 實施建議

### 設計原則

- 保持過濾器的單一職責

- 避免過濾器之間的直接依賴

- 設計清晰的資料介面

- 考慮錯誤處理和恢復機制

### 效能優化

- 使用適當的緩衝機制

- 考慮並行處理的可能性

- 避免不必要的資料複製

- 監控記憶體使用情況

### 監控和除錯

- 添加適當的日誌記錄

- 實現處理進度追蹤

- 提供管線視覺化工具

- 建立效能監控機制

### 測試策略

- 單元測試每個過濾器

- 整合測試整個管線

- 效能測試和壓力測試

- 錯誤情況測試

<br />

## 總結

Pipeline Architecture 是一種強大的架構模式，特別適合需要對資料進行多階段處理的系統。通過將複雜的處理流程分解為獨立的過濾器，這種架構提供了良好的模組化、可重用性和可擴展性。

雖然這種架構可能會增加系統的複雜性和效能開銷，但對於需要處理大量資料或複雜處理流程的系統來說，這些優點遠遠超過缺點。關鍵在於根據具體需求選擇合適的實現方式，並注意效能優化和錯誤處理。

在實際應用中，Pipeline Architecture 經常與其他架構模式結合使用，例如：在微服務架構中，每個服務可能內部使用管線架構來處理資料，而服務之間則通過事件驅動的方式進行通訊。
