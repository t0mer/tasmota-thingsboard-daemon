# tasmota-thingsboard-daemon
tasmota-thingsboard-daemon is a bridge between tasmota devices and ThingsBoard server.

In today's world, where energy efficiency and sustainability are increasingly paramount,
monitoring power consumption has become essential for individuals and businesses alike.

The advent of smart technology has revolutionized this process, offering unparalleled insights and control over energy usage.
Among these innovations, Tasmota smart sockets stand out as versatile and reliable solutions for managing power consumption in a variety of settings.

This guide explores the intersection of Tasmota smart sockets and the Things Board platform, presenting a comprehensive approach to monitoring power usage. By integrating Tasmota-enabled devices with Things Board, users can leverage sophisticated monitoring capabilities, real-time data visualization, and actionable insights to optimize energy efficiency.


# Getting started

## Installing ThingsBoard Using Docker
This section provides detailed instructions for installing ThingsBoard, an open-source IoT platform, using Docker. ThingsBoard offers various deployment options, including single-instance setups with different databases and messaging systems. By leveraging Docker containers, users can quickly set up and manage ThingsBoard installations with ease.

Depending on your requirements and preferences, you can choose from three types of ThingsBoard single-instance Docker images:

### Running ThingsBoard Docker Images

* thingsboard/tb-postgres: Single instance of ThingsBoard with PostgreSQL database.
  * Recommended for small servers with at least 1GB of RAM and minimal load.
  * 2-4GB RAM is recommended for optimal performance.
* thingsboard/tb-cassandra: Single instance of ThingsBoard with Cassandra database.
  * The most performant option, requiring at least 4GB of RAM.
  * 8GB RAM is recommended for optimal performance.
* thingsboard/tb: Single instance of ThingsBoard with embedded HSQLDB database.
  * Not recommended for evaluation or production usage; suitable only for development and testing purposes.

In this guide, we'll focus on using the thingsboard/tb-postgres image. However, you can choose any other image based on your database requirements.

### Choose ThingsBoard Queue Service
ThingsBoard supports various messaging systems/brokers for storing messages and facilitating communication between services. The choice of queue implementation depends on your deployment scenario:

* In Memory: Built-in and default, suitable for development environments but not recommended for production.
* Kafka: Recommended for production deployments, providing scalability and reliability.
* RabbitMQ: Suitable for deployments with low load and existing experience with RabbitMQ.
* AWS SQS, Google Pub/Sub, Azure Service Bus: Fully managed services from cloud providers, useful for cloud deployments.
* Confluent Cloud: Managed streaming platform based on Kafka, suitable for cloud-agnostic deployments.

### Docker Compose Configuration
To set up ThingsBoard with Docker Compose, follow these steps:

* Create a docker-compose.yml file.
* Add the necessary configurations, such as ports mapping and environment variables.
* Start the Docker containers using Docker Compose.

#### Example Docker Compose Configuration

```yaml
version: '3.0'
services:
  mytb:
    restart: always
    image: "thingsboard/tb-postgres"
    ports:
      - "8080:9090"
      - "1883:1883"
      - "7070:7070"
      - "5683-5688:5683-5688/udp"
    environment:
      TB_QUEUE_TYPE: in-memory
    volumes:
      - ~/.mytb-data:/data
      - ~/.mytb-logs:/var/log/thingsboard
```

Explanation of key configurations:

* Ports Mapping: Maps the host's ports to the exposed internal ports of ThingsBoard.
* Environment Variables: Configures the ThingsBoard queue service (in-memory in this example).
* Volumes: Mounts host directories for data storage and logs.


Before starting the containers, ensure to create directories for data storage and logs, and adjust permissions accordingly.

#### Starting ThingsBoard Docker Containers
Once the Docker Compose file is configured, execute the following commands to start ThingsBoard:

```bash
docker-compose up -d
docker-compose logs -f mytb
```

Replace mytb with the name of your service if different. After starting the containers, you can access ThingsBoard via http://{your-host-ip}:8080 in your browser.