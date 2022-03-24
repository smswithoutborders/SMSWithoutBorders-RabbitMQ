rabbitmq_instance=deps/rabbitmq-server-generic-unix-3.9.9.tar.xz 
rabbitmq_python_instance=rabbitmq-server-unix-instance.py


configure:
	# Extract tar files
	@mkdir deps/builds
	@echo -e "[*] Extracting dependencies..."
	@tar -xf ${rabbitmq_instance} -C deps/builds/
	@echo -e "[*] Done!"

start:
	@echo -e "[*] Starting rabbitmq instances..."
	@pm2 start ${rabbitmq_python_instance} --interpreter ./venv/bin/python3

stop:
	@echo -e "[*] Stopping rabbitmq instances..."
	@pm2 stop ${rabbitmq_python_instance}

clear:
	@echo -e "[-] Removing dependencies..."
	@rm -rf deps/builds

delete: stop clear
	@echo -e "[-] Deleting RabbitMQ instances..."
	@pm2 delete ${rabbitmq_python_instance}
