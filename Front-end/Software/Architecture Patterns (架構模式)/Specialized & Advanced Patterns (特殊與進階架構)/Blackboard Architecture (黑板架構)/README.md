# Blackboard Architecture (黑板架構)

Blackboard Architecture (黑板架構) 是一種基於共享資料空間的軟體架構模式，多個獨立的知識源 (Knowledge Sources) 透過共同的黑板 (Blackboard) 進行協作，解決複雜的問題。

這種架構特別適用於需要多種專業知識協同工作的問題領域，例如：人工智慧、專家系統、語音識別、影像處理等複雜的認知任務。

<br />

## 動機

在解決複雜問題時，常見的挑戰包括

- 問題需要多種不同的專業知識和演算法

- 解決方案的路徑不確定，需要探索性的方法

- 各個知識源之間需要共享中間結果

- 系統需要支援增量式的問題解決過程

Blackboard Architecture 通過提供共享的工作空間和靈活的控制機制，解決這些問題，讓系統具備

- 模組化：各知識源獨立開發和維護

- 靈活性：支援動態的問題解決策略

- 可擴展性：容易添加新的知識源

- 協作性：多個專家系統協同工作

<br />

## 結構

Blackboard Architecture 由三個主要元件構成

### 1. Blackboard (黑板)

共享的資料結構，存儲問題解決過程中的所有資訊。

- 包含問題的初始狀態、中間結果和最終解答

- 提供結構化的資料組織方式

- 支援多層次的抽象層級

### 2. Knowledge Sources (知識源)

獨立的專家模組，各自擁有特定領域的知識。

- 監控黑板上的相關資訊

- 在適當時機貢獻知識

- 不直接與其他知識源通訊

### 3. Control Component (控制元件)

協調知識源的執行順序和策略。

- 決定下一個執行的知識源

- 管理問題解決的整體策略

- 處理衝突和優先順序

以下是 Blackboard Architecture 的結構圖

```text
┌───────────────────────────────────────────────────────────────┐
│                       Control Component                       │
└──────────────────────────────┬────────────────────────────────┘
                               │
                               │ control
                               │
┌──────────────────────────────▼────────────────────────────────┐
│                         Blackboard                            │
│   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐      │
│   │   Level 3    │   │   Level 2    │   │   Level 1    │      │
│   └──────────────┘   └──────────────┘   └──────────────┘      │
└──────────▲──────────────────▲───────────────────▲─────────────┘
           │                  │                   │
           │  read/write      │  read/write       │  read/write
           │                  │                   │
   ┌───────▼───────┐   ┌──────▼────────┐   ┌──────▼────────┐
   │  Knowledge    │   │  Knowledge    │   │  Knowledge    │
   │  Source 1     │   │  Source 2     │   │  Source 3     │
   └───────────────┘   └───────────────┘   └───────────────┘
```

<br />

## 核心原則

### 機會主義問題解決 (Opportunistic Problem Solving)

知識源根據當前黑板狀態決定是否執行，支援靈活的問題解決策略。

### 增量式構建 (Incremental Construction)

解決方案透過多個知識源的貢獻逐步建構完成。

### 多層次抽象 (Multi-level Abstraction)

黑板支援不同抽象層級的資料表示和處理。

<br />

## 實現方式

### Java 實現範例

以語音識別系統為例

- Blackboard (黑板)

    ```java
    /** 黑板資料結構 */
    public class Blackboard {
        private final Map<String, Object> data = new ConcurrentHashMap<>();
        private final List<BlackboardListener> listeners = new ArrayList<>();
        private final ReadWriteLock lock = new ReentrantReadWriteLock();

        public void write(String key, Object value) {
            lock.writeLock().lock();
            try {
                data.put(key, value);
                notifyListeners(key, value);
            } finally {
                lock.writeLock().unlock();
            }
        }

        public <T> Optional<T> read(String key, Class<T> type) {
            lock.readLock().lock();
            try {
                Object value = data.get(key);
                return type.isInstance(value) ? 
                    Optional.of(type.cast(value)) : Optional.empty();
            } finally {
                lock.readLock().unlock();
            }
        }

        public void addListener(BlackboardListener listener) {
            listeners.add(listener);
        }

        private void notifyListeners(String key, Object value) {
            listeners.forEach(listener -> listener.onDataChanged(key, value));
        }
    }

    /** 黑板監聽器介面 */
    public interface BlackboardListener {
        void onDataChanged(String key, Object value);
    }
    ```

- Knowledge Sources (知識源)

    ```java
    /** 知識源基礎類別 */
    public abstract class KnowledgeSource implements BlackboardListener {
        protected final Blackboard blackboard;
        protected final String name;

        public KnowledgeSource(String name, Blackboard blackboard) {
            this.name = name;
            this.blackboard = blackboard;
            this.blackboard.addListener(this);
        }

        public abstract boolean canExecute();
        public abstract void execute();
        public abstract int getPriority();

        @Override
        public void onDataChanged(String key, Object value) {
            if (canExecute()) {
                ControlComponent.getInstance().scheduleExecution(this);
            }
        }
    }

    /** 聲學處理知識源 */
    public class AcousticProcessor extends KnowledgeSource {
        public AcousticProcessor(Blackboard blackboard) {
            super("AcousticProcessor", blackboard);
        }

        @Override
        public boolean canExecute() {
            return blackboard.read("rawAudio", byte[].class).isPresent() &&
                   !blackboard.read("acousticFeatures", double[].class).isPresent();
        }

        @Override
        public void execute() {
            Optional<byte[]> rawAudio = blackboard.read("rawAudio", byte[].class);
            if (rawAudio.isPresent()) {
                double[] features = extractAcousticFeatures(rawAudio.get());
                blackboard.write("acousticFeatures", features);
            }
        }

        @Override
        public int getPriority() {
            return 10; // 高優先順序
        }

        private double[] extractAcousticFeatures(byte[] audio) {
            // 聲學特徵提取演算法
            return new double[]{0.1, 0.2, 0.3}; // 簡化範例
        }
    }

    /** 語音識別知識源 */
    public class SpeechRecognizer extends KnowledgeSource {
        public SpeechRecognizer(Blackboard blackboard) {
            super("SpeechRecognizer", blackboard);
        }

        @Override
        public boolean canExecute() {
            return blackboard.read("acousticFeatures", double[].class).isPresent() &&
                   !blackboard.read("recognizedWords", List.class).isPresent();
        }

        @Override
        public void execute() {
            Optional<double[]> features = blackboard.read("acousticFeatures", double[].class);
            if (features.isPresent()) {
                List<String> words = recognizeWords(features.get());
                blackboard.write("recognizedWords", words);
            }
        }

        @Override
        public int getPriority() {
            return 8;
        }

        private List<String> recognizeWords(double[] features) {
            // 語音識別演算法
            return Arrays.asList("hello", "world"); // 簡化範例
        }
    }
    ```

- Control Component (控制元件)

    ```java
    /** 控制元件 */
    public class ControlComponent {
        private static ControlComponent instance;
        private final PriorityQueue<KnowledgeSource> executionQueue;
        private final ExecutorService executor;
        private volatile boolean running = true;

        private ControlComponent() {
            this.executionQueue = new PriorityQueue<>(
                Comparator.comparingInt(KnowledgeSource::getPriority).reversed()
            );
            this.executor = Executors.newSingleThreadExecutor();
            startControlLoop();
        }

        public static synchronized ControlComponent getInstance() {
            if (instance == null) {
                instance = new ControlComponent();
            }
            return instance;
        }

        public synchronized void scheduleExecution(KnowledgeSource ks) {
            if (!executionQueue.contains(ks)) {
                executionQueue.offer(ks);
            }
        }

        private void startControlLoop() {
            executor.submit(() -> {
                while (running) {
                    try {
                        KnowledgeSource ks = getNextKnowledgeSource();
                        if (ks != null && ks.canExecute()) {
                            ks.execute();
                        }
                        Thread.sleep(100); // 避免忙碌等待
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            });
        }

        private synchronized KnowledgeSource getNextKnowledgeSource() {
            return executionQueue.poll();
        }

        public void shutdown() {
            running = false;
            executor.shutdown();
        }
    }
    ```

### TypeScript 與 Node.js 實現範例

以影像處理系統為例

- Blackboard (黑板)

    ```typescript
    /** 黑板事件介面 */
    interface BlackboardEvent {
      key: string;
      value: any;
      timestamp: Date;
    }

    /** 黑板監聽器介面 */
    interface BlackboardListener {
      onDataChanged(event: BlackboardEvent): void;
    }

    /** 黑板實作 */
    export class Blackboard {
      private data = new Map<string, any>();
      private listeners: BlackboardListener[] = [];

      write(key: string, value: any): void {
        this.data.set(key, value);
        const event: BlackboardEvent = {
          key,
          value,
          timestamp: new Date()
        };
        this.notifyListeners(event);
      }

      read<T>(key: string): T | undefined {
        return this.data.get(key) as T;
      }

      has(key: string): boolean {
        return this.data.has(key);
      }

      addListener(listener: BlackboardListener): void {
        this.listeners.push(listener);
      }

      private notifyListeners(event: BlackboardEvent): void {
        this.listeners.forEach(listener => {
          try {
            listener.onDataChanged(event);
          } catch (error) {
            console.error('監聽器執行錯誤:', error);
          }
        });
      }
    }
    ```

- Knowledge Sources (知識源)

    ```typescript
    /** 知識源基礎類別 */
    export abstract class KnowledgeSource implements BlackboardListener {
      constructor(
        protected readonly name: string,
        protected readonly blackboard: Blackboard
      ) {
        this.blackboard.addListener(this);
      }

      abstract canExecute(): boolean;
      abstract execute(): Promise<void>;
      abstract getPriority(): number;

      onDataChanged(event: BlackboardEvent): void {
        if (this.canExecute()) {
          ControlComponent.getInstance().scheduleExecution(this);
        }
      }
    }

    /** 邊緣檢測知識源 */
    export class EdgeDetector extends KnowledgeSource {
      constructor(blackboard: Blackboard) {
        super('EdgeDetector', blackboard);
      }

      canExecute(): boolean {
        return this.blackboard.has('rawImage') && 
               !this.blackboard.has('edges');
      }

      async execute(): Promise<void> {
        const rawImage = this.blackboard.read<ImageData>('rawImage');
        if (rawImage) {
          const edges = await this.detectEdges(rawImage);
          this.blackboard.write('edges', edges);
        }
      }

      getPriority(): number {
        return 9;
      }

      private async detectEdges(image: ImageData): Promise<number[][]> {
        // 邊緣檢測演算法
        return [[1, 0, 1], [0, 1, 0], [1, 0, 1]]; // 簡化範例
      }
    }

    /** 物件識別知識源 */
    export class ObjectRecognizer extends KnowledgeSource {
      constructor(blackboard: Blackboard) {
        super('ObjectRecognizer', blackboard);
      }

      canExecute(): boolean {
        return this.blackboard.has('edges') && 
               !this.blackboard.has('objects');
      }

      async execute(): Promise<void> {
        const edges = this.blackboard.read<number[][]>('edges');
        if (edges) {
          const objects = await this.recognizeObjects(edges);
          this.blackboard.write('objects', objects);
        }
      }

      getPriority(): number {
        return 7;
      }

      private async recognizeObjects(edges: number[][]): Promise<string[]> {
        // 物件識別演算法
        return ['car', 'person']; // 簡化範例
      }
    }
    ```

- Control Component (控制元件)

    ```typescript
    /** 控制元件 */
    export class ControlComponent {
      private static instance: ControlComponent;
      private executionQueue: KnowledgeSource[] = [];
      private isRunning = false;

      private constructor() {}

      static getInstance(): ControlComponent {
        if (!ControlComponent.instance) {
          ControlComponent.instance = new ControlComponent();
        }
        return ControlComponent.instance;
      }

      scheduleExecution(ks: KnowledgeSource): void {
        if (!this.executionQueue.includes(ks)) {
          this.executionQueue.push(ks);
          this.sortQueue();
        }

        if (!this.isRunning) {
          this.startControlLoop();
        }
      }

      private sortQueue(): void {
        this.executionQueue.sort((a, b) => b.getPriority() - a.getPriority());
      }

      private async startControlLoop(): Promise<void> {
        this.isRunning = true;

        while (this.executionQueue.length > 0) {
          const ks = this.executionQueue.shift();
          if (ks && ks.canExecute()) {
            try {
              await ks.execute();
            } catch (error) {
              console.error(`知識源 ${ks.name} 執行錯誤:`, error);
            }
          }

          /** 短暫延遲避免忙碌等待 */
          await new Promise(resolve => setTimeout(resolve, 10));
        }

        this.isRunning = false;
      }
    }
    ```

### React 前端實現範例

以協作式文件編輯為例

- Blackboard (黑板)

    ```typescript
    /** 文件狀態介面 */
    interface DocumentState {
      content: string;
      cursor: number;
      selection: { start: number; end: number } | null;
      suggestions: string[];
      errors: Array<{ line: number; message: string }>;
    }

    /** React 黑板 Hook */
    export const useBlackboard = () => {
      const [state, setState] = useState<DocumentState>({
        content: '',
        cursor: 0,
        selection: null,
        suggestions: [],
        errors: []
      });

      const blackboard = useMemo(() => {
        const bb = new Blackboard();

        /** 監聽黑板變化並更新 React 狀態 */
        bb.addListener({
          onDataChanged: (event) => {
            setState(prevState => ({
              ...prevState,
              [event.key]: event.value
            }));
          }
        });

        return bb;
      }, []);

      const updateContent = useCallback((content: string) => {
        blackboard.write('content', content);
      }, [blackboard]);

      const updateCursor = useCallback((cursor: number) => {
        blackboard.write('cursor', cursor);
      }, [blackboard]);

      return {
        state,
        blackboard,
        updateContent,
        updateCursor
      };
    };
    ```

- Knowledge Sources (知識源)

    ```typescript
    /** 語法檢查知識源 */
    export class SyntaxChecker extends KnowledgeSource {
      constructor(blackboard: Blackboard) {
        super('SyntaxChecker', blackboard);
      }

      canExecute(): boolean {
        return this.blackboard.has('content');
      }

      async execute(): Promise<void> {
        const content = this.blackboard.read<string>('content');
        if (content) {
          const errors = this.checkSyntax(content);
          this.blackboard.write('errors', errors);
        }
      }

      getPriority(): number {
        return 8;
      }

      private checkSyntax(content: string): Array<{ line: number; message: string }> {
        const errors: Array<{ line: number; message: string }> = [];
        const lines = content.split('\n');

        lines.forEach((line, index) => {
          if (line.includes('TODO')) {
            errors.push({
              line: index + 1,
              message: '待完成項目'
            });
          }
        });

        return errors;
      }
    }

    /** 自動完成知識源 */
    export class AutoCompleter extends KnowledgeSource {
      constructor(blackboard: Blackboard) {
        super('AutoCompleter', blackboard);
      }

      canExecute(): boolean {
        return this.blackboard.has('content') && this.blackboard.has('cursor');
      }

      async execute(): Promise<void> {
        const content = this.blackboard.read<string>('content');
        const cursor = this.blackboard.read<number>('cursor');

        if (content && cursor !== undefined) {
          const suggestions = this.generateSuggestions(content, cursor);
          this.blackboard.write('suggestions', suggestions);
        }
      }

      getPriority(): number {
        return 6;
      }

      private generateSuggestions(content: string, cursor: number): string[] {
        const currentWord = this.getCurrentWord(content, cursor);
        const keywords = ['function', 'const', 'let', 'var', 'class', 'interface'];

        return keywords.filter(keyword => 
          keyword.startsWith(currentWord.toLowerCase())
        );
      }

      private getCurrentWord(content: string, cursor: number): string {
        const beforeCursor = content.substring(0, cursor);
        const match = beforeCursor.match(/\w+$/);
        return match ? match[0] : '';
      }
    }
    ```

- React 元件

    ```typescript
    /** 協作編輯器元件 */
    export const CollaborativeEditor: React.FC = () => {
      const { state, blackboard, updateContent, updateCursor } = useBlackboard();
      const textareaRef = useRef<HTMLTextAreaElement>(null);

      /** 初始化知識源 */
      useEffect(() => {
        const syntaxChecker = new SyntaxChecker(blackboard);
        const autoCompleter = new AutoCompleter(blackboard);

        return () => {
          // 清理資源
        };
      }, [blackboard]);

      const handleContentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        const newContent = e.target.value;
        updateContent(newContent);
      };

      const handleCursorChange = () => {
        if (textareaRef.current) {
          updateCursor(textareaRef.current.selectionStart);
        }
      };

      const applySuggestion = (suggestion: string) => {
        if (textareaRef.current) {
          const textarea = textareaRef.current;
          const start = textarea.selectionStart;
          const end = textarea.selectionEnd;
          const newContent = 
            state.content.substring(0, start) + 
            suggestion + 
            state.content.substring(end);

          updateContent(newContent);
        }
      };

      return (
        <div className="collaborative-editor">
          <div className="editor-container">
            <textarea
              ref={textareaRef}
              value={state.content}
              onChange={handleContentChange}
              onSelect={handleCursorChange}
              onKeyUp={handleCursorChange}
              className="editor-textarea"
              placeholder="開始輸入..."
            />

            {state.suggestions.length > 0 && (
              <div className="suggestions">
                <h4>建議</h4>
                {state.suggestions.map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={() => applySuggestion(suggestion)}
                    className="suggestion-item"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            )}
          </div>

          {state.errors.length > 0 && (
            <div className="errors">
              <h4>錯誤</h4>
              {state.errors.map((error, index) => (
                <div key={index} className="error-item">
                  第 {error.line} 行: {error.message}
                </div>
              ))}
            </div>
          )}
        </div>
      );
    };
    ```

<br />

## 優點

### 模組化設計

各知識源獨立開發和測試，系統具有良好的模組化特性。

### 靈活性

- 支援動態的問題解決策略

- 可以根據情況調整執行順序

- 容易添加新的知識源

### 可重用性

知識源可以在不同的問題領域中重複使用。

### 容錯性

單一知識源的失敗不會影響整個系統的運作。

### 透明性

所有中間結果都存儲在黑板上，便於除錯和分析。

<br />

## 缺點

### 效能開銷

頻繁的黑板讀寫和知識源調度可能造成效能問題。

### 複雜的控制策略

設計有效的控制策略需要深入理解問題領域。

### 除錯困難

非確定性的執行順序使得除錯變得複雜。

### 資料一致性

多個知識源同時修改黑板可能導致資料不一致。

### 記憶體消耗

黑板需要存儲大量的中間結果，可能消耗較多記憶體。

<br />

## 適用場景

### 適合使用

- 人工智慧系統：需要多種演算法協作的 AI 應用

- 專家系統：整合多個領域專家知識的系統

- 語音識別：需要聲學、語言學等多種處理的系統

- 影像處理：需要多階段處理的電腦視覺應用

- 協作系統：多個代理需要共享資訊的系統

- 增量式問題解決：解決方案需要逐步建構的問題

### 不適合使用

- 簡單的順序處理：有明確處理流程的應用

- 即時系統：對回應時間要求嚴格的系統

- 資源受限環境：記憶體或處理能力有限的環境

- 確定性需求：需要可預測執行結果的系統

<br />

## 實施建議

### 黑板設計

設計結構化的黑板資料模型，支援不同抽象層級的資料表示。

### 知識源開發

- 保持知識源的獨立性和專一性

- 實作清楚的執行條件判斷

- 提供適當的優先順序設定

### 控制策略

- 設計有效的調度演算法

- 考慮知識源之間的依賴關係

- 實作衝突解決機制

### 效能最佳化

- 使用事件驅動機制減少不必要的檢查

- 實作增量更新避免重複計算

- 考慮平行處理提升效能

### 測試策略

- 單獨測試各個知識源

- 測試不同的執行順序組合

- 驗證系統的收斂性

<br />

## 總結

Blackboard Architecture 提供了一個強大的框架來解決需要多種專業知識協作的複雜問題。透過共享的黑板和獨立的知識源，系統能夠靈活且有效處理不確定性高的問題領域。

雖然這種架構在控制複雜度和效能方面存在挑戰，但對於人工智慧、專家系統等需要探索性問題解決的應用來說，Blackboard Architecture 仍然是一個非常有價值的選擇。

關鍵在於根據具體的問題特性來設計適當的黑板結構、知識源和控制策略，並在系統複雜度和效能之間找到平衡點。
