#!/usr/bin/env python
import pika
import time
import Fake_Neural

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)
    channel.start_consuming()


def callback(ch, method, properties, body):
    file = body.decode()
    data = dict()
    print(f" [x] Received {file}\n[x] Done")
    data = parseInputData(file=file.split())
    searchNeural(data)
    time.sleep(body.count(b'.'))

    ch.basic_ack(delivery_tag=method.delivery_tag)

def searchNeural(data):
    if data.get('param') == 'colorizer':
        return Fake_Neural.colorizer(init_img_binary_data=data.get('pic1'), params={'0': 1})
    elif data.get('param') == 'delete_background':
        return Fake_Neural.delete_background(init_img_binary_data=data.get('pic1'), params={'0': 1})
    elif data.get('param') == 'upscaler':
        return Fake_Neural.upscaler(init_img_binary_data=data.get('pic1'), params={'0': 1})
    elif data.get('param') == 'image_to_image':
        return Fake_Neural.image_to_image(init_img_binary_data=data.get('pic1'), caption='string', params={'0': 1})
    elif data.get('param') == 'text_to_image':
        return Fake_Neural.text_to_image(caption='string', params={'0': 1})
    elif data.get('param') == 'image_captioning':
        return Fake_Neural.image_captioning(init_img_binary_data=data.get('pic1'), caption='string', params={'0': 1})
    elif data.get('param') == 'image_classification':
        return Fake_Neural.image_classification(init_img_binary_data=data.get('pic1'))
    elif data.get('param') == 'translation':
        return Fake_Neural.translation(input_text='string', source_lang='string', dest_lang='string')
    elif data.get('param') == 'inpainting':
        return Fake_Neural.inpainting(init_img_binary_data=data.get('pic1'), mask_binary_data=b'.', caption='string', params={'0': 1})
    elif data.get('param') == 'stylization':
        return Fake_Neural.stylization(content_binary_data=data.get('pic1'), style_binary_data=b'.', prompt='string', params={'0': 1})
    elif data.get('param') == 'image_fusion':
        return Fake_Neural.image_fusion(img1_binary_data=data.get('pic1'), img2_binary_data=data.get('pic2'), prompt1='string', prompt2='string', params={'0': 1})
    else:
        print("\nYour type of Neural doesn't exist\n")


# Функция разбиения исходной строки формата: "pic1 = byte pic2 = byte param = название нейронки"
def parseInputData(file):
    data = dict()
    for step in range(len(file)):
        if file[step] == 'param':
            data['param'] = file[step + 2]
            i = 0
            while file[i] != 'param':
                if file[i] == 'pic1':
                    data['picOne'] = file[i + 2]
                elif file[i] == 'pic2':
                    data['picTwo'] = file[i + 2]
                i += 1
            break
    return data


main()