# MQTT-to-ThingsBoard-Temp-Humi-USING-MQTT
Đoạn code trên là một ví dụ về cách sử dụng thư viện Paho MQTT trong Python để kết nối và giao tiếp với một broker MQTT, cụ thể là ThingsBoard, một nền tảng IoT.
# Import thư viện và module
- `import paho.mqtt.client as mqtt` : Import module mqtt từ thư viện Paho MQTT và đặt tên ngắn là mqtt.
- `import json`: Import module json để xử lý dữ liệu JSON.
# Thiết lập Thingsboard
- `THINGSBOARD_HOST = "localhost"` : Host của ThingsBoard MQTT Broker
- `THINGSBOARD_PORT = 1883` : Port của ThingsBoard MQTT Broker.
- `ACCESS_TOKEN = "IlBvTvKqEJgVQLcyHIeo"` : Mã truy cập để xác thực với ThingsBoard.
# Định nghĩa xử lý hàm sự kiện khi kết nối tới MQTT broker
```sh
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code " + str(rc))
    
    # SUBCRIBE MQTT
    client.subscribe("esp32/temperature")
    client.subscribe("esp32/humidity")
```
- In ra thông báo xác nhận về việc kết nối thành công với MQTT Broker cùng với mã kết quả (rc).
- Đăng ký (subscribe) các chủ đề MQTT cụ thể (esp32/temperature và esp32/humidity) để nhận các tin nhắn từ các thiết bị gửi dữ liệu nhiệt độ và độ ẩm.
- `on_connect` : Hàm được gọi khi kết nối thành công với MQTT broker.
- `client`: đối tợợng client MQTT
- `userdata` : Dữ liệu người dùng đụược tùy chọn truyền vào khi thiết lập client MQTT.
- `flags` : Các cờ kết nối MQTT
- Các cờ kết nối MQTT được truyền vào hàm `on_connect` là một tham số để cung cấp thông tin về trạng thái kết nối MQTT. Các cờ này có thể giúp bạn kiểm soát và xử lý các trường hợp đặc biệt khi kết nối với broker MQTT. Dưới đây là một số cờ thông dụng và ý nghĩa của chúng:
- `flags['clean_session']`: Biến boolean xác định liệu session của client MQTT có phải là session mới (clean session) hay không. Nếu `clean_session` là True, broker sẽ loại bỏ mọi thông tin về client khi client ngắt kết nối; nếu là False, thông tin session sẽ được giữ lại.
- `flags['session_present']`: Biến boolean chỉ ra liệu có tồn tại session trước đó cho client này trên broker hay không. Nếu `session_present` là True, đây là một kết nối tiếp theo của client, và broker có thể khôi phục lại trạng thái của session trước đó.
- `flags['will']`: Biến boolean xác định liệu client này có thông điệp "will" (lời từ biệt) được thiết lập hay không. Nếu có, client sẽ gửi thông điệp "will" đến broker khi client ngắt kết nối một cách bất thường.
- `flags['will_retain']`: Biến boolean chỉ ra liệu thông điệp "will" được gửi với cờ retain hay không. Nếu `will_retain` là True, thông điệp "will" sẽ được lưu trữ (retain) trên broker và gửi cho các client mới kết nối sau này.
- `flags['username_flag']` và `flags['password_flag']`: Các biến boolean chỉ ra liệu thông tin tên người dùng (username) và mật khẩu (password) đã được gửi kèm theo trong gói tin kết nối hay không.
Những cờ này cung cấp thông tin chi tiết về trạng thái kết nối MQTT và có thể được sử dụng để xử lý logic phù hợp trong hàm `on_connect`.
- `rc` : Mã kết quả của quá trình kết nối. Mã này đụược sử dụng để kiểm tra kết quả của việc kết nối.

```sh
# DINH NGHIA HAM ON_MESSAGE
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    topic = msg.topic # LAY CHU DE TU DEVICE GUI TOI BROKER 

    if topic == "esp32/temperature":
        temperature = payload.get("temperature")
      if temperature is not None:
            send_to_thingsboard("temperature", temperature)
    
    elif topic == "esp32/humidity": 
        humidity = payload.get("humidity")
        if humidity is not None:
            send_to_thingsboard("humidity", humidity)
```
Hàm `on_message` được định nghĩa để xử lý các tin nhắn nhận được từ broker MQTT khi kết nối với các chủ đề cụ thể. 

### Tham số:
- `client`: Đối tượng client MQTT.
- `userdata`: Dữ liệu người dùng tùy chọn được truyền vào khi thiết lập client MQTT.
- `msg`: Đối tượng tin nhắn MQTT, bao gồm các thông tin như chủ đề (topic) và nội dung tin nhắn (payload).

### Chức năng:
- Chuyển đổi dữ liệu payload từ dạng JSON sang đối tượng Python.
- Trích xuất chủ đề của tin nhắn và dữ liệu từ payload.
- Kiểm tra chủ đề của tin nhắn và xử lý dữ liệu tương ứng.
- Gửi dữ liệu tới ThingsBoard thông qua hàm `send_to_thingsboard` nếu dữ liệu được trích xuất thành công.

### Giải Thích Chi Tiết:
1. **Chuyển Đổi Dữ Liệu Payload:**
   - Dòng `payload = json.loads(msg.payload)` chuyển đổi dữ liệu payload từ dạng JSON sang đối tượng Python, để có thể truy cập và xử lý các trường dữ liệu cụ thể.

2. **Trích Xuất Chủ Đề và Dữ Liệu:**
   - Dòng `topic = msg.topic` gán chủ đề của tin nhắn vào biến `topic`, để xác định loại dữ liệu được gửi từ thiết bị tới broker.
   - Dòng `temperature = payload.get("temperature")` và `humidity = payload.get("humidity")` trích xuất dữ liệu nhiệt độ và độ ẩm từ payload nếu chúng tồn tại.

3. **Xử Lý Dữ Liệu Tương Ứng:**
   - Sử dụng các điều kiện để kiểm tra chủ đề của tin nhắn:
     - Nếu chủ đề là `"esp32/temperature"`, thực hiện xử lý dữ liệu nhiệt độ.
     - Nếu chủ đề là `"esp32/humidity"`, thực hiện xử lý dữ liệu độ ẩm.
   - Nếu dữ liệu nhiệt độ hoặc độ ẩm được trích xuất thành công (`temperature is not None` hoặc `humidity is not None`), thì gọi hàm `send_to_thingsboard` để gửi dữ liệu tới ThingsBoard.

4. **Gửi Dữ Liệu Tới ThingsBoard:**
   - Hàm `send_to_thingsboard` được gọi để gửi dữ liệu nhiệt độ hoặc độ ẩm tới ThingsBoard thông qua giao thức MQTT, dựa trên loại dữ liệu được xác định từ chủ đề của tin nhắn.

```sh
def send_to_thingsboard(sensor_type, value):
    # Send data to ThingsBoard using MQTT
    thingsboard_topic = f"v1/devices/me/telemetry"
    data = {sensor_type: value}
    client.publish(thingsboard_topic, json.dumps(data), qos=1)
    print(f"Data sent to ThingsBoard via MQTT: {sensor_type} -{value}")
```

Hàm `send_to_thingsboard` được định nghĩa để gửi dữ liệu từ cảm biến tới ThingsBoard sử dụng giao thức MQTT.

### Tham số:
- `sensor_type`: Loại cảm biến, ví dụ: "temperature", "humidity".
- `value`: Giá trị đo được từ cảm biến.

### Chức năng:
- Xây dựng và gửi gói tin chứa dữ liệu cảm biến tới ThingsBoard qua giao thức MQTT.
- In ra thông báo xác nhận việc gửi dữ liệu tới ThingsBoard.

### Giải Thích Chi Tiết:
1. **Xây Dựng Chủ Đề và Dữ Liệu:**
   - Dòng `thingsboard_topic = f"v1/devices/me/telemetry"` xây dựng chủ đề MQTT để gửi dữ liệu tới ThingsBoard. Trong trường hợp này, `v1/devices/me/telemetry` là định dạng chung để gửi dữ liệu tới ThingsBoard theo chuẩn của nền tảng, hiện tại mình dùng local.
   - Dòng `data = {sensor_type: value}` tạo một đối tượng từ điển `data` chứa dữ liệu của cảm biến, với `sensor_type` là khóa và `value` là giá trị của cảm biến.

2. **Gửi Dữ Liệu Tới ThingsBoard:**
   - Hàm `client.publish(thingsboard_topic, json.dumps(data), qos=1)` gửi dữ liệu tới ThingsBoard thông qua giao thức MQTT. Tham số `thingsboard_topic` là chủ đề MQTT, `json.dumps(data)` là dữ liệu dạng JSON của cảm biến được chuyển đổi thành chuỗi, và `qos=1` chỉ định mức độ chất lượng dịch vụ (Quality of Service) là 1.
   
3. **In Thông Báo:**
   - Dòng `print(f"Data sent to ThingsBoard via MQTT: {sensor_type} -{value}")` in ra thông báo xác nhận rằng dữ liệu đã được gửi thành công tới ThingsBoard thông qua giao thức MQTT, kèm theo loại cảm biến và giá trị của nó.

# Tạo và cấu hình Client MQTT:
```sh
#Create and setup Client MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, THINGSBOARD_PORT, 60)
```
- `client = mqtt.Client()` : Tạo một đối tượng Client MQTT mới.
- `client.on_connect = on_connect` : Gán hàm on_connect cho sự kiện kết nối.
- `client.on_message = on_message` : Gán hàm on_message cho sự kiện nhận tin nhắn.
- `client.username_pw_set(ACCESS_TOKEN)` : Thiết lập mã truy cập cho client.
- `client.connect(THINGSBOARD_HOST, THINGSBOARD_PORT, 60)`: Kết nối tới ThingsBoard MQTT Broker.
- Tạo và cấu hình một đối tượng client MQTT để kết nối và giao tiếp với broker MQTT (ThingsBoard) dựa trên các thông tin cấu hình như mã truy cập và địa chỉ broker đã được xác định trước đó. 

1. **Tạo Đối Tượng Client MQTT:**
   - Dòng `client = mqtt.Client()` tạo một đối tượng client MQTT mới. Đối tượng này sẽ được sử dụng để thiết lập kết nối và trao đổi dữ liệu với broker MQTT.

2. **Cấu Hình Hàm Xử Lý Sự Kiện:**
   - Dòng `client.on_connect = on_connect` gán hàm `on_connect` cho sự kiện kết nối. Điều này có nghĩa là khi client kết nối thành công với broker MQTT, hàm `on_connect` sẽ được gọi để xử lý sự kiện.
   - Dòng `client.on_message = on_message` gán hàm `on_message` cho sự kiện nhận tin nhắn. Khi client nhận được một tin nhắn từ broker MQTT, hàm `on_message` sẽ được gọi để xử lý tin nhắn đó.

3. **Thiết Lập Mã Truy Cập và Kết Nối:**
   - Dòng `client.username_pw_set(ACCESS_TOKEN)` thiết lập mã truy cập (ACCESS_TOKEN) để xác thực với broker MQTT. Mã truy cập này sẽ được sử dụng để xác định client khi kết nối với broker.
   - Dòng `client.connect(THINGSBOARD_HOST, THINGSBOARD_PORT, 60)` thực hiện kết nối tới broker MQTT. Tham số đầu tiên là `THINGSBOARD_HOST` và `THINGSBOARD_PORT` là địa chỉ và cổng của broker MQTT. Tham số thứ ba (60) là thời gian timeout, tức là thời gian tối đa (trong giây) mà client sẽ chờ khi kết nối với broker.

Sau khi các bước trên được thực hiện, client MQTT sẽ được thiết lập và kết nối với broker MQTT, và sẵn sàng để gửi và nhận dữ liệu.
```sh
# LISTEN AND DUY TRI KET NOI
client.loop_start()

# Giu chuong trinh chay vo han
while True:
    pass
```
Dòng mã `client.loop_start()` bắt đầu một luồng dữ liệu để duy trì kết nối với broker MQTT. Luồng này cho phép client MQTT lắng nghe các sự kiện từ broker mà không cần chờ đợi các sự kiện đó trong luồng chính của chương trình. Điều này giúp tránh tình trạng chương trình bị chặn khi phải chờ đợi sự kiện từ broker.

Sau khi gọi `client.loop_start()`, chương trình tiếp tục vào một vòng lặp vô hạn (`while True:`) để giữ chương trình chạy liên tục. Vòng lặp này không có nội dung (dòng `pass` chỉ đơn giản là một lệnh trống không làm gì cả), do đó chương trình chỉ tiếp tục chạy mà không thực hiện bất kỳ công việc cụ thể nào trong vòng lặp.

Như vậy, với cách triển khai này, chương trình sẽ tiếp tục chạy vo hạn, trong khi vẫn duy trì kết nối với broker MQTT và lắng nghe các sự kiện từ broker một cách đồng thời.
# Lắng nghe và duy trì kết nối:
- `client.loop_start()` : Bắt đầu một luồng dữ liệu để duy trì kết nối với broker.
# Vòng lặp chính:
- ` while True: pass:` Vòng lặp vô hạn để duy trì chương trình chạy, vì luồng dữ liệu được duy trì trong luồng riêng biệt.
