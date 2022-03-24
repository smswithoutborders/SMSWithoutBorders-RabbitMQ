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
wget -O- https://packages.erlang-solutions.com/ubuntu/erlang_solutions.asc | sudo apt-key add -
echo "deb https://packages.erlang-solutions.com/ubuntu focal contrib" | sudo tee /etc/apt/sources.list.d/erlang-solution.list
sudo apt update
sudo apt-get install -y erlang-base \
                        erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
                        erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
                        erlang-runtime-tools erlang-snmp erlang-ssl \
                        erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl

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
from src.rabbitmq as RabbitMQ
```

- Add new users
```python3
from src.rabbitmq as RabbitMQ

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
from src.rabbitmq as RabbitMQ

smswithoutborders_dev_id = ""
try:
	r = RabbitMQ(dev_id=smswithoutborders_dev_id)
	r.delete()
except Exception as error:
	raise error
```

- Check if user already exist
```python3
from src.rabbitmq as RabbitMQ

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
