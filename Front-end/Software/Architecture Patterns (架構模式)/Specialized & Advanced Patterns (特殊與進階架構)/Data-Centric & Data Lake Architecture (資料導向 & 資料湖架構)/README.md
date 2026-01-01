# Data-Centric & Data Lake Architecture (資料導向 & 資料湖架構)

Data-Centric & Data Lake Architecture (資料導向 & 資料湖架構) 是一種以資料為核心的架構模式，將原始資料以自然格式儲存在中央儲存庫中，支援多種資料處理和分析需求。

這種架構強調資料的靈活性和可擴展性，允許組織儲存大量結構化、半結構化和非結構化資料，並根據需要進行處理和分析。

<br />

## 動機

在現代資料驅動的環境中，組織面臨的挑戰包括

- 資料來源多樣化，包含結構化、半結構化和非結構化資料

- 傳統資料倉儲無法有效處理大量異質資料

- 資料處理需求多樣，從批次處理到即時分析

- 資料儲存成本高昂，且擴展性有限

Data Lake Architecture 通過集中式資料儲存和靈活的處理框架，解決這些問題，讓組織能夠

- 彈性儲存：支援各種格式的資料儲存

- 成本效益：使用低成本的儲存解決方案

- 可擴展性：水平擴展以處理大量資料

- 敏捷分析：快速適應新的分析需求

<br />

## 結構

Data Lake Architecture 採用分層結構，從資料攝取到資料消費分為多個層次

### 1. Data Sources (資料來源層)

各種資料來源的集合點。

- 結構化資料：關聯式資料庫、ERP 系統

- 半結構化資料：JSON、XML、日誌檔案

- 非結構化資料：影像、影片、文件

- 串流資料：IoT 感測器、點擊流

### 2. Data Ingestion (資料攝取層)

負責將資料從來源系統移動到資料湖。

- 批次攝取：定期批量處理

- 即時攝取：串流資料處理

- 資料驗證和品質檢查

- 元資料管理

### 3. Data Storage (資料儲存層)

中央資料儲存庫，以原始格式保存資料。

- 原始資料區：未處理的原始資料

- 處理資料區：清理和轉換後的資料

- 策劃資料區：業務就緒的資料

- 歸檔資料區：長期保存的歷史資料

### 4. Data Processing (資料處理層)

對儲存的資料進行各種處理和轉換。

- ETL/ELT 處理：資料轉換和載入

- 機器學習：模型訓練和推論

- 資料品質管理：清理和驗證

- 資料治理：政策和合規性

### 5. Data Access (資料存取層)

提供多種方式存取和分析資料。

- 分析工具：BI 工具、報表系統

- API 服務：程式化資料存取

- 查詢引擎：SQL 和 NoSQL 查詢

- 視覺化工具：儀表板和圖表

以下是 Data Lake Architecture 的層次圖

```text
┌───────────────────────────────────────────────────────────┐
│                    Data Access Layer                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐  │
│  │  BI Tools   │ │     API     │ │    Visualization    │  │
│  └─────────────┘ └─────────────┘ └─────────────────────┘  │
└───────────────────────────────────────────────────────────┘
┌───────────────────────────────────────────────────────────┐
│                  Data Processing Layer                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐  │
│  │   ETL/ELT   │ │ ML Pipeline │ │    Data Quality     │  │
│  └─────────────┘ └─────────────┘ └─────────────────────┘  │
└───────────────────────────────────────────────────────────┘
┌───────────────────────────────────────────────────────────┐
│                    Data Storage Layer                     │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐  │
│  │  Raw Data   │ │  Processed  │ │    Curated Data     │  │
│  └─────────────┘ └─────────────┘ └─────────────────────┘  │
└───────────────────────────────────────────────────────────┘
┌───────────────────────────────────────────────────────────┐
│                   Data Ingestion Layer                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐  │
│  │    Batch    │ │  Streaming  │ │    Metadata Mgmt    │  │
│  └─────────────┘ └─────────────┘ └─────────────────────┘  │
└───────────────────────────────────────────────────────────┘
┌───────────────────────────────────────────────────────────┐
│                       Data Sources                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐  │
│  │  Databases  │ │    Files    │ │   Streaming Data    │  │
│  └─────────────┘ └─────────────┘ └─────────────────────┘  │
└───────────────────────────────────────────────────────────┘
```

<br />

## 核心原則

### Schema-on-Read (讀取時定義結構)

資料以原始格式儲存，在讀取時才定義結構和格式。

### 資料不可變性 (Data Immutability)

原始資料保持不變，所有轉換都產生新的資料集。

### 彈性儲存 (Flexible Storage)

支援各種資料格式和結構，不需要預先定義 schema。

### 水平擴展 (Horizontal Scaling)

通過增加節點來擴展儲存和處理能力。

<br />

## 實現方式

### AWS 實現範例

以電商平台的資料湖為例

- 資料攝取層

    ```python
    import boto3
    import json
    from datetime import datetime

    class DataIngestionService:
        def __init__(self):
            self.s3_client = boto3.client('s3')
            self.kinesis_client = boto3.client('kinesis')
            self.bucket_name = 'ecommerce-data-lake'

        def ingest_batch_data(self, data_source, data):
            """批次資料攝取"""
            timestamp = datetime.now().strftime('%Y/%m/%d/%H')
            key = f"raw/{data_source}/{timestamp}/data.json"

            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=json.dumps(data),
                Metadata={
                    'source': data_source,
                    'ingestion_time': datetime.now().isoformat(),
                    'data_type': 'batch'
                }
            )

        def ingest_streaming_data(self, stream_name, data):
            """串流資料攝取"""
            self.kinesis_client.put_record(
                StreamName=stream_name,
                Data=json.dumps(data),
                PartitionKey=str(data.get('user_id', 'default'))
            )

        def validate_data_quality(self, data, schema):
            """資料品質驗證"""
            required_fields = schema.get('required_fields', [])

            for field in required_fields:
                if field not in data:
                    raise ValueError(f"缺少必要欄位: {field}")

            return True
    ```
- 資料處理層

    ```python
    import pandas as pd
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col, when, isnan, count

    class DataProcessingService:
        def __init__(self):
            self.spark = SparkSession.builder \
                .appName("DataLakeProcessing") \
                .getOrCreate()

        def clean_customer_data(self, input_path, output_path):
            """清理客戶資料"""
            df = self.spark.read.json(input_path)

            # 移除重複資料
            df_clean = df.dropDuplicates(['customer_id'])

            # 處理缺失值
            df_clean = df_clean.fillna({
                'phone': 'unknown',
                'address': 'unknown'
            })

            # 資料驗證
            df_clean = df_clean.filter(
                col('email').rlike(r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$')
            )

            # 儲存處理後的資料
            df_clean.write.mode('overwrite').parquet(output_path)

        def aggregate_sales_data(self, input_path, output_path):
            """聚合銷售資料"""
            df = self.spark.read.parquet(input_path)

            # 按日期和產品聚合
            daily_sales = df.groupBy('date', 'product_id') \
                .agg({
                    'quantity': 'sum',
                    'revenue': 'sum',
                    'order_id': 'countDistinct'
                }) \
                .withColumnRenamed('sum(quantity)', 'total_quantity') \
                .withColumnRenamed('sum(revenue)', 'total_revenue') \
                .withColumnRenamed('count(DISTINCT order_id)', 'order_count')

            daily_sales.write.mode('overwrite').parquet(output_path)

        def generate_data_quality_report(self, data_path):
            """產生資料品質報告"""
            df = self.spark.read.parquet(data_path)

            quality_metrics = {}

            for column in df.columns:
                null_count = df.filter(col(column).isNull()).count()
                total_count = df.count()

                quality_metrics[column] = {
                    'null_percentage': (null_count / total_count) * 100,
                    'completeness': ((total_count - null_count) / total_count) * 100
                }

            return quality_metrics
    ```

- 資料存取層

    ```python
    from flask import Flask, jsonify, request
    import boto3
    from pyspark.sql import SparkSession

    class DataAccessAPI:
        def __init__(self):
            self.app = Flask(__name__)
            self.spark = SparkSession.builder \
                .appName("DataLakeAPI") \
                .getOrCreate()
            self.s3_client = boto3.client('s3')
            self.setup_routes()

        def setup_routes(self):
            @self.app.route('/api/customers/<customer_id>', methods=['GET'])
            def get_customer(customer_id):
                try:
                    df = self.spark.read.parquet('s3://data-lake/curated/customers/')
                    customer = df.filter(col('customer_id') == customer_id).collect()

                    if customer:
                        return jsonify(customer[0].asDict())
                    else:
                        return jsonify({'error': '客戶不存在'}), 404

                except Exception as e:
                    return jsonify({'error': str(e)}), 500

            @self.app.route('/api/sales/summary', methods=['GET'])
            def get_sales_summary():
                try:
                    start_date = request.args.get('start_date')
                    end_date = request.args.get('end_date')

                    df = self.spark.read.parquet('s3://data-lake/curated/sales/')

                    if start_date and end_date:
                        df = df.filter(
                            (col('date') >= start_date) & 
                            (col('date') <= end_date)
                        )

                    summary = df.agg({
                        'total_revenue': 'sum',
                        'total_quantity': 'sum',
                        'order_count': 'sum'
                    }).collect()[0]

                    return jsonify(summary.asDict())

                except Exception as e:
                    return jsonify({'error': str(e)}), 500

        def run(self, host='0.0.0.0', port=5000):
            self.app.run(host=host, port=port)
    ```

### Apache Spark 實現範例

- 資料處理管道

    ```scala
    import org.apache.spark.sql.{SparkSession, DataFrame}
    import org.apache.spark.sql.functions._
    import org.apache.spark.sql.types._

    class DataLakePipeline {
      val spark: SparkSession = SparkSession.builder()
        .appName("DataLakePipeline")
        .getOrCreate()

      import spark.implicits._

      def processUserEvents(inputPath: String, outputPath: String): Unit = {
        /** 讀取原始事件資料 */
        val rawEvents = spark.read
          .option("multiline", "true")
          .json(inputPath)

        /** 資料清理和轉換 */
        val cleanEvents = rawEvents
          .filter($"event_type".isNotNull)
          .filter($"user_id".isNotNull)
          .withColumn("processed_at", current_timestamp())
          .withColumn("event_date", to_date($"timestamp"))

        /** 按事件類型分割資料 */
        val pageViews = cleanEvents.filter($"event_type" === "page_view")
        val purchases = cleanEvents.filter($"event_type" === "purchase")
        val clicks = cleanEvents.filter($"event_type" === "click")

        /** 儲存分割後的資料 */
        pageViews.write
          .mode("append")
          .partitionBy("event_date")
          .parquet(s"$outputPath/page_views")

        purchases.write
          .mode("append")
          .partitionBy("event_date")
          .parquet(s"$outputPath/purchases")

        clicks.write
          .mode("append")
          .partitionBy("event_date")
          .parquet(s"$outputPath/clicks")
      }

      def generateUserSegments(inputPath: String, outputPath: String): Unit = {
        val userEvents = spark.read.parquet(inputPath)

        /** 計算使用者行為指標 */
        val userMetrics = userEvents
          .groupBy("user_id")
          .agg(
            count("*").as("total_events"),
            countDistinct("session_id").as("session_count"),
            sum(when($"event_type" === "purchase", $"amount").otherwise(0)).as("total_spent"),
            max("timestamp").as("last_activity")
          )

        /** 使用者分群 */
        val userSegments = userMetrics
          .withColumn("segment",
            when($"total_spent" > 1000 and $"session_count" > 10, "high_value")
              .when($"total_spent" > 100 and $"session_count" > 5, "medium_value")
              .otherwise("low_value")
          )

        userSegments.write
          .mode("overwrite")
          .parquet(outputPath)
      }

      def createDataMart(inputPath: String, outputPath: String): Unit = {
        val events = spark.read.parquet(inputPath)

        /** 建立日銷售摘要 */
        val dailySales = events
          .filter($"event_type" === "purchase")
          .groupBy("event_date", "product_category")
          .agg(
            sum("amount").as("daily_revenue"),
            count("*").as("transaction_count"),
            countDistinct("user_id").as("unique_customers")
          )

        dailySales.write
          .mode("overwrite")
          .partitionBy("event_date")
          .parquet(s"$outputPath/daily_sales")
      }
    }
    ```

### TypeScript 與 Node.js 實現範例

- 資料攝取服務

    ```typescript
    import { S3 } from 'aws-sdk';
    import { Kafka, Producer } from 'kafkajs';

    interface DataIngestionConfig {
      s3Bucket: string;
      kafkaBootstrapServers: string[];
    }

    export class DataIngestionService {
      private s3: S3;
      private kafkaProducer: Producer;

      constructor(private config: DataIngestionConfig) {
        this.s3 = new S3();

        const kafka = new Kafka({
          clientId: 'data-lake-ingestion',
          brokers: config.kafkaBootstrapServers
        });

        this.kafkaProducer = kafka.producer();
      }

      async ingestBatchData(source: string, data: any[]): Promise<void> {
        const timestamp = new Date().toISOString().slice(0, 13).replace(/[-T:]/g, '/');
        const key = `raw/${source}/${timestamp}/batch-${Date.now()}.json`;

        await this.s3.putObject({
          Bucket: this.config.s3Bucket,
          Key: key,
          Body: JSON.stringify(data),
          ContentType: 'application/json',
          Metadata: {
            source,
            ingestionTime: new Date().toISOString(),
            recordCount: data.length.toString()
          }
        }).promise();
      }

      async ingestStreamingData(topic: string, data: any): Promise<void> {
        await this.kafkaProducer.send({
          topic,
          messages: [{
            key: data.id || Date.now().toString(),
            value: JSON.stringify({
              ...data,
              ingestionTimestamp: new Date().toISOString()
            })
          }]
        });
      }

      async validateDataSchema(data: any, schema: any): Promise<boolean> {
        /** 簡單的 schema 驗證 */
        for (const field of schema.required || []) {
          if (!(field in data)) {
            throw new Error(`缺少必要欄位: ${field}`);
          }
        }

        for (const [field, type] of Object.entries(schema.properties || {})) {
          if (field in data && typeof data[field] !== type) {
            throw new Error(`欄位 ${field} 類型錯誤，期望 ${type}`);
          }
        }

        return true;
      }
    }
    ```

- 資料查詢服務

    ```typescript
    import { Athena, S3 } from 'aws-sdk';

    interface QueryResult {
      columns: string[];
      rows: any[][];
      executionTime: number;
    }

    export class DataQueryService {
      private athena: Athena;
      private s3: S3;

      constructor(
        private outputBucket: string,
        private database: string = 'data_lake_db'
      ) {
        this.athena = new Athena();
        this.s3 = new S3();
      }

      async executeQuery(sql: string): Promise<QueryResult> {
        const startTime = Date.now();

        /** 開始查詢執行 */
        const execution = await this.athena.startQueryExecution({
          QueryString: sql,
          QueryExecutionContext: {
            Database: this.database
          },
          ResultConfiguration: {
            OutputLocation: `s3://${this.outputBucket}/query-results/`
          }
        }).promise();

        const executionId = execution.QueryExecutionId!;

        /** 等待查詢完成 */
        await this.waitForQueryCompletion(executionId);

        /** 取得查詢結果 */
        const results = await this.athena.getQueryResults({
          QueryExecutionId: executionId
        }).promise();

        const executionTime = Date.now() - startTime;

        return this.formatResults(results, executionTime);
      }

      private async waitForQueryCompletion(executionId: string): Promise<void> {
        while (true) {
          const status = await this.athena.getQueryExecution({
            QueryExecutionId: executionId
          }).promise();

          const state = status.QueryExecution?.Status?.State;

          if (state === 'SUCCEEDED') {
            break;
          } else if (state === 'FAILED' || state === 'CANCELLED') {
            throw new Error(`查詢失敗: ${status.QueryExecution?.Status?.StateChangeReason}`);
          }

          await new Promise(resolve => setTimeout(resolve, 1000));
        }
      }

      private formatResults(results: any, executionTime: number): QueryResult {
        const resultSet = results.ResultSet;
        const rows = resultSet.Rows || [];

        if (rows.length === 0) {
          return { columns: [], rows: [], executionTime };
        }

        /** 第一行是欄位名稱 */
        const columns = rows[0].Data.map((col: any) => col.VarCharValue || '');

        /** 其餘行是資料 */
        const dataRows = rows.slice(1).map((row: any) => 
          row.Data.map((cell: any) => cell.VarCharValue || null)
        );

        return {
          columns,
          rows: dataRows,
          executionTime
        };
      }

      async getTableMetadata(tableName: string): Promise<any> {
        const sql = `DESCRIBE ${tableName}`;
        return await this.executeQuery(sql);
      }

      async getDataCatalog(): Promise<string[]> {
        const sql = 'SHOW TABLES';
        const result = await this.executeQuery(sql);
        return result.rows.map(row => row[0]);
      }
    }
    ```

### React 前端實現範例

- 資料視覺化元件

    ```typescript
    import React, { useState, useEffect } from 'react';
    import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

    interface DataPoint {
      date: string;
      revenue: number;
      orders: number;
    }

    interface DataLakeDashboardProps {
      dataQueryService: DataQueryService;
    }

    export const DataLakeDashboard: React.FC<DataLakeDashboardProps> = ({ 
      dataQueryService 
    }) => {
      const [salesData, setSalesData] = useState<DataPoint[]>([]);
      const [loading, setLoading] = useState(false);
      const [dateRange, setDateRange] = useState({
        startDate: '2024-01-01',
        endDate: '2024-12-31'
      });

      useEffect(() => {
        loadSalesData();
      }, [dateRange]);

      const loadSalesData = async () => {
        setLoading(true);
        try {
          const sql = `
            SELECT 
              date_format(order_date, '%Y-%m-%d') as date,
              SUM(total_amount) as revenue,
              COUNT(*) as orders
            FROM curated_sales 
            WHERE order_date BETWEEN '${dateRange.startDate}' AND '${dateRange.endDate}'
            GROUP BY date_format(order_date, '%Y-%m-%d')
            ORDER BY date
          `;

          const result = await dataQueryService.executeQuery(sql);

          const formattedData = result.rows.map(row => ({
            date: row[0],
            revenue: parseFloat(row[1]) || 0,
            orders: parseInt(row[2]) || 0
          }));

          setSalesData(formattedData);
        } catch (error) {
          console.error('載入銷售資料失敗:', error);
        } finally {
          setLoading(false);
        }
      };

      const handleDateRangeChange = (field: 'startDate' | 'endDate', value: string) => {
        setDateRange(prev => ({ ...prev, [field]: value }));
      };

      return (
        <div className="data-lake-dashboard">
          <h2>資料湖儀表板</h2>

          <div className="date-range-selector">
            <label>
              開始日期:
              <input
                type="date"
                value={dateRange.startDate}
                onChange={(e) => handleDateRangeChange('startDate', e.target.value)}
              />
            </label>
            <label>
              結束日期:
              <input
                type="date"
                value={dateRange.endDate}
                onChange={(e) => handleDateRangeChange('endDate', e.target.value)}
              />
            </label>
          </div>

          {loading ? (
            <div className="loading">載入中...</div>
          ) : (
            <div className="charts-container">
              <div className="chart">
                <h3>每日營收趨勢</h3>
                <LineChart width={800} height={300} data={salesData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="revenue" stroke="#8884d8" />
                </LineChart>
              </div>

              <div className="chart">
                <h3>每日訂單數量</h3>
                <LineChart width={800} height={300} data={salesData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="orders" stroke="#82ca9d" />
                </LineChart>
              </div>
            </div>
          )}
        </div>
      );
    };
    ```

<br />

## 優點

### 彈性儲存

支援各種資料格式，無需預先定義結構，適應不斷變化的資料需求。

### 成本效益

- 低成本儲存：使用物件儲存降低成本

- 按需計算：只在需要時進行資料處理

- 資源最佳化：根據工作負載動態調整資源

### 可擴展性

水平擴展能力，可以處理 PB 級別的資料量。

### 敏捷分析

快速適應新的分析需求，支援多種分析工具和框架。

### 資料民主化

讓更多使用者能夠存取和分析資料，促進資料驅動決策。

<br />

## 缺點

### 資料治理挑戰

缺乏結構可能導致資料品質問題和治理困難。

### 效能考量

查詢效能可能不如傳統資料倉儲，特別是複雜的分析查詢。

### 技能要求

需要專業的資料工程和分析技能。

### 安全性複雜度

大量異質資料的安全管理更加複雜。

### 資料沼澤風險

若管理不當，可能變成難以使用的「資料沼澤」。

<br />

## 適用場景

### 適合使用

- 大資料分析：需要處理大量多樣化資料

- 機器學習：需要大量訓練資料的 ML 專案

- IoT 應用：處理大量感測器資料

- 即時分析：需要即時處理串流資料

- 資料探索：需要靈活探索未知資料模式

### 不適合使用

- 簡單報表：只需要基本報表功能

- 即時交易：需要低延遲的交易處理

- 小資料量：資料量小且結構固定

- 嚴格合規：需要嚴格資料治理的環境

<br />

## 實施建議

### 資料治理策略

建立清晰的資料分類、標記和生命週期管理政策。

### 段階式實施

從特定用例開始，逐步擴展到整個組織。

### 技能培養

投資團隊的資料工程和分析技能培訓。

### 工具選擇

選擇適合組織需求的資料處理和分析工具。

### 監控和最佳化

建立監控機制，持續最佳化效能和成本。

<br />

## 總結

Data-Centric & Data Lake Architecture 為組織提供了一個靈活、可擴展的資料管理解決方案，特別適合需要處理大量多樣化資料的現代企業。雖然實施複雜度較高，但能夠為組織帶來強大的資料分析能力和業務洞察。

成功實施的關鍵在於建立適當的資料治理框架、選擇合適的技術棧，以及培養團隊的相關技能。隨著資料量和複雜度的不斷增長，資料湖架構將成為企業數位轉型的重要基礎設施。
