# 4.4.1 Error Boundaries 簡介

<br />

## 基本概念

Error Boundaries 是 React 元件，用於捕獲子元件樹中發生的 JavaScript 錯誤，記錄錯誤並顯示備用 UI，而不是讓整個元件樹崩潰。

### 1. 基本 Error Boundary

```jsx
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    /** 更新狀態以顯示備用 UI */
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    /** 記錄錯誤資訊 */
    console.error('Error Boundary 捕獲錯誤：', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <h1>發生錯誤，請稍後再試。</h1>;
    }

    return this.props.children;
  }
}

/** 使用方式 */
function App() {
  return (
    <ErrorBoundary>
      <Header />
      <MainContent />
      <Footer />
    </ErrorBoundary>
  );
}
```

### 2. 詳細錯誤資訊顯示

```jsx
class DetailedErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null
    };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    });

    /** 錯誤報告服務 */
    this.reportError(error, errorInfo);
  }

  reportError = (error, errorInfo) => {
    /** 發送錯誤報告到監控服務 */
    console.error('錯誤報告：', {
      message: error.message,
      stack: error.stack,
      componentStack: errorInfo.componentStack,
      timestamp: new Date().toISOString()
    });
  };

  handleRetry = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null
    });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <h2>應用程式發生錯誤</h2>
          <p>很抱歉，發生了意外錯誤。</p>

          <button onClick={this.handleRetry}>
            重試
          </button>

          {process.env.NODE_ENV === 'development' && (
            <details style={{ whiteSpace: 'pre-wrap', marginTop: '20px' }}>
              <summary>錯誤詳情 (開發模式)</summary>
              <p><strong>錯誤訊息：</strong></p>
              <pre>{this.state.error && this.state.error.toString()}</pre>

              <p><strong>元件堆疊：</strong></p>
              <pre>{this.state.errorInfo.componentStack}</pre>

              <p><strong>錯誤堆疊：</strong></p>
              <pre>{this.state.error && this.state.error.stack}</pre>
            </details>
          )}
        </div>
      );
    }

    return this.props.children;
  }
}
```

<br />

## 函式元件版本 (使用 Hook)

### 1. 自定義 Hook 實作

```jsx
function useErrorHandler() {
  const [error, setError] = useState(null);

  const resetError = () => setError(null);

  const captureError = useCallback((error, errorInfo) => {
    setError({ error, errorInfo });
    console.error('錯誤捕獲：', error, errorInfo);
  }, []);

  useEffect(() => {
    if (error) {
      /** 錯誤報告 */
      console.error('應用程式錯誤：', error);
    }
  }, [error]);

  return { error, resetError, captureError };
}

function ErrorBoundaryWrapper({ children, fallback }) {
  const { error, resetError } = useErrorHandler();

  if (error) {
    return fallback ? fallback(error, resetError) : (
      <div>
        <h2>發生錯誤</h2>
        <button onClick={resetError}>重試</button>
      </div>
    );
  }

  return children;
}
```

### 2. React Error Boundary Hook (第三方)

```jsx
import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div role="alert" className="error-fallback">
      <h2>發生錯誤</h2>
      <p>錯誤訊息：{error.message}</p>
      <button onClick={resetErrorBoundary}>
        重試
      </button>
    </div>
  );
}

function App() {
  const handleError = (error, errorInfo) => {
    console.error('Error Boundary 錯誤：', error, errorInfo);
  };

  return (
    <ErrorBoundary
      FallbackComponent={ErrorFallback}
      onError={handleError}
      onReset={() => window.location.reload()}
    >
      <MainApp />
    </ErrorBoundary>
  );
}
```

<br />

## 錯誤類型與處理

### 1. 渲染錯誤處理

```jsx
function ProblematicComponent({ data }) {
  /** 模擬可能出錯的渲染 */
  if (!data) {
    throw new Error('資料不能為空');
  }

  if (data.type === 'error') {
    throw new Error('模擬渲染錯誤');
  }

  return (
    <div>
      <h3>{data.title}</h3>
      <p>{data.content}</p>
    </div>
  );
}

function SafeComponent({ data }) {
  return (
    <ErrorBoundary>
      <ProblematicComponent data={data} />
    </ErrorBoundary>
  );
}

function App() {
  const [testData, setTestData] = useState({ title: '正常資料', content: '內容' });

  const triggerError = () => {
    setTestData({ type: 'error' });
  };

  const triggerNullError = () => {
    setTestData(null);
  };

  const resetData = () => {
    setTestData({ title: '正常資料', content: '內容' });
  };

  return (
    <div>
      <div>
        <button onClick={triggerError}>觸發渲染錯誤</button>
        <button onClick={triggerNullError}>觸發空資料錯誤</button>
        <button onClick={resetData}>重設資料</button>
      </div>

      <SafeComponent data={testData} />
    </div>
  );
}
```

### 2. 非同步錯誤處理

```jsx
class AsyncErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('非同步錯誤：', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div>
          <h3>載入失敗</h3>
          <p>錯誤：{this.state.error?.message}</p>
          <button onClick={() => this.setState({ hasError: false, error: null })}>
            重試
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

function AsyncComponent() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      /** 模擬 API 呼叫 */
      const response = await fetch('/api/data');
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      const result = await response.json();
      setData(result);
    } catch (error) {
      /** 對於非同步錯誤，需要手動拋出到 Error Boundary */
      throw error;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) return <div>載入中...</div>;

  return (
    <div>
      <h3>非同步資料</h3>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
```

<br />

## 多層 Error Boundary

### 1. 分層錯誤處理

```jsx
/** 應用程式層級 Error Boundary */
class AppErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('應用程式層級錯誤：', error, errorInfo);
    /** 發送到錯誤監控服務 */
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="app-error">
          <h1>應用程式發生嚴重錯誤</h1>
          <p>請重新整理頁面或聯絡技術支援。</p>
          <button onClick={() => window.location.reload()}>
            重新整理頁面
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

/** 功能層級 Error Boundary */
class FeatureErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error(`${this.props.feature} 功能錯誤：`, error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="feature-error">
          <h3>{this.props.feature} 功能暫時無法使用</h3>
          <p>請稍後再試或使用其他功能。</p>
          <button onClick={() => this.setState({ hasError: false })}>
            重試
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

/** 元件層級 Error Boundary */
class ComponentErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="component-error">
          <p>此元件載入失敗</p>
        </div>
      );
    }

    return this.props.children;
  }
}

/** 應用程式結構 */
function App() {
  return (
    <AppErrorBoundary>
      <Header />

      <main>
        <FeatureErrorBoundary feature="使用者管理">
          <ComponentErrorBoundary>
            <UserManagement />
          </ComponentErrorBoundary>
        </FeatureErrorBoundary>

        <FeatureErrorBoundary feature="產品目錄">
          <ComponentErrorBoundary>
            <ProductCatalog />
          </ComponentErrorBoundary>
        </FeatureErrorBoundary>
      </main>

      <Footer />
    </AppErrorBoundary>
  );
}
```

### 2. 條件式 Error Boundary

```jsx
function ConditionalErrorBoundary({ 
  children, 
  enabled = true, 
  fallback,
  onError 
}) {
  if (!enabled) {
    return children;
  }

  return (
    <ErrorBoundary
      FallbackComponent={fallback}
      onError={onError}
    >
      {children}
    </ErrorBoundary>
  );
}

function App() {
  const [errorBoundaryEnabled, setErrorBoundaryEnabled] = useState(true);
  const [debugMode, setDebugMode] = useState(false);

  const customFallback = ({ error, resetErrorBoundary }) => (
    <div>
      <h3>功能暫時無法使用</h3>
      {debugMode && <p>錯誤：{error.message}</p>}
      <button onClick={resetErrorBoundary}>重試</button>
    </div>
  );

  return (
    <div>
      <div>
        <label>
          <input
            type="checkbox"
            checked={errorBoundaryEnabled}
            onChange={(e) => setErrorBoundaryEnabled(e.target.checked)}
          />
          啟用 Error Boundary
        </label>

        <label>
          <input
            type="checkbox"
            checked={debugMode}
            onChange={(e) => setDebugMode(e.target.checked)}
          />
          除錯模式
        </label>
      </div>

      <ConditionalErrorBoundary
        enabled={errorBoundaryEnabled}
        fallback={customFallback}
        onError={(error, errorInfo) => {
          console.error('條件式錯誤邊界：', error, errorInfo);
        }}
      >
        <MainContent />
      </ConditionalErrorBoundary>
    </div>
  );
}
```

<br />

## 錯誤報告與監控

### 1. 錯誤資訊收集

```jsx
class MonitoringErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    const errorReport = {
      message: error.message,
      stack: error.stack,
      componentStack: errorInfo.componentStack,
      timestamp: new Date().toISOString(),
      userAgent: navigator.userAgent,
      url: window.location.href,
      userId: this.props.userId,
      sessionId: this.props.sessionId,
      buildVersion: process.env.REACT_APP_VERSION
    };

    this.sendErrorReport(errorReport);
  }

  sendErrorReport = async (errorReport) => {
    try {
      await fetch('/api/errors', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(errorReport)
      });
    } catch (reportError) {
      console.error('錯誤報告發送失敗：', reportError);
    }
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <h2>發生錯誤</h2>
          <p>錯誤已自動回報，會盡快修復。</p>
          <button onClick={() => this.setState({ hasError: false })}>
            重試
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

### 2. 錯誤統計與分析

```jsx
class AnalyticsErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
      hasError: false,
      errorCount: 0,
      lastError: null
    };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState(prev => ({
      errorCount: prev.errorCount + 1,
      lastError: {
        error: error.message,
        timestamp: new Date().toISOString()
      }
    }));

    /** 錯誤分類 */
    const errorCategory = this.categorizeError(error);

    /** 發送分析資料 */
    this.trackError(error, errorInfo, errorCategory);
  }

  categorizeError = (error) => {
    if (error.message.includes('Network')) return 'network';
    if (error.message.includes('Permission')) return 'permission';
    if (error.message.includes('Timeout')) return 'timeout';
    return 'unknown';
  };

  trackError = (error, errorInfo, category) => {
    /** 發送到分析服務 */
    if (window.gtag) {
      window.gtag('event', 'exception', {
        description: error.message,
        fatal: false,
        custom_map: {
          category: category,
          component_stack: errorInfo.componentStack
        }
      });
    }
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <h2>發生錯誤</h2>
          <p>錯誤次數：{this.state.errorCount}</p>
          {this.state.lastError && (
            <p>最後錯誤：{this.state.lastError.timestamp}</p>
          )}
          <button onClick={() => this.setState({ hasError: false })}>
            重試
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

<br />

## Error Boundary 限制

### 1. 無法捕獲的錯誤類型

```jsx
function ErrorBoundaryLimitations() {
  const [asyncError, setAsyncError] = useState(null);

  /** Error Boundary 無法捕獲的錯誤類型 */

  /** 1. 事件處理器中的錯誤 */
  const handleClick = () => {
    try {
      throw new Error('事件處理器錯誤');
    } catch (error) {
      console.error('事件錯誤需要手動處理：', error);
      setAsyncError(error.message);
    }
  };

  /** 2. 非同步程式碼錯誤 */
  const handleAsyncError = async () => {
    try {
      await new Promise((resolve, reject) => {
        setTimeout(() => reject(new Error('非同步錯誤')), 1000);
      });
    } catch (error) {
      console.error('非同步錯誤需要手動處理：', error);
      setAsyncError(error.message);
    }
  };

  /** 3. setTimeout/setInterval 錯誤 */
  const handleTimerError = () => {
    setTimeout(() => {
      try {
        throw new Error('定時器錯誤');
      } catch (error) {
        console.error('定時器錯誤需要手動處理：', error);
        setAsyncError(error.message);
      }
    }, 1000);
  };

  return (
    <div>
      <h3>Error Boundary 限制示例</h3>

      <button onClick={handleClick}>
        觸發事件處理器錯誤
      </button>

      <button onClick={handleAsyncError}>
        觸發非同步錯誤
      </button>

      <button onClick={handleTimerError}>
        觸發定時器錯誤
      </button>

      {asyncError && (
        <div className="error-message">
          手動捕獲的錯誤：{asyncError}
          <button onClick={() => setAsyncError(null)}>清除</button>
        </div>
      )}
    </div>
  );
}
```

<br />

## 最佳實務

### 1. Error Boundary 放置策略

- 應用程式根部：捕獲全域錯誤

- 路由層級：防止單一頁面錯誤影響整個應用

- 功能模組：隔離不同功能的錯誤

- 關鍵元件：保護重要的業務元件

### 2. 錯誤處理原則

- 優雅降級：提供有意義的備用 UI

- 錯誤報告：收集錯誤資訊用於修復

- 使用者體驗：避免白屏或應用崩潰

- 開發除錯：開發環境顯示詳細錯誤資訊

### 3. 錯誤邊界設計

- 分層處理：不同層級處理不同類型的錯誤

- 重試機制：允許使用者重試失敗的操作

- 錯誤分類：根據錯誤類型提供不同的處理方式

- 監控整合：與錯誤監控服務整合

### 4. 開發與生產環境

- 開發環境：顯示詳細錯誤資訊便於除錯

- 生產環境：顯示使用者友善的錯誤訊息

- 錯誤記錄：生產環境記錄完整錯誤資訊

- 效能影響：避免錯誤處理影響應用效能
