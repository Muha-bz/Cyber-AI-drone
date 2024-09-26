import time
import signal
import cv2
import numpy as np
import socketio
import asyncio
import aiofiles
from collections import defaultdict
# from video_processing import Connect_yolo
from datetime import datetime
# import  test_photo
import logging
import  socket
from ultralytics import YOLO

# model = YOLO("Cyber-AI-drone.pt")
server = 'http://192.168.10.115:3006/'  # адресс вашего ровера
IP_ADDRESS      = socket.gethostbyname(socket.gethostname())
PORT_YOLO       = 12345
RTSP_LINK       = 'rtsp://192.168.10.115:8554/usb'
# Создаем экземпляр асинхронного клиента Socket.IO
sio = socketio.AsyncClient()
diameter_of_wheel = 0.24  # Диаметр колеса в метрах
circumference = 3.14159 * diameter_of_wheel  # Окружность колеса


async def write_report(message):  # Функция создания автоматического отчета
    filename = f'Отчет_Фамилия_Имя.txt'
    async with aiofiles.open(filename, mode='a', encoding='utf-8') as file:
        await file.write(message + "\n")


# Определяем обработчик события "connect"
@sio.event
async def connect():
    await write_report('Подключено к серверу Socket.IO')


async def on_move(result):
    await write_report(f'Command done: {result}')


async def perform_movement(distance_cm):
    max_speed = 0.5  # Максимальная скорость м/с (примерная, можно изменить)
    distance_m = distance_cm / 100.0  # Переводим сантиметры в метры
    time_to_travel = distance_m / max_speed

    start_time = time.time()
    while (time.time() - start_time) < time_to_travel:
        await sio.emit('command', {
            'id': 1,
            'type': "move",
            'value': {
                'x': 0,
                'y': 1,
                'sensitivity': 0.75,
            },
        }, namespace='/vehicles', callback=on_move)
        await asyncio.sleep(0.2)

    movement_message = f"Команда движения отправлена, ожидайте {time_to_travel:.2f} секунд."
    await write_report(movement_message)
    print(movement_message)
    await asyncio.sleep(time_to_travel)

    await asyncio.sleep(1)

    completion_message = f"Движение завершено: Пройденное расстояние {distance_m} м."
    await write_report(completion_message)
    print(completion_message)


async def on_spin(result):
    await write_report(f'Spin command done: {result}')


async def perform_spin_angle(angle, clockwise=True):
    FULL_ROTATION_TIME = 1.1
    ACCELERATION_FACTOR = 0.0005
    rotation_time = (angle / 360) * FULL_ROTATION_TIME
    total_time = rotation_time + (rotation_time * ACCELERATION_FACTOR)

    start_time = time.time()
    while (time.time() - start_time) < total_time:
        await sio.emit('command', {
            'id': 1,
            'type': "spin",
            'value': {
                'state': True,
                'direction': clockwise
            },
        }, namespace='/vehicles', callback=on_spin)
        await asyncio.sleep(0.2)

    spin_message = f"Начат поворот на {angle} градусов, {'по часовой стрелке' if clockwise else 'против часовой стрелки'}"
    await write_report(spin_message)
    print(spin_message)

    completion_spin_message = f"Поворот на {angle} градусов завершён."
    await write_report(completion_spin_message)
    print(completion_spin_message)


async def on_lights(result):
    await write_report(f'Lights command done: {result}')


async def control_lights(on: bool):
    # Команда для управления светом
    lights_command = {
        'id': 1,
        'type': 'lights',
        'value': on
    }

    # Отправляем команду на сервер
    await sio.emit('command', lights_command, namespace='/vehicles', callback=on_lights)

    # Записываем сообщение в файл отчета и выводим его в консоль
    action = "включены" if on else "выключены"
    message = f"Команда на включение света {action} отправлена."
    await write_report(message)
    print(message)


async def video():
    model = YOLO("Сyber-AI-drone.pt")

    # Open the video file
    video_path = "path/to/video.mp4"
    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("rtsp://192.168.10.115:8554/usb")
    # cap.release()
    # cv2.destroyAllWindows()
    # cap = cv2.VideoCapture("rtsp://192.168.10.115:8554/usb")


    # Store the track history
    track_history = defaultdict(lambda: [])

    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            # Run YOLOv8 tracking on the frame, persisting tracks between frames
            results = model.track(frame, persist=True)

            # Get the boxes and track IDs
            boxes = results[0].boxes.xywh.cpu()
            # track_ids = results[0].boxes.id.int().cpu().tolist()

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Plot the tracks
            # for box, track_id in zip(boxes, track_ids):
            #     x, y, w, h = box
            #     track = track_history[track_id]
            #     track.append((float(x), float(y)))  # x, y center point
            #     if len(track) > 30:  # retain 90 tracks for 90 frames
            #         track.pop(0)

                # Draw the tracking lines
                # points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                # cv2.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=10)

            # Display the annotated frame
            cv2.imshow("YOLOv8 Tracking", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            await asyncio.sleep(0.01)
        else:
            # Break the loop if the end of the video is reached
            break

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()
    print("session closed")


async def write_video():
    cap = cv2.VideoCapture("rtsp://192.168.10.115:8554/usb")
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output1.mp4', fourcc, 20.0, (640, 480))
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        frame = cv2.flip(frame, 90)
        # write the flipped frame
        out.write(frame)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) == ord('q'):
            break
        await asyncio.sleep(0.1)
    # Release everything if job is finished
    cap.release()
    out.release()


async def main():  # Код выполнения подключения и выполнения команд движения Ровера Контакт
    await sio.connect(server, wait_timeout=20, namespaces=['/vehicles'],
                      auth={"token": '000c2287-011a-4228-844e-e31z44b06d65'})




    await control_lights(True)
    await perform_movement(150)
    await asyncio.sleep(1)
    await perform_spin_angle(110, clockwise=True)
    # await asyncio.sleep(1)
    # await perform_movement(30)
    # await asyncio.sleep(1)
    # await perform_spin_angle(110, clockwise=True)
    # await asyncio.sleep(1)
    # await perform_movement(55)
    # await  asyncio.sleep(1)
    # await  perform_spin_angle(80, clockwise=True)
    # await  asyncio.sleep(1)
    #
    # await perform_movement(65)

    await control_lights(True)
    await  asyncio.sleep(1)
    await control_lights(False)
    await  asyncio.sleep(1)
    await control_lights(True)
    await  asyncio.sleep(1)
    await control_lights(False)
    await  asyncio.sleep(1)
    await control_lights(True)
    await  asyncio.sleep(1)
    await control_lights(False)
    await  asyncio.sleep(1)
    await control_lights(True)
    await  asyncio.sleep(1)
    await perform_movement(60)
    await  asyncio.sleep(1)
    await perform_spin_angle(110, clockwise=True)
    await  asyncio.sleep(1)
    await perform_movement(60)
    await  asyncio.sleep(1)
    await perform_spin_angle(110, clockwise=True)
    await  asyncio.sleep(1)
    await perform_movement(120)
    await  asyncio.sleep(1)
    await perform_spin_angle(110, clockwise=False)
    await  asyncio.sleep(1)
    #
    # await perform_movement(100)
    # await asyncio.sleep(1)
    # await perform_spin_angle(110, clockwise=True)
    # await asyncio.sleep(1)
    # await perform_spin_angle(110, clockwise=True)
    # await asyncio.sleep(1)
    # await perform_movement(100)
    # await asyncio.sleep(1)
    await control_lights(False)

    # yolo.stop()

    await sio.disconnect()  # Закрываем соединение после завершения всех операций


# Функция для нахождения ближайшей к заданным координатам метки
def find_closest_marker(markers, target_x, target_y):
    closest_marker = None
    min_distance = float('inf')

    for marker in markers:
        center_x = marker['center'][0]
        center_y = marker['center'][1]
        distance = np.sqrt((center_x - target_x) ** 2 + (center_y - target_y) ** 2)

        if distance < min_distance:
            closest_marker = marker
            min_distance = distance

    return closest_marker


# Функция для нахождения угла поворота камеры
def calculate_rotation_angle(marker_center, target_x):
    marker_x = marker_center[0]
    delta_x = target_x - marker_x
    focal_length = 1000  # Пример фокусного расстояния камеры

    angle_rad = np.arctan(delta_x / focal_length)
    angle_deg = np.degrees(angle_rad)

    return angle_deg


def calculate_rotation_angles(marker_center, target_x):
    marker_x = marker_center
    delta_x = target_x - marker_x
    focal_length = 1000  # Пример фокусного расстояния камеры

    angle_rad = np.arctan(delta_x / focal_length)
    angle_deg = np.degrees(angle_rad)

    return angle_deg


def aruco_detect(frame, closest_id):
    # Преобразование в оттенки серого и поиск меток
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
    parameters = cv2.aruco.DetectorParameters()
    corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is not None:
        markers = []
        mass_id_mark = []
        for i, marker_id in enumerate(ids):
            marker_center = np.mean(corners[i][0], axis=0)
            mass_id_mark.append([marker_id[0], corners[i][0]])
            markers.append({'id': marker_id[0], 'center': marker_center})

        # Находим ближайшую метку к x=360, y=10
        target_x = 960
        target_y = 1000
        closest_marker = find_closest_marker(markers, target_x, target_y)

        if closest_marker is not None:
            # closest_id = closest_marker['id']
            # closest_center = closest_marker['center']

            # Выводим информацию о найденной метке
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

            # Находим индекс первого элемента массива, у которого первый элемент равен closest_id
            y1 = 0
            y2 = 0
            ps = int(closest_id)
            for sub_arr in mass_id_mark:
                # Проверяем, если первый элемент массива равен 5
                if sub_arr[0] == ps:
                    mass = sub_arr[1]
                    y1 = int(mass[2][1])
                    y2 = int(mass[3][1])
            return y1, y2
    return 0, 0


async def main2():
    cap = cv2.VideoCapture("rtsp://localhost:8554/web")
    await sio.connect(server, wait_timeout=20, namespaces=['/vehicles'],
                      auth={"token": '000c2287-011a-4228-844e-e31z44b06d65'})
    cv2.namedWindow('Frame', cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('Frame', 640, 640)
    # while True:
    # Считывание кадра
    for i in range(1):
        _, frame = cap.read()

        # Преобразование в оттенки серого и поиск меток
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
        parameters = cv2.aruco.DetectorParameters()
        corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if ids is not None:
            markers = []
            mass_id_mark = []
            for i, marker_id in enumerate(ids):
                marker_center = np.mean(corners[i][0], axis=0)
                markers.append({'id': marker_id[0], 'center': marker_center})

            # Находим ближайшую метку к x=360, y=10
            target_x = 960
            target_y = 1000
            closest_marker = find_closest_marker(markers, target_x, target_y)

            if closest_marker is not None:
                closest_id = closest_marker['id']
                closest_center = closest_marker['center']

                await control_lights(True)

                # Выводим информацию о найденной метке
                cv2.aruco.drawDetectedMarkers(frame, corners, ids)

                # Вычисляем угол поворота камеры
                angle_deg = calculate_rotation_angle(closest_center, target_x)
                print(f"Closest marker ID: {closest_id}, Rotation angle needed: {angle_deg} degrees")
                if angle_deg < 0:
                    await perform_spin_angle(int(-angle_deg + 10), True)
                elif angle_deg > 0:
                    await perform_spin_angle(int(angle_deg + 10), False)
                time.sleep(2)

                y_start = closest_center[1]
                y_end = 1920

                # Коэффициент пропорциональности (должен быть настраиваемым в зависимости от вашей конкретной ситуации)
                pixel_to_cm_ratio = 0.017

                # Вычисление расстояния в сантиметрах
                distance_cm = abs(y_end - y_start) * pixel_to_cm_ratio

                await perform_movement(distance_cm)

                ret, frame = cap.read()
                y1, y2 = aruco_detect(frame, closest_id.T)
                if y1 == 0 and y2 == 0:
                    print("aruco is not detected")
                else:
                    angle_virav = calculate_rotation_angles(y1, y2)
                    print(f"Closest marker ID: {closest_id}, Rotation angle needed: {angle_virav} degrees")

    # Освобождение ресурсов
    cap.release()
    # cv2.destroyAllWindows()
    cv2.destroyAllWindows()


async def start():
    # Запускаем асинхронный цикл main()
    task1 = asyncio.create_task(video())
    task2 = asyncio.create_task(main())
    # task2 = asyncio.create_task(video())

    await asyncio.gather(task1, task2)
    # await task1
    # await task2


asyncio.run(start())
