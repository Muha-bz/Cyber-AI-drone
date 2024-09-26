from ultralytics import YOLO

# Загрузка модели
model = YOLO("cyber-ai-drone.pt")

# Трекинг объектов в видео
results = model.track(source="2.mp4", show=True)

# Порог уверенности для включения в отчёт
confidence_threshold = 0.5

# Создаем файл для отчета
with open("detection_report.txt", "w") as report_file:
    for frame_idx, result in enumerate(results):
        object_count = {}  # Словарь для хранения количества объектов каждого класса в кадре
        
        # Проходим по объектам в кадре
        for box in result.boxes:
            confidence = box.conf.item()
            if confidence >= confidence_threshold:
                obj_class = box.cls.item()  # Класс объекта
                
                # Считаем количество объектов каждого класса
                if obj_class in object_count:
                    object_count[obj_class] += 1
                else:
                    object_count[obj_class] = 1
        
        # Записываем результаты для кадра, если есть распознанные объекты
        if object_count:
            report_file.write(f"Frame {frame_idx}:\n")
            for obj_class, count in object_count.items():
                report_file.write(f"  Object class {obj_class}: {count} instances\n")

print("Отчет успешно создан: detection_report.txt")
