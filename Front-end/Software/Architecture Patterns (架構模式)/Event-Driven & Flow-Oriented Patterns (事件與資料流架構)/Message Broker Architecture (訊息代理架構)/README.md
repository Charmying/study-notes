# Message Broker Architecture (訊息代理架構)

Message Broker Architecture (訊息代理架構) 是一種分散式系統架構模式，透過中介軟體來處理應用程式之間的訊息傳遞。

這種架構將訊息的產生者 (Producer) 和消費者 (Consumer) 解耦，使系統具備更好的可擴展性、可靠性和彈性。

<br />

## 動機

在分散式系統中，常見的問題包括

- 服務之間緊密耦合，一個服務的變更影響其他服務

- 同步通訊造成系統阻塞，影響整體效能

- 服務故障時缺乏容錯機制，導致連鎖反應

- 難以處理高併發和流量突增的情況

Message Broker Architecture 通過引入訊息代理，解決這些問題，讓系統具備

- 解耦性：服務之間透過訊息進行間接通訊

- 可靠性：訊息持久化和重試機制確保訊息不遺失

- 可擴展性：可以動態增加消費者來處理更多訊息

- 彈性：服務可以獨立部署和擴展

<br />

## 結構

Message Broker Architecture 包含以下核心元件

### 1. Producer (生產者)

負責產生和發送訊息到 Message Broker。

- 將業務事件轉換為訊息

- 決定訊息的路由和優先級

- 不需要知道消費者的存在

### 2. Message Broker (訊息代理)

中央訊息處理中心，負責接收、儲存和轉發訊息。

- 訊息路由和分發

- 訊息持久化和備份

- 負載平衡和容錯處理

### 3. Consumer (消費者)

從 Message Broker 接收和處理訊息。

- 訂閱感興趣的訊息類型

- 處理業務流程

- 確認訊息處理完成

### 4. Queue/Topic (佇列/主題)

訊息的儲存和組織結構。

- Queue：點對點通訊模式

- Topic：發布訂閱通訊模式

- 支援訊息分區和優先級

以下是 Message Broker Architecture 的結構圖

```text
┌─────────────┐    ┌─────────────────────────────┐    ┌─────────────┐
│  Producer   │───>│       Message Broker        │<───│  Consumer   │
│     A       │    │  ┌─────────┐  ┌─────────┐   │    │      X      │
└─────────────┘    │  │ Queue 1 │  │ Topic A │   │    └─────────────┘
                   │  └─────────┘  └─────────┘   │
┌─────────────┐    │  ┌─────────┐  ┌─────────┐   │    ┌─────────────┐
│  Producer   │───>│  │ Queue 2 │  │ Topic B │   │<───│  Consumer   │
│     B       │    │  └─────────┘  └─────────┘   │    │      Y      │
└─────────────┘    └─────────────────────────────┘    └─────────────┘

                                                      ┌─────────────┐
                                                  <───│  Consumer   │
                                                      │      Z      │
                                                      └─────────────┘
```

<br />

## 核心原則

### 異步通訊 (Asynchronous Communication)

生產者發送訊息後不需要等待消費者處理完成，提升系統效能。

### 訊息持久化 (Message Persistence)

重要訊息會被持久化儲存，確保系統重啟後訊息不遺失。

### 至少一次傳遞 (At-Least-Once Delivery)

確保每個訊息至少被傳遞一次，避免訊息遺失。

<br />

## 實現方式

### Apache Kafka 實現範例

以電商系統的訂單處理為例

- Producer (生產者)

    ```java
    /** 訂單事件生產者 */
    @Component
    public class OrderEventProducer {
        private final KafkaTemplate<String, Object> kafkaTemplate;
        private final ObjectMapper objectMapper;

        public OrderEventProducer(KafkaTemplate<String, Object> kafkaTemplate, ObjectMapper objectMapper) {
            this.kafkaTemplate = kafkaTemplate;
            this.objectMapper = objectMapper;
        }

        public void publishOrderCreated(Order order) {
            try {
                OrderCreatedEvent event = new OrderCreatedEvent(
                    order.getId(),
                    order.getCustomerId(),
                    order.getTotalAmount(),
                    Instant.now()
                );

                kafkaTemplate.send("order-events", order.getId(), event)
                    .addCallback(
                        result -> log.info("訂單事件發送成功: {}", order.getId()),
                        failure -> log.error("訂單事件發送失敗: {}", order.getId(), failure)
                    );
            } catch (Exception e) {
                log.error("發送訂單事件時發生錯誤", e);
            }
        }

        public void publishOrderCancelled(String orderId, String reason) {
            OrderCancelledEvent event = new OrderCancelledEvent(orderId, reason, Instant.now());
            kafkaTemplate.send("order-events", orderId, event);
        }
    }
    ```

- Consumer (消費者)

    ```java
    /** 庫存服務消費者 */
    @Component
    public class InventoryEventConsumer {
        private final InventoryService inventoryService;

        @KafkaListener(topics = "order-events", groupId = "inventory-service")
        public void handleOrderEvent(ConsumerRecord<String, Object> record) {
            try {
                String eventType = record.headers().lastHeader("eventType").value().toString();

                switch (eventType) {
                    case "OrderCreated":
                        handleOrderCreated((OrderCreatedEvent) record.value());
                        break;
                    case "OrderCancelled":
                        handleOrderCancelled((OrderCancelledEvent) record.value());
                        break;
                    default:
                        log.warn("未知的事件類型: {}", eventType);
                }
            } catch (Exception e) {
                log.error("處理訂單事件時發生錯誤", e);
                /** 可以實現重試機制或將訊息發送到死信佇列 */
            }
        }

        private void handleOrderCreated(OrderCreatedEvent event) {
            log.info("處理訂單建立事件: {}", event.getOrderId());
            inventoryService.reserveItems(event.getOrderId(), event.getItems());
        }

        private void handleOrderCancelled(OrderCancelledEvent event) {
            log.info("處理訂單取消事件: {}", event.getOrderId());
            inventoryService.releaseReservation(event.getOrderId());
        }
    }
    ```

- Configuration (配置)

    ```java
    @Configuration
    @EnableKafka
    public class KafkaConfig {

        @Bean
        public ProducerFactory<String, Object> producerFactory() {
            Map<String, Object> props = new HashMap<>();
            props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
            props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
            props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, JsonSerializer.class);
            props.put(ProducerConfig.ACKS_CONFIG, "all");
            props.put(ProducerConfig.RETRIES_CONFIG, 3);
            props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
            return new DefaultKafkaProducerFactory<>(props);
        }

        @Bean
        public KafkaTemplate<String, Object> kafkaTemplate() {
            return new KafkaTemplate<>(producerFactory());
        }

        @Bean
        public ConsumerFactory<String, Object> consumerFactory() {
            Map<String, Object> props = new HashMap<>();
            props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
            props.put(ConsumerConfig.GROUP_ID_CONFIG, "order-processing");
            props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
            props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, JsonDeserializer.class);
            props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
            props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);
            return new DefaultKafkaConsumerFactory<>(props);
        }
    }
    ```

### RabbitMQ 實現範例

- Producer (生產者)

    ```typescript
    /** 通知事件生產者 */
    export class NotificationProducer {
      constructor(private readonly channel: Channel) {}

      async publishEmailNotification(notification: EmailNotification): Promise<void> {
        const exchange = 'notifications';
        const routingKey = 'email.send';

        try {
          const message = Buffer.from(JSON.stringify(notification));

          const published = this.channel.publish(
            exchange,
            routingKey,
            message,
            {
              persistent: true,
              messageId: notification.id,
              timestamp: Date.now(),
              headers: {
                type: 'EmailNotification',
                priority: notification.priority
              }
            }
          );

          if (!published) {
            throw new Error('訊息發送失敗');
          }

          console.log(`郵件通知已發送: ${notification.id}`);
        } catch (error) {
          console.error('發送郵件通知失敗:', error);
          throw error;
        }
      }

      async publishSmsNotification(notification: SmsNotification): Promise<void> {
        const exchange = 'notifications';
        const routingKey = 'sms.send';
        const message = Buffer.from(JSON.stringify(notification));

        this.channel.publish(exchange, routingKey, message, { persistent: true });
        console.log(`簡訊通知已發送: ${notification.id}`);
      }
    }
    ```

- Consumer (消費者)

    ```typescript
    /** 郵件服務消費者 */
    export class EmailConsumer {
      constructor(
        private readonly channel: Channel,
        private readonly emailService: EmailService
      ) {}

      async startConsuming(): Promise<void> {
        const queue = 'email-notifications';

        await this.channel.assertQueue(queue, {
          durable: true,
          arguments: {
            'x-dead-letter-exchange': 'notifications-dlx',
            'x-dead-letter-routing-key': 'email.failed'
          }
        });

        await this.channel.bindQueue(queue, 'notifications', 'email.send');

        this.channel.consume(queue, async (msg) => {
          if (!msg) return;

          try {
            const notification: EmailNotification = JSON.parse(msg.content.toString());

            await this.emailService.sendEmail({
              to: notification.recipient,
              subject: notification.subject,
              body: notification.body
            });

            console.log(`郵件發送成功: ${notification.id}`);
            this.channel.ack(msg);
          } catch (error) {
            console.error('處理郵件通知失敗:', error);

            /** 重試機制 */
            const retryCount = (msg.properties.headers?.retryCount || 0) + 1;

            if (retryCount <= 3) {
              /** 延遲重試 */
              setTimeout(() => {
                this.channel.nack(msg, false, true);
              }, retryCount * 1000);
            } else {
              /** 發送到死信佇列 */
              this.channel.nack(msg, false, false);
            }
          }
        }, {
          noAck: false,
          prefetch: 10
        });
      }
    }
    ```

- Configuration (配置)

    ```typescript
    /** RabbitMQ 連接配置 */
    export class RabbitMQConfig {
      private connection: Connection;
      private channel: Channel;

      async connect(): Promise<void> {
        try {
          this.connection = await amqp.connect({
            hostname: 'localhost',
            port: 5672,
            username: 'guest',
            password: 'guest',
            heartbeat: 60
          });

          this.channel = await this.connection.createChannel();

          /** 設定 Exchange */
          await this.channel.assertExchange('notifications', 'topic', {
            durable: true
          });

          /** 設定死信 Exchange */
          await this.channel.assertExchange('notifications-dlx', 'direct', {
            durable: true
          });

          console.log('RabbitMQ 連接成功');
        } catch (error) {
          console.error('RabbitMQ 連接失敗:', error);
          throw error;
        }
      }

      getChannel(): Channel {
        return this.channel;
      }

      async close(): Promise<void> {
        await this.channel?.close();
        await this.connection?.close();
      }
    }
    ```

### Redis Pub/Sub 實現範例

- Publisher (發布者)

    ```python
    import json
    import redis
    from datetime import datetime
    from typing import Dict, Any

    class EventPublisher:
        def __init__(self, redis_client: redis.Redis):
            self.redis_client = redis_client

        def publish_user_registered(self, user_id: str, email: str) -> None:
            """發布使用者註冊事件"""
            event = {
                'event_type': 'user_registered',
                'user_id': user_id,
                'email': email,
                'timestamp': datetime.utcnow().isoformat()
            }

            self.redis_client.publish('user_events', json.dumps(event))
            print(f"使用者註冊事件已發布: {user_id}")

        def publish_order_completed(self, order_id: str, user_id: str, amount: float) -> None:
            """發布訂單完成事件"""
            event = {
                'event_type': 'order_completed',
                'order_id': order_id,
                'user_id': user_id,
                'amount': amount,
                'timestamp': datetime.utcnow().isoformat()
            }

            self.redis_client.publish('order_events', json.dumps(event))
            print(f"訂單完成事件已發布: {order_id}")
    ```

- Subscriber (訂閱者)

    ```python
    import json
    import redis
    from typing import Callable, Dict, Any

    class EventSubscriber:
        def __init__(self, redis_client: redis.Redis):
            self.redis_client = redis_client
            self.pubsub = redis_client.pubsub()
            self.handlers: Dict[str, Callable] = {}

        def subscribe_to_user_events(self) -> None:
            """訂閱使用者事件"""
            self.pubsub.subscribe('user_events')
            self.handlers['user_registered'] = self.handle_user_registered

        def subscribe_to_order_events(self) -> None:
            """訂閱訂單事件"""
            self.pubsub.subscribe('order_events')
            self.handlers['order_completed'] = self.handle_order_completed

        def start_listening(self) -> None:
            """開始監聽事件"""
            print("開始監聽事件...")

            for message in self.pubsub.listen():
                if message['type'] == 'message':
                    try:
                        event_data = json.loads(message['data'])
                        event_type = event_data.get('event_type')

                        if event_type in self.handlers:
                            self.handlers[event_type](event_data)
                        else:
                            print(f"未知的事件類型: {event_type}")
                    except Exception as e:
                        print(f"處理事件時發生錯誤: {e}")

        def handle_user_registered(self, event_data: Dict[str, Any]) -> None:
            """處理使用者註冊事件"""
            user_id = event_data['user_id']
            email = event_data['email']

            print(f"處理使用者註冊: {user_id}")
            # 發送歡迎郵件
            self.send_welcome_email(email)
            # 建立使用者設定檔
            self.create_user_profile(user_id)

        def handle_order_completed(self, event_data: Dict[str, Any]) -> None:
            """處理訂單完成事件"""
            order_id = event_data['order_id']
            user_id = event_data['user_id']
            amount = event_data['amount']

            print(f"處理訂單完成: {order_id}")
            # 更新使用者積分
            self.update_user_points(user_id, amount)
            # 發送確認郵件
            self.send_order_confirmation(user_id, order_id)

        def send_welcome_email(self, email: str) -> None:
            print(f"發送歡迎郵件至: {email}")

        def create_user_profile(self, user_id: str) -> None:
            print(f"建立使用者設定檔: {user_id}")

        def update_user_points(self, user_id: str, amount: float) -> None:
            points = int(amount * 0.01) # 1% 回饋
            print(f"更新使用者積分: {user_id} +{points}")

        def send_order_confirmation(self, user_id: str, order_id: str) -> None:
            print(f"發送訂單確認郵件: {user_id}, {order_id}")
    ```

### AWS SQS/SNS 實現範例

- Producer (生產者)

    ```typescript
    import { SQSClient, SendMessageCommand } from '@aws-sdk/client-sqs';
    import { SNSClient, PublishCommand } from '@aws-sdk/client-sns';

    /** SQS 訊息生產者 */
    export class SQSProducer {
      constructor(
        private readonly sqsClient: SQSClient,
        private readonly queueUrl: string
      ) {}

      async sendMessage(message: any, delaySeconds?: number): Promise<void> {
        const command = new SendMessageCommand({
          QueueUrl: this.queueUrl,
          MessageBody: JSON.stringify(message),
          DelaySeconds: delaySeconds,
          MessageAttributes: {
            messageType: {
              DataType: 'String',
              StringValue: message.type
            },
            timestamp: {
              DataType: 'String',
              StringValue: new Date().toISOString()
            }
          }
        });

        try {
          const result = await this.sqsClient.send(command);
          console.log(`訊息已發送至 SQS: ${result.MessageId}`);
        } catch (error) {
          console.error('發送 SQS 訊息失敗:', error);
          throw error;
        }
      }
    }

    /** SNS 訊息發布者 */
    export class SNSPublisher {
      constructor(
        private readonly snsClient: SNSClient,
        private readonly topicArn: string
      ) {}

      async publishMessage(message: any, subject?: string): Promise<void> {
        const command = new PublishCommand({
          TopicArn: this.topicArn,
          Message: JSON.stringify(message),
          Subject: subject,
          MessageAttributes: {
            messageType: {
              DataType: 'String',
              StringValue: message.type
            }
          }
        });

        try {
          const result = await this.snsClient.send(command);
          console.log(`訊息已發布至 SNS: ${result.MessageId}`);
        } catch (error) {
          console.error('發布 SNS 訊息失敗:', error);
          throw error;
        }
      }
    }
    ```

- Consumer (消費者)

    ```typescript
    import { SQSClient, ReceiveMessageCommand, DeleteMessageCommand } from '@aws-sdk/client-sqs';

    /** SQS 訊息消費者 */
    export class SQSConsumer {
      private isRunning = false;

      constructor(
        private readonly sqsClient: SQSClient,
        private readonly queueUrl: string,
        private readonly messageHandler: (message: any) => Promise<void>
      ) {}

      async startPolling(): Promise<void> {
        this.isRunning = true;
        console.log('開始輪詢 SQS 訊息...');

        while (this.isRunning) {
          try {
            const command = new ReceiveMessageCommand({
              QueueUrl: this.queueUrl,
              MaxNumberOfMessages: 10,
              WaitTimeSeconds: 20,
              MessageAttributeNames: ['All']
            });

            const result = await this.sqsClient.send(command);

            if (result.Messages) {
              for (const message of result.Messages) {
                try {
                  const messageBody = JSON.parse(message.Body || '{}');
                  await this.messageHandler(messageBody);

                  /** 處理成功後刪除訊息 */
                  await this.deleteMessage(message.ReceiptHandle!);
                } catch (error) {
                  console.error('處理訊息失敗:', error);
                  /** 可以實現重試機制或發送到死信佇列 */
                }
              }
            }
          } catch (error) {
            console.error('輪詢 SQS 時發生錯誤:', error);
            await this.sleep(5000); // 等待 5 秒後重試
          }
        }
      }

      async stopPolling(): Promise<void> {
        this.isRunning = false;
        console.log('停止輪詢 SQS 訊息');
      }

      private async deleteMessage(receiptHandle: string): Promise<void> {
        const command = new DeleteMessageCommand({
          QueueUrl: this.queueUrl,
          ReceiptHandle: receiptHandle
        });

        await this.sqsClient.send(command);
      }

      private sleep(ms: number): Promise<void> {
        return new Promise(resolve => setTimeout(resolve, ms));
      }
    }
    ```

<br />

## 優點

### 解耦性

生產者和消費者之間沒有直接依賴，可以獨立開發和部署。

### 可靠性

- 訊息持久化：重要訊息不會因系統故障而遺失

- 重試機制：失敗的訊息可以自動重試

- 死信佇列：無法處理的訊息會被隔離

### 可擴展性

可以動態增加消費者來處理更多訊息，支援水平擴展。

### 彈性

服務可以按需啟動和停止，不影響其他服務的運作。

### 流量控制

可以控制訊息處理的速度，避免系統過載。

<br />

## 缺點

### 複雜性

引入額外的基礎設施元件，增加系統複雜度。

### 延遲

異步處理可能導致資料一致性延遲。

### 運維成本

Message Broker 需要額外的監控、維護和管理。

### 除錯困難

分散式系統的除錯和追蹤比較困難。

### 訊息順序

在分散式環境中保證訊息順序比較複雜。

<br />

## 適用場景

### 適合使用

- 微服務架構：服務之間需要解耦通訊

- 高併發系統：需要處理大量異步請求

- 事件驅動架構：基於事件的業務流程

- 資料同步：多個系統之間的資料同步

- 工作流程：複雜的業務流程處理

### 不適合使用

- 簡單應用：只有少數服務的簡單系統

- 即時性要求：需要即時回應的場景

- 強一致性：需要強一致性保證的業務

- 資源受限：硬體資源有限的環境

<br />

## 實施建議

### 選擇合適的 Message Broker

根據業務需求選擇合適的訊息代理系統

- Apache Kafka：高吞吐量、持久化、分區

- RabbitMQ：功能豐富、易用、支援多種協定

- Redis Pub/Sub：輕量級、高效能、簡單

- AWS SQS/SNS：託管服務、高可用、易擴展

### 設計訊息格式

定義清楚的訊息格式和版本控制策略。

### 錯誤處理

實現完善的錯誤處理和重試機制。

### 監控和告警

建立完整的監控系統，追蹤訊息處理狀況。

### 測試策略

建立端到端的測試，確保訊息流程正確。

<br />

## 總結

Message Broker Architecture 是構建可擴展、可靠分散式系統的重要架構模式。透過引入訊息代理，系統可以實現服務解耦、提升可靠性和可擴展性。

選擇這種架構時需要考慮系統的複雜度、效能需求和團隊的技術能力。對於需要處理大量異步訊息的系統，Message Broker Architecture 能夠帶來顯著的價值。
