# Serverless Architecture (無伺服器架構)

Serverless Architecture (無伺服器架構) 是一種雲端運算執行模式，開發者可以建構和執行應用程式，而無需管理底層的伺服器基礎設施。

這種架構模式讓開發者專注於業務功能的實現，而將伺服器管理、擴展、維護等工作交給雲端服務提供商處理。

<br />

## 動機

在傳統的應用程式部署中，常見的問題包括

- 需要預先配置和管理伺服器資源，增加營運成本

- 難以預測流量變化，導致資源浪費或效能不足

- 需要處理伺服器維護、安全更新、監控等基礎設施工作

- 擴展應用程式需要手動調整伺服器配置

Serverless Architecture 通過事件驅動和自動擴展，解決這些問題，讓系統具備

- 自動擴展：根據需求自動調整資源

- 成本效益：只為實際使用的資源付費

- 快速部署：專注於程式碼而非基礎設施

- 高可用性：雲端服務提供商負責可用性保證

<br />

## 結構

Serverless Architecture 主要由以下元件組成

### 1. Function as a Service (FaaS)

核心運算單元，執行特定的業務功能。

- 事件觸發執行

- 無狀態設計

- 自動擴展

### 2. Backend as a Service (BaaS)

提供後端服務的雲端解決方案。

- 資料庫服務

- 身份驗證服務

- 檔案儲存服務

### 3. Event Sources (事件來源)

觸發函數執行的事件來源。

- HTTP 請求

- 資料庫變更

- 檔案上傳

- 定時任務

### 4. API Gateway

管理和路由 API 請求的服務。

- 請求路由

- 身份驗證

- 流量控制

- 監控分析

以下是 Serverless Architecture 的架構圖

```text
┌───────────────────────────────────────────────────────┐
│                   Client Applications                 │
└───────────────────────────┬───────────────────────────┘
                            │
┌───────────────────────────▼───────────────────────────┐
│                      API Gateway                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐  │
│  │   Routing   │ │    Auth     │ │  Rate Limiting  │  │
│  └─────────────┘ └─────────────┘ └─────────────────┘  │
└───────────────────────────┬───────────────────────────┘
                            │
┌───────────────────────────▼───────────────────────────┐
│                   Lambda Functions                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐  │
│  │  Function A │ │  Function B │ │    Function C   │  │
│  └─────────────┘ └─────────────┘ └─────────────────┘  │
└───────────────────────────┬───────────────────────────┘
                            │
┌───────────────────────────▼───────────────────────────┐
│                Backend Services (BaaS)                │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐  │
│  │  Database   │ │   Storage   │ │   External APIs │  │
│  └─────────────┘ └─────────────┘ └─────────────────┘  │
└───────────────────────────────────────────────────────┘
```

<br />

## 核心原則

### 事件驅動 (Event-Driven)

函數由事件觸發執行，而非持續運行。

### 無狀態 (Stateless)

每次函數執行都是獨立的，不保存狀態資訊。

### 自動擴展 (Auto-Scaling)

根據請求量自動調整執行實例數量。

### 按使用付費 (Pay-per-Use)

只為實際執行時間和資源使用付費。

<br />

## 實現方式

### AWS Lambda 實現範例

以電商系統的訂單處理為例

- 訂單建立函數

    ```javascript
    const AWS = require('aws-sdk');
    const dynamodb = new AWS.DynamoDB.DocumentClient();
    const sns = new AWS.SNS();

    exports.handler = async (event) => {
      try {
        const orderData = JSON.parse(event.body);

        /** 驗證訂單資料 */
        if (!orderData.customerId || !orderData.items) {
          return {
            statusCode: 400,
            body: JSON.stringify({ error: '訂單資料不完整' })
          };
        }

        /** 計算總金額 */
        const totalAmount = orderData.items.reduce((sum, item) => {
          return sum + (item.price * item.quantity);
        }, 0);

        /** 建立訂單 */
        const order = {
          orderId: generateOrderId(),
          customerId: orderData.customerId,
          items: orderData.items,
          totalAmount: totalAmount,
          status: 'PENDING',
          createdAt: new Date().toISOString()
        };

        /** 儲存到 DynamoDB */
        await dynamodb.put({
          TableName: 'Orders',
          Item: order
        }).promise();

        /** 發送通知 */
        await sns.publish({
          TopicArn: process.env.ORDER_TOPIC_ARN,
          Message: JSON.stringify({
            eventType: 'ORDER_CREATED',
            orderId: order.orderId,
            customerId: order.customerId
          })
        }).promise();

        return {
          statusCode: 201,
          body: JSON.stringify({
            orderId: order.orderId,
            status: order.status,
            totalAmount: order.totalAmount
          })
        };
      } catch (error) {
        console.error('建立訂單失敗:', error);
        return {
          statusCode: 500,
          body: JSON.stringify({ error: '內部伺服器錯誤' })
        };
      }
    };

    function generateOrderId() {
      return 'ORDER-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
    }
    ```

- 訂單狀態更新函數

    ```javascript
    const AWS = require('aws-sdk');
    const dynamodb = new AWS.DynamoDB.DocumentClient();
    const ses = new AWS.SES();

    exports.handler = async (event) => {
      try {
        /** 處理 SNS 訊息 */
        for (const record of event.Records) {
          const message = JSON.parse(record.Sns.Message);

          if (message.eventType === 'ORDER_CREATED') {
            await processNewOrder(message.orderId, message.customerId);
          }
        }

        return { statusCode: 200 };
      } catch (error) {
        console.error('處理訂單事件失敗:', error);
        throw error;
      }
    };

    async function processNewOrder(orderId, customerId) {
      /** 模擬訂單處理流程 */
      await new Promise(resolve => setTimeout(resolve, 2000));

      /** 更新訂單狀態 */
      await dynamodb.update({
        TableName: 'Orders',
        Key: { orderId: orderId },
        UpdateExpression: 'SET #status = :status, updatedAt = :updatedAt',
        ExpressionAttributeNames: {
          '#status': 'status'
        },
        ExpressionAttributeValues: {
          ':status': 'CONFIRMED',
          ':updatedAt': new Date().toISOString()
        }
      }).promise();

      /** 取得客戶資訊 */
      const customer = await dynamodb.get({
        TableName: 'Customers',
        Key: { customerId: customerId }
      }).promise();

      /** 發送確認郵件 */
      if (customer.Item && customer.Item.email) {
        await ses.sendEmail({
          Source: 'noreply@example.com',
          Destination: {
            ToAddresses: [customer.Item.email]
          },
          Message: {
            Subject: {
              Data: '訂單確認通知'
            },
            Body: {
              Text: {
                Data: `親愛的客戶，訂單 ${orderId} 已確認處理。`
              }
            }
          }
        }).promise();
      }
    }
    ```

### Azure Functions 實現範例

- HTTP 觸發函數

    ```javascript
    const { CosmosClient } = require('@azure/cosmos');
    const { ServiceBusClient } = require('@azure/service-bus');

    const cosmosClient = new CosmosClient(process.env.COSMOS_CONNECTION_STRING);
    const database = cosmosClient.database('ecommerce');
    const container = database.container('products');

    module.exports = async function (context, req) {
      try {
        const productId = req.params.id;

        if (!productId) {
          context.res = {
            status: 400,
            body: { error: '產品 ID 為必填' }
          };
          return;
        }

        /** 從 Cosmos DB 取得產品資訊 */
        const { resource: product } = await container.item(productId, productId).read();

        if (!product) {
          context.res = {
            status: 404,
            body: { error: '產品不存在' }
          };
          return;
        }

        /** 記錄查詢事件 */
        const serviceBusClient = new ServiceBusClient(process.env.SERVICE_BUS_CONNECTION_STRING);
        const sender = serviceBusClient.createSender('product-views');

        await sender.sendMessages({
          body: {
            productId: productId,
            timestamp: new Date().toISOString(),
            userAgent: req.headers['user-agent']
          }
        });

        await sender.close();
        await serviceBusClient.close();

        context.res = {
          status: 200,
          body: {
            id: product.id,
            name: product.name,
            price: product.price,
            description: product.description,
            inStock: product.inventory > 0
          }
        };
      } catch (error) {
        context.log.error('取得產品資訊失敗:', error);
        context.res = {
          status: 500,
          body: { error: '內部伺服器錯誤' }
        };
      }
    };
    ```

### Google Cloud Functions 實現範例

- Pub/Sub 觸發函數

    ```javascript
    const { Firestore } = require('@google-cloud/firestore');
    const { PubSub } = require('@google-cloud/pubsub');
    const sgMail = require('@sendgrid/mail');

    const firestore = new Firestore();
    const pubsub = new PubSub();
    sgMail.setApiKey(process.env.SENDGRID_API_KEY);

    exports.processUserRegistration = async (message, context) => {
      try {
        const userData = JSON.parse(Buffer.from(message.data, 'base64').toString());

        /** 建立使用者檔案 */
        const userRef = firestore.collection('users').doc(userData.userId);
        await userRef.set({
          email: userData.email,
          name: userData.name,
          registeredAt: new Date(),
          emailVerified: false,
          status: 'ACTIVE'
        });

        /** 產生驗證 token */
        const verificationToken = generateVerificationToken();

        /** 儲存驗證 token */
        await firestore.collection('email-verifications').doc(userData.userId).set({
          token: verificationToken,
          email: userData.email,
          createdAt: new Date(),
          expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000) /** 24小時後過期 */
        });

        /** 發送驗證郵件 */
        const verificationUrl = `${process.env.FRONTEND_URL}/verify-email?token=${verificationToken}`;

        await sgMail.send({
          to: userData.email,
          from: 'noreply@example.com',
          subject: '請驗證電子郵件地址',
          html: `
            <h2>歡迎加入！</h2>
            <p>請點擊以下連結驗證電子郵件地址：</p>
            <a href="${verificationUrl}">驗證郵件</a>
            <p>此連結將在 24 小時後失效。</p>
          `
        });

        /** 發送歡迎通知到其他服務 */
        const welcomeTopic = pubsub.topic('user-welcome');
        await welcomeTopic.publishMessage({
          data: Buffer.from(JSON.stringify({
            userId: userData.userId,
            email: userData.email,
            name: userData.name
          }))
        });

        console.log(`使用者註冊處理完成: ${userData.userId}`);
      } catch (error) {
        console.error('處理使用者註冊失敗:', error);
        throw error;
      }
    };

    function generateVerificationToken() {
      return require('crypto').randomBytes(32).toString('hex');
    }
    ```

### Serverless Framework 配置範例

- serverless.yml 配置

    ```yaml
    service: ecommerce-serverless

    provider:
      name: aws
      runtime: nodejs18.x
      region: us-east-1
      environment:
        ORDERS_TABLE: ${self:service}-orders-${self:provider.stage}
        CUSTOMERS_TABLE: ${self:service}-customers-${self:provider.stage}
        ORDER_TOPIC_ARN: !Ref OrderTopic
      iamRoleStatements:
        - Effect: Allow
          Action:
            - dynamodb:Query
            - dynamodb:Scan
            - dynamodb:GetItem
            - dynamodb:PutItem
            - dynamodb:UpdateItem
            - dynamodb:DeleteItem
          Resource:
            - !GetAtt OrdersTable.Arn
            - !GetAtt CustomersTable.Arn
        - Effect: Allow
          Action:
            - sns:Publish
          Resource: !Ref OrderTopic
        - Effect: Allow
          Action:
            - ses:SendEmail
          Resource: "*"

    functions:
      createOrder:
        handler: handlers/orders.create
        events:
          - http:
              path: /orders
              method: post
              cors: true
        environment:
          ORDERS_TABLE: !Ref OrdersTable

      processOrder:
        handler: handlers/orders.process
        events:
          - sns:
              arn: !Ref OrderTopic
              topicName: order-events

      getOrder:
        handler: handlers/orders.get
        events:
          - http:
              path: /orders/{id}
              method: get
              cors: true

      scheduledCleanup:
        handler: handlers/cleanup.run
        events:
          - schedule: rate(1 day)

    resources:
      Resources:
        OrdersTable:
          Type: AWS::DynamoDB::Table
          Properties:
            TableName: ${self:provider.environment.ORDERS_TABLE}
            AttributeDefinitions:
              - AttributeName: orderId
                AttributeType: S
            KeySchema:
              - AttributeName: orderId
                KeyType: HASH
            BillingMode: PAY_PER_REQUEST

        CustomersTable:
          Type: AWS::DynamoDB::Table
          Properties:
            TableName: ${self:provider.environment.CUSTOMERS_TABLE}
            AttributeDefinitions:
              - AttributeName: customerId
                AttributeType: S
            KeySchema:
              - AttributeName: customerId
                KeyType: HASH
            BillingMode: PAY_PER_REQUEST

        OrderTopic:
          Type: AWS::SNS::Topic
          Properties:
            TopicName: order-events
    ```

### TypeScript Serverless 實現範例

- 型別定義

    ```typescript
    /** 領域模型 */
    export interface Order {
      orderId: string;
      customerId: string;
      items: OrderItem[];
      totalAmount: number;
      status: OrderStatus;
      createdAt: string;
      updatedAt?: string;
    }

    export interface OrderItem {
      productId: string;
      productName: string;
      quantity: number;
      price: number;
    }

    export enum OrderStatus {
      PENDING = 'PENDING',
      CONFIRMED = 'CONFIRMED',
      SHIPPED = 'SHIPPED',
      DELIVERED = 'DELIVERED',
      CANCELLED = 'CANCELLED'
    }

    /** API 請求/回應模型 */
    export interface CreateOrderRequest {
      customerId: string;
      items: OrderItem[];
    }

    export interface CreateOrderResponse {
      orderId: string;
      status: OrderStatus;
      totalAmount: number;
    }
    ```

- Lambda 函數實作

    ```typescript
    import { APIGatewayProxyHandler, APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';
    import { DynamoDB, SNS } from 'aws-sdk';
    import { CreateOrderRequest, CreateOrderResponse, Order, OrderStatus } from '../types/order';

    const dynamodb = new DynamoDB.DocumentClient();
    const sns = new SNS();

    export const createOrder: APIGatewayProxyHandler = async (
      event: APIGatewayProxyEvent
    ): Promise<APIGatewayProxyResult> => {
      try {
        /** 解析請求資料 */
        const request: CreateOrderRequest = JSON.parse(event.body || '{}');

        /** 驗證請求資料 */
        const validationError = validateCreateOrderRequest(request);
        if (validationError) {
          return createErrorResponse(400, validationError);
        }

        /** 建立訂單 */
        const order = await createOrderEntity(request);

        /** 儲存訂單 */
        await saveOrder(order);

        /** 發送事件 */
        await publishOrderCreatedEvent(order);

        /** 回傳結果 */
        const response: CreateOrderResponse = {
          orderId: order.orderId,
          status: order.status,
          totalAmount: order.totalAmount
        };

        return {
          statusCode: 201,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          },
          body: JSON.stringify(response)
        };
      } catch (error) {
        console.error('建立訂單失敗:', error);
        return createErrorResponse(500, '內部伺服器錯誤');
      }
    };

    function validateCreateOrderRequest(request: CreateOrderRequest): string | null {
      if (!request.customerId) {
        return '客戶 ID 為必填';
      }

      if (!request.items || request.items.length === 0) {
        return '訂單項目不能為空';
      }

      for (const item of request.items) {
        if (!item.productId || item.quantity <= 0 || item.price <= 0) {
          return '訂單項目資料不正確';
        }
      }

      return null;
    }

    async function createOrderEntity(request: CreateOrderRequest): Promise<Order> {
      const totalAmount = request.items.reduce(
        (sum, item) => sum + (item.price * item.quantity),
        0
      );

      return {
        orderId: generateOrderId(),
        customerId: request.customerId,
        items: request.items,
        totalAmount: totalAmount,
        status: OrderStatus.PENDING,
        createdAt: new Date().toISOString()
      };
    }

    async function saveOrder(order: Order): Promise<void> {
      await dynamodb.put({
        TableName: process.env.ORDERS_TABLE!,
        Item: order
      }).promise();
    }

    async function publishOrderCreatedEvent(order: Order): Promise<void> {
      await sns.publish({
        TopicArn: process.env.ORDER_TOPIC_ARN!,
        Message: JSON.stringify({
          eventType: 'ORDER_CREATED',
          orderId: order.orderId,
          customerId: order.customerId,
          totalAmount: order.totalAmount
        })
      }).promise();
    }

    function generateOrderId(): string {
      return 'ORDER-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
    }

    function createErrorResponse(statusCode: number, message: string): APIGatewayProxyResult {
      return {
        statusCode,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({ error: message })
      };
    }
    ```

<br />

## 優點

### 成本效益

只為實際執行時間付費，無需為閒置資源付費。

### 自動擴展

根據請求量自動調整資源，無需手動配置。

### 快速部署

專注於程式碼開發，快速部署和更新。

### 高可用性

雲端服務提供商負責基礎設施的可用性和容錯。

### 減少營運負擔

無需管理伺服器、作業系統更新、安全修補等。

<br />

## 缺點

### 冷啟動延遲

函數首次執行或長時間未使用後會有啟動延遲。

### 執行時間限制

大多數 FaaS 平台對函數執行時間有限制。

### 供應商鎖定

依賴特定雲端服務提供商的服務和 API。

### 除錯困難

分散式架構使得除錯和監控變得複雜。

### 狀態管理複雜

無狀態設計要求外部儲存狀態資訊。

<br />

## 適用場景

### 適合使用

- 事件驅動應用：需要響應特定事件的應用

- 微服務架構：將大型應用拆分為小型服務

- API 後端：提供 RESTful API 服務

- 資料處理：批次處理、ETL 作業

- 定時任務：排程執行的背景作業

- 原型開發：快速驗證概念和想法

### 不適合使用

- 長時間運行：需要持續執行的應用

- 高頻率請求：需要極低延遲的應用

- 複雜狀態管理：需要維護複雜狀態的應用

- 大型檔案處理：需要處理大型檔案的應用

- 即時通訊：需要持續連線的應用

<br />

## 最佳實踐

### 函數設計

- 保持函數小而專注，遵循單一職責原則

- 設計無狀態函數，避免依賴本地狀態

- 優化冷啟動時間，減少依賴和初始化時間

- 實作適當的錯誤處理和重試機制

### 效能優化

- 重用連線和資源，避免重複初始化

- 使用連線池管理資料庫連線

- 實作快取策略減少外部服務呼叫

- 選擇適當的記憶體配置

### 安全考量

- 使用最小權限原則配置 IAM 角色

- 加密敏感資料和環境變數

- 實作適當的身份驗證和授權

- 定期更新依賴套件

### 監控和除錯

- 實作結構化日誌記錄

- 使用分散式追蹤監控請求流程

- 設定適當的警報和監控指標

- 建立健康檢查和監控儀表板

<br />

## 實施建議

### 漸進式遷移

從邊緣功能開始，逐步將現有應用遷移到 Serverless 架構。

### 選擇合適的雲端服務

評估不同雲端服務提供商的功能、價格和生態系統。

### 建立 CI/CD 流程

自動化部署和測試流程，確保程式碼品質。

### 團隊培訓

培訓團隊成員了解 Serverless 開發模式和最佳實踐。

### 成本監控

建立成本監控機制，避免意外的高額費用。

<br />

## 總結

Serverless Architecture 提供了一種新的應用程式開發和部署模式，特別適合事件驅動和微服務架構的應用。雖然存在一些限制，但對於合適的使用場景，能夠顯著降低營運成本、提高開發效率和系統可擴展性。

關鍵在於理解 Serverless 的特性和限制，選擇合適的使用場景，並遵循最佳實踐來設計和實作應用程式。隨著雲端技術的不斷發展，Serverless Architecture 將成為現代應用程式開發的重要選擇。
