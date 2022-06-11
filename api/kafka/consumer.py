import os
from time import sleep
from fpdf import FPDF

# Logger variables to be used for logging
from api.aws_utils import AWSUtils
from api.models import Citizen
from kafka_queue_service import KafkaQueueService
from task1.settings import BASE_DIR


def run(*args):
    try:
        topic_name = "PdfCreator"
        kqs_consumer = KafkaQueueService(topic_name, 'consumer')

        if kqs_consumer.consumer is None:
            raise Exception("Consumer is not available")
        while True:
            kqs_consumer.incoming_queue(read_consumer)
            sleep(10)  # Sleep for 10 seconds
    except Exception as e:
        print("Some error occurred please check")


def read_consumer(consumer):
    print('Getting message.')

    for message in consumer:
        print("message", message)
        print("OFFSET: " + str(message[0]) + "\t MSG: " + str(message))
        message_dict = message.value
        citizen = message_dict["citizen"]
        print("citizen", citizen, type(citizen))
    consumer.close()


def generate_pdf(citizen):
    citizen_obj = Citizen.objects.get(citizen_id=citizen)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)

    pdf.cell(200, 10, txt="Name: " + str(citizen_obj.name), ln=1, align='C')
    pdf.cell(200, 10, txt="Aadhar: " + str(citizen_obj.aadhar), ln=1, align='C')
    pdf.cell(200, 10, txt="dob: " + str(citizen_obj.dob), ln=1, align='C')
    pdf.cell(200, 10, txt="state: " + str(citizen_obj.state), ln=1, align='C')
    pdf.cell(200, 10, txt="location: " + str(citizen_obj.location), ln=1, align='C')
    pdf.cell(200, 10, txt="address: " + str(citizen_obj.address), ln=1, align='C')

    file_name = 'citizen_report_id_' + str(citizen) + '.pdf'
    pdf.output(file_name, os.path.join(BASE_DIR, 'pdf/'))

    # Upload to s3
    aws_dl_object = AWSUtils("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "bucket_name", "S3DIRECT_REGION")
    aws_dl_object.upload_to_s3(file_name, "s3_folder_name" + "/" + file_name)
