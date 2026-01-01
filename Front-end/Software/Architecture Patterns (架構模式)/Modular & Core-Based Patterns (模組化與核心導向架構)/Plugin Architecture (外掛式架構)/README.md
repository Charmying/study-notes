# Plugin Architecture (外掛式架構)

Plugin Architecture (外掛式架構) 是一種軟體架構模式，允許應用程式透過外掛機制動態擴展功能，而無需修改核心系統。

這種架構將應用程式分為核心系統和外掛模組兩部分，核心系統提供基礎功能和外掛管理機制，外掛模組則實現特定功能，可以在執行時期動態載入或卸載。

<br />

## 動機

在軟體開發中，常見的問題包括

- 功能需求變化頻繁，核心系統需要不斷修改

- 不同客戶需要不同功能組合，難以維護多個版本

- 第三方開發者無法擴展應用程式功能

- 新功能開發影響核心系統穩定性

Plugin Architecture 通過模組化設計和動態載入機制，解決這些問題，讓系統具備

- 可擴展性：透過外掛動態添加新功能

- 可定制性：根據需求選擇性載入外掛

- 可維護性：外掛獨立開發和維護

- 穩定性：核心系統與外掛功能分離

<br />

## 結構

Plugin Architecture 主要由兩個核心元件構成

### 1. Core System (核心系統)

提供應用程式的基礎功能和外掛管理機制。

- 定義外掛介面和契約

- 管理外掛生命週期

- 提供外掛間通訊機制

- 處理外掛載入和卸載

### 2. Plugin Modules (外掛模組)

實現特定功能的獨立模組。

- 實現核心系統定義的介面

- 提供特定業務功能

- 可獨立開發和部署

- 支援動態載入和卸載

以下是 Plugin Architecture 的結構圖

```text
┌────────────────────────────────────────────────────┐
│                     Core System                    │
│  ┌───────────────────┐  ┌──────────────────────┐   │
│  │  Plugin Manager   │  │  Core Functionality  │   │
│  │                   │  │                      │   │
│  │  - Load/Unload    │  │  - Basic Features    │   │
│  │  - Lifecycle      │  │  - Plugin Interface  │   │
│  │  - Communication  │  │  - Event System      │   │
│  └───────────────────┘  └──────────────────────┘   │
└────────────────────────────────────────────────────┘
                        │
                        │ Plugin Interface
                        │
┌─────────────┬─────────────┬─────────────┬─────────────┐
│  Plugin A   │  Plugin B   │  Plugin C   │  Plugin D   │
│             │             │             │             │
│ - Feature A │ - Feature B │ - Feature C │ - Feature D │
│ - Config A  │ - Config B  │ - Config C  │ - Config C  │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

<br />

## 核心原則

### 介面分離原則 (Interface Segregation Principle)

外掛只需要實現所需的介面，避免依賴不必要的功能。

### 開放封閉原則 (Open-Closed Principle)

系統對擴展開放，對修改封閉，透過外掛添加新功能。

### 依賴反轉原則 (Dependency Inversion Principle)

核心系統依賴抽象介面，而非具體外掛實現。

<br />

## 實現方式

### Java 實現範例

以文字編輯器的外掛系統為例

- Core System (核心系統)

    ```java
    /** 外掛介面 */
    public interface EditorPlugin {
        String getName();
        String getVersion();
        void initialize(PluginContext context);
        void execute();
        void shutdown();
    }

    /** 外掛上下文 */
    public interface PluginContext {
        String getCurrentText();
        void setText(String text);
        void showMessage(String message);
        void registerMenuItem(String name, Runnable action);
    }

    /** 外掛管理器 */
    public class PluginManager {
        private final Map<String, EditorPlugin> plugins = new HashMap<>();
        private final PluginContext context;

        public PluginManager(PluginContext context) {
            this.context = context;
        }

        public void loadPlugin(String pluginPath) {
            try {
                URLClassLoader classLoader = new URLClassLoader(
                    new URL[]{new File(pluginPath).toURI().toURL()}
                );

                ServiceLoader<EditorPlugin> loader = ServiceLoader.load(
                    EditorPlugin.class, classLoader
                );

                for (EditorPlugin plugin : loader) {
                    plugin.initialize(context);
                    plugins.put(plugin.getName(), plugin);
                    System.out.println("載入外掛: " + plugin.getName());
                }
            } catch (Exception e) {
                System.err.println("載入外掛失敗: " + e.getMessage());
            }
        }

        public void unloadPlugin(String pluginName) {
            EditorPlugin plugin = plugins.remove(pluginName);
            if (plugin != null) {
                plugin.shutdown();
                System.out.println("卸載外掛: " + pluginName);
            }
        }

        public void executePlugin(String pluginName) {
            EditorPlugin plugin = plugins.get(pluginName);
            if (plugin != null) {
                plugin.execute();
            }
        }

        public List<EditorPlugin> getLoadedPlugins() {
            return new ArrayList<>(plugins.values());
        }
    }
    ```

- Plugin Implementation (外掛實現)

    ```java
    /** 文字統計外掛 */
    public class WordCountPlugin implements EditorPlugin {
        private PluginContext context;

        @Override
        public String getName() {
            return "Word Count";
        }

        @Override
        public String getVersion() {
            return "1.0.0";
        }

        @Override
        public void initialize(PluginContext context) {
            this.context = context;
            context.registerMenuItem("統計字數", this::execute);
        }

        @Override
        public void execute() {
            String text = context.getCurrentText();
            int wordCount = text.split("\\s+").length;
            int charCount = text.length();

            String message = String.format(
                "字數: %d\n字元數: %d", wordCount, charCount
            );
            context.showMessage(message);
        }

        @Override
        public void shutdown() {
            // 清理資源
        }
    }

    /** 文字轉換外掛 */
    public class TextTransformPlugin implements EditorPlugin {
        private PluginContext context;

        @Override
        public String getName() {
            return "Text Transform";
        }

        @Override
        public String getVersion() {
            return "1.0.0";
        }

        @Override
        public void initialize(PluginContext context) {
            this.context = context;
            context.registerMenuItem("轉大寫", this::toUpperCase);
            context.registerMenuItem("轉小寫", this::toLowerCase);
        }

        @Override
        public void execute() {
            // 預設執行轉大寫
            toUpperCase();
        }

        private void toUpperCase() {
            String text = context.getCurrentText();
            context.setText(text.toUpperCase());
        }

        private void toLowerCase() {
            String text = context.getCurrentText();
            context.setText(text.toLowerCase());
        }

        @Override
        public void shutdown() {
            // 清理資源
        }
    }
    ```

### TypeScript 與 Node.js 實現範例

- Core System (核心系統)

    ```typescript
    /** 外掛介面 */
    export interface Plugin {
      name: string;
      version: string;
      initialize(context: PluginContext): Promise<void>;
      execute(command: string, args?: any[]): Promise<any>;
      shutdown(): Promise<void>;
    }

    /** 外掛上下文 */
    export interface PluginContext {
      registerCommand(name: string, handler: CommandHandler): void;
      emitEvent(event: string, data?: any): void;
      onEvent(event: string, handler: EventHandler): void;
      getConfig(key: string): any;
      setConfig(key: string, value: any): void;
    }

    type CommandHandler = (args?: any[]) => Promise<any>;
    type EventHandler = (data?: any) => void;

    /** 外掛管理器 */
    export class PluginManager {
      private plugins = new Map<string, Plugin>();
      private commands = new Map<string, CommandHandler>();
      private eventHandlers = new Map<string, EventHandler[]>();
      private config = new Map<string, any>();

      private context: PluginContext = {
        registerCommand: (name, handler) => {
          this.commands.set(name, handler);
        },
        emitEvent: (event, data) => {
          const handlers = this.eventHandlers.get(event) || [];
          handlers.forEach(handler => handler(data));
        },
        onEvent: (event, handler) => {
          const handlers = this.eventHandlers.get(event) || [];
          handlers.push(handler);
          this.eventHandlers.set(event, handlers);
        },
        getConfig: (key) => this.config.get(key),
        setConfig: (key, value) => this.config.set(key, value)
      };

      async loadPlugin(pluginPath: string): Promise<void> {
        try {
          const pluginModule = await import(pluginPath);
          const plugin: Plugin = new pluginModule.default();

          await plugin.initialize(this.context);
          this.plugins.set(plugin.name, plugin);

          console.log(`載入外掛: ${plugin.name} v${plugin.version}`);
        } catch (error) {
          console.error(`載入外掛失敗: ${error.message}`);
        }
      }

      async unloadPlugin(pluginName: string): Promise<void> {
        const plugin = this.plugins.get(pluginName);
        if (plugin) {
          await plugin.shutdown();
          this.plugins.delete(pluginName);
          console.log(`卸載外掛: ${pluginName}`);
        }
      }

      async executeCommand(command: string, args?: any[]): Promise<any> {
        const handler = this.commands.get(command);
        if (handler) {
          return await handler(args);
        }
        throw new Error(`命令不存在: ${command}`);
      }

      getLoadedPlugins(): Plugin[] {
        return Array.from(this.plugins.values());
      }
    }
    ```

- Plugin Implementation (外掛實現)

    ```typescript
    /** 檔案操作外掛 */
    export default class FileOperationPlugin implements Plugin {
      name = 'File Operations';
      version = '1.0.0';
      private context!: PluginContext;

      async initialize(context: PluginContext): Promise<void> {
        this.context = context;

        context.registerCommand('file.read', this.readFile.bind(this));
        context.registerCommand('file.write', this.writeFile.bind(this));
        context.registerCommand('file.delete', this.deleteFile.bind(this));

        context.onEvent('app.startup', () => {
          console.log('檔案操作外掛已啟動');
        });
      }

      async execute(command: string, args?: any[]): Promise<any> {
        return await this.context.executeCommand(command, args);
      }

      private async readFile(args: any[]): Promise<string> {
        const [filePath] = args;
        const fs = await import('fs/promises');
        return await fs.readFile(filePath, 'utf-8');
      }

      private async writeFile(args: any[]): Promise<void> {
        const [filePath, content] = args;
        const fs = await import('fs/promises');
        await fs.writeFile(filePath, content, 'utf-8');
        this.context.emitEvent('file.written', { filePath, size: content.length });
      }

      private async deleteFile(args: any[]): Promise<void> {
        const [filePath] = args;
        const fs = await import('fs/promises');
        await fs.unlink(filePath);
        this.context.emitEvent('file.deleted', { filePath });
      }

      async shutdown(): Promise<void> {
        console.log('檔案操作外掛已關閉');
      }
    }

    /** HTTP 客戶端外掛 */
    export default class HttpClientPlugin implements Plugin {
      name = 'HTTP Client';
      version = '1.0.0';
      private context!: PluginContext;

      async initialize(context: PluginContext): Promise<void> {
        this.context = context;

        context.registerCommand('http.get', this.get.bind(this));
        context.registerCommand('http.post', this.post.bind(this));

        /** 設定預設配置 */
        context.setConfig('http.timeout', 5000);
        context.setConfig('http.retries', 3);
      }

      async execute(command: string, args?: any[]): Promise<any> {
        return await this.context.executeCommand(command, args);
      }

      private async get(args: any[]): Promise<any> {
        const [url, options = {}] = args;
        const timeout = this.context.getConfig('http.timeout');

        const response = await fetch(url, {
          method: 'GET',
          ...options,
          signal: AbortSignal.timeout(timeout)
        });

        return await response.json();
      }

      private async post(args: any[]): Promise<any> {
        const [url, data, options = {}] = args;
        const timeout = this.context.getConfig('http.timeout');

        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...options.headers
          },
          body: JSON.stringify(data),
          signal: AbortSignal.timeout(timeout)
        });

        return await response.json();
      }

      async shutdown(): Promise<void> {
        console.log('HTTP 客戶端外掛已關閉');
      }
    }
    ```

### React 前端實現範例

- Core System (核心系統)

    ```typescript
    /** 外掛介面 */
    export interface UIPlugin {
      name: string;
      version: string;
      component: React.ComponentType<any>;
      initialize(context: UIPluginContext): void;
      destroy(): void;
    }

    /** UI 外掛上下文 */
    export interface UIPluginContext {
      registerRoute(path: string, component: React.ComponentType): void;
      registerMenuItem(item: MenuItem): void;
      registerWidget(widget: Widget): void;
      emitEvent(event: string, data?: any): void;
      onEvent(event: string, handler: (data?: any) => void): void;
    }

    interface MenuItem {
      id: string;
      label: string;
      icon?: string;
      onClick: () => void;
    }

    interface Widget {
      id: string;
      title: string;
      component: React.ComponentType;
      position: 'sidebar' | 'header' | 'footer';
    }

    /** 外掛管理器 Hook */
    export const usePluginManager = () => {
      const [plugins, setPlugins] = useState<Map<string, UIPlugin>>(new Map());
      const [routes, setRoutes] = useState<Array<{path: string, component: React.ComponentType}>>([]);
      const [menuItems, setMenuItems] = useState<MenuItem[]>([]);
      const [widgets, setWidgets] = useState<Widget[]>([]);
      const [eventHandlers] = useState<Map<string, Array<(data?: any) => void>>>(new Map());

      const context: UIPluginContext = {
        registerRoute: (path, component) => {
          setRoutes(prev => [...prev, { path, component }]);
        },
        registerMenuItem: (item) => {
          setMenuItems(prev => [...prev, item]);
        },
        registerWidget: (widget) => {
          setWidgets(prev => [...prev, widget]);
        },
        emitEvent: (event, data) => {
          const handlers = eventHandlers.get(event) || [];
          handlers.forEach(handler => handler(data));
        },
        onEvent: (event, handler) => {
          const handlers = eventHandlers.get(event) || [];
          handlers.push(handler);
          eventHandlers.set(event, handlers);
        }
      };

      const loadPlugin = async (pluginFactory: () => UIPlugin) => {
        try {
          const plugin = pluginFactory();
          plugin.initialize(context);
          setPlugins(prev => new Map(prev).set(plugin.name, plugin));
          console.log(`載入 UI 外掛: ${plugin.name}`);
        } catch (error) {
          console.error(`載入 UI 外掛失敗:`, error);
        }
      };

      const unloadPlugin = (pluginName: string) => {
        const plugin = plugins.get(pluginName);
        if (plugin) {
          plugin.destroy();
          setPlugins(prev => {
            const newMap = new Map(prev);
            newMap.delete(pluginName);
            return newMap;
          });
          console.log(`卸載 UI 外掛: ${pluginName}`);
        }
      };

      return {
        plugins: Array.from(plugins.values()),
        routes,
        menuItems,
        widgets,
        loadPlugin,
        unloadPlugin,
        context
      };
    };
    ```

- Plugin Implementation (外掛實現)

    ```typescript
    /** 待辦事項外掛 */
    const TodoWidget: React.FC = () => {
      const [todos, setTodos] = useState<string[]>([]);
      const [newTodo, setNewTodo] = useState('');

      const addTodo = () => {
        if (newTodo.trim()) {
          setTodos(prev => [...prev, newTodo.trim()]);
          setNewTodo('');
        }
      };

      const removeTodo = (index: number) => {
        setTodos(prev => prev.filter((_, i) => i !== index));
      };

      return (
        <div className="todo-widget">
          <div className="todo-input">
            <input
              type="text"
              value={newTodo}
              onChange={(e) => setNewTodo(e.target.value)}
              placeholder="新增待辦事項"
              onKeyPress={(e) => e.key === 'Enter' && addTodo()}
            />
            <button onClick={addTodo}>新增</button>
          </div>
          <ul className="todo-list">
            {todos.map((todo, index) => (
              <li key={index}>
                <span>{todo}</span>
                <button onClick={() => removeTodo(index)}>刪除</button>
              </li>
            ))}
          </ul>
        </div>
      );
    };

    export const createTodoPlugin = (): UIPlugin => ({
      name: 'Todo Widget',
      version: '1.0.0',
      component: TodoWidget,
      initialize: (context) => {
        context.registerWidget({
          id: 'todo-widget',
          title: '待辦事項',
          component: TodoWidget,
          position: 'sidebar'
        });

        context.registerMenuItem({
          id: 'todo-menu',
          label: '待辦事項',
          onClick: () => {
            context.emitEvent('navigate', '/todos');
          }
        });
      },
      destroy: () => {
        console.log('待辦事項外掛已銷毀');
      }
    });

    /** 天氣外掛 */
    const WeatherWidget: React.FC = () => {
      const [weather, setWeather] = useState<{temp: number, condition: string} | null>(null);
      const [loading, setLoading] = useState(true);

      useEffect(() => {
        const fetchWeather = async () => {
          try {
            /** 模擬 API 呼叫 */
            await new Promise(resolve => setTimeout(resolve, 1000));
            setWeather({ temp: 25, condition: '晴天' });
          } catch (error) {
            console.error('取得天氣資訊失敗:', error);
          } finally {
            setLoading(false);
          }
        };

        fetchWeather();
      }, []);

      if (loading) {
        return <div className="weather-widget loading">載入中...</div>;
      }

      return (
        <div className="weather-widget">
          {weather ? (
            <>
              <div className="temperature">{weather.temp}°C</div>
              <div className="condition">{weather.condition}</div>
            </>
          ) : (
            <div className="error">無法取得天氣資訊</div>
          )}
        </div>
      );
    };

    export const createWeatherPlugin = (): UIPlugin => ({
      name: 'Weather Widget',
      version: '1.0.0',
      component: WeatherWidget,
      initialize: (context) => {
        context.registerWidget({
          id: 'weather-widget',
          title: '天氣',
          component: WeatherWidget,
          position: 'header'
        });
      },
      destroy: () => {
        console.log('天氣外掛已銷毀');
      }
    });
    ```

- Application Usage (應用程式使用)

    ```typescript
    /** 主應用程式 */
    const App: React.FC = () => {
      const {
        plugins,
        routes,
        menuItems,
        widgets,
        loadPlugin,
        unloadPlugin
      } = usePluginManager();

      useEffect(() => {
        /** 載入預設外掛 */
        loadPlugin(createTodoPlugin);
        loadPlugin(createWeatherPlugin);
      }, []);

      const sidebarWidgets = widgets.filter(w => w.position === 'sidebar');
      const headerWidgets = widgets.filter(w => w.position === 'header');

      return (
        <div className="app">
          <header className="app-header">
            <h1>外掛式應用程式</h1>
            <div className="header-widgets">
              {headerWidgets.map(widget => (
                <div key={widget.id} className="widget">
                  <h3>{widget.title}</h3>
                  <widget.component />
                </div>
              ))}
            </div>
          </header>

          <nav className="app-nav">
            {menuItems.map(item => (
              <button key={item.id} onClick={item.onClick}>
                {item.label}
              </button>
            ))}
          </nav>

          <div className="app-content">
            <main className="main-content">
              <Routes>
                {routes.map(route => (
                  <Route
                    key={route.path}
                    path={route.path}
                    element={<route.component />}
                  />
                ))}
                <Route path="/" element={<div>歡迎使用外掛式應用程式</div>} />
              </Routes>
            </main>

            <aside className="sidebar">
              {sidebarWidgets.map(widget => (
                <div key={widget.id} className="widget">
                  <h3>{widget.title}</h3>
                  <widget.component />
                </div>
              ))}
            </aside>
          </div>

          <div className="plugin-manager">
            <h3>已載入外掛</h3>
            <ul>
              {plugins.map(plugin => (
                <li key={plugin.name}>
                  {plugin.name} v{plugin.version}
                  <button onClick={() => unloadPlugin(plugin.name)}>卸載</button>
                </li>
              ))}
            </ul>
          </div>
        </div>
      );
    };
    ```

<br />

## 優點

### 可擴展性

透過外掛機制輕鬆添加新功能，無需修改核心系統。

### 可定制性

- 按需載入：根據需求選擇性載入外掛

- 配置靈活：每個外掛可獨立配置

- 版本管理：不同外掛可使用不同版本

### 可維護性

外掛與核心系統分離，便於獨立開發和維護。

### 生態系統

第三方開發者可以開發外掛，形成豐富的生態系統。

<br />

## 缺點

### 複雜性

需要設計完善的外掛介面和管理機制。

### 效能開銷

動態載入和外掛間通訊可能帶來效能損失。

### 相依性管理

外掛間的相依性和版本相容性問題。

### 安全性風險

外掛可能包含惡意程式碼或安全漏洞。

<br />

## 適用場景

### 適合使用

- 開發工具：IDE、編輯器、建置工具

- 內容管理系統：需要豐富外掛生態

- 瀏覽器：支援擴充功能

- 遊戲引擎：支援模組化開發

- 企業軟體：需要客製化功能

### 不適合使用

- 簡單應用：功能固定且簡單

- 效能敏感：對效能要求極高的系統

- 安全關鍵：對安全性要求極高的系統

- 嵌入式系統：資源受限的環境

<br />

## 實施建議

### 設計完善的外掛介面

定義清楚的外掛契約和生命週期管理。

### 建立外掛市場

提供外掛發現、安裝和更新機制。

### 安全性考量

實施外掛簽名驗證和沙盒執行環境。

### 效能監控

監控外掛效能影響，提供效能分析工具。

### 文件和範例

提供完整的外掛開發文件和範例程式碼。

<br />

## 總結

Plugin Architecture 提供了一個強大的擴展機制，特別適合需要高度可定制和可擴展的應用程式。雖然增加了系統複雜性，但能夠帶來極大的靈活性和可維護性。

關鍵在於設計良好的外掛介面和管理機制，平衡功能豐富性與系統複雜性。對於需要支援第三方擴展或頻繁功能變更的系統，Plugin Architecture 是一個優秀的選擇。
