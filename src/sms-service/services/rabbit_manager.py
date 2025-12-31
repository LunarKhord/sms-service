"""
This module serves the purpose of managing RabbitMQ connections for the SMS service.
It establishes a robust connection to the RabbitMQ server using the provided RABBITMQ_URL.
"""


from lifespan import bootup_rabbitmq
import aio_pika
import aio_pika.abc 


async def get_rabbitmq_connection() -> aio_pika.abc.AbstractRobustConnection:
    rabbitmq_connection = await bootup_rabbitmq()
    print(f"RabbitMQ connection in get_rabbitmq_connection: {rabbitmq_connection}")
    return rabbitmq_connection