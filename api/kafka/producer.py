from kafka_queue_service import KafkaQueueService


def run(*args):
    try:
        topic_name = "PdfCreator"
        kqs_producer = KafkaQueueService(topic_name, 'producer')

        if kqs_producer.producer is None:
            raise Exception("Producer is not available")

        outgoing_data = {"citizen_id": 27001}
        kqs_producer.outgoing_queue(outgoing_data, True)

    except Exception as e:
        print("Some error occurred please check")

