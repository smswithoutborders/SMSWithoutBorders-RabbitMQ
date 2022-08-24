# RabbitMQ for OpenAPI

### Dependencies

- pm2 
```bash
sudo npm install -g pm2
```

- Erlang (minimum 23)

> Arch
```bash
sudo pacman -S erlang
```

> Ubuntu
```bash
sudo apt install wget

wget -c https://packages.erlang-solutions.com/erlang/debian/pool/esl-erlang_24.2-1~ubuntu~focal_amd64.deb -O esl-erlang-24.deb --continue

sudo dpkg -i esl-erlang-24.deb

rm esl-erlang-24.deb

```


### Installation
```bash
make
make start
```

### Uninstallation
```bash
make delete
```

### Usage

#### RabbitMQ Usage
- *Enable management plugin:* View and manage RabbitMQ instances on browser (http://{node-hostname}:15672/)

> For example
> http://localhost:15672/

```bash
./deps/builds/rabbitmq_server-3.9.9/sbin/rabbitmq-plugins enable rabbitmq_management
```
More information: [https://www.rabbitmq.com/management.html](https://www.rabbitmq.com/management.html)

#### Python3 Usage
- Import RabbitMQ libs
```python3
from src.rabbitmq import RabbitMQ
```

- Add new users
```python3
from src.rabbitmq import RabbitMQ

# From Dev SMSWithoutBorders
smswithoutborders_dev_id = ""

# From Dev SMSWithoutBorders
smswithoutborders_dev_key = ""

r = RabbitMQ(dev_id = smswithoutborders_dev_id)

try:
	r.add_users(dev_key=smswithoutborders_dev_key)
except Exception as error:
	raise error
```

- Delete users
```python3
from src.rabbitmq import RabbitMQ

smswithoutborders_dev_id = ""
try:
	r = RabbitMQ(dev_id=smswithoutborders_dev_id)
	r.delete()
except Exception as error:
	raise error
```

- Check if user already exist
```python3
from src.rabbitmq import RabbitMQ

smswithoutborders_dev_id = ""
try:
	r = RabbitMQ(dev_id=smswithoutborders_dev_id)
	if r.exist():
		print("user exist")
	else:
		print("user does not exist")
except Exception as error:
	raise error
```

- Queue SMS messages
```python3
from src.rabbitmq import RabbitMQ

# operator_name = name of operator e.g MTN Cameroon (provided by user)
# text = message to be sent as SMS
# number = reciepeints phone number

data = {
"operator_name":"",
"text":"",
"number":"",
}

try:
	r = RabbitMQ(dev_id=smswithoutborders_dev_id)
	r.request_sms(data=data)
except Exception as error:
	raise error
```
