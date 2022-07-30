M_IN_KM = 1000
MIN_IN_HOUR = 60
print('Начало')


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 info: str,
                 ) -> None:
        self.info = info


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 LEN_STEP: float = 0.65) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.LEN_STEP = LEN_STEP

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = training.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        print(training.get_distance())
        print(training.get_mean_speed())
        print(training.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        duration_minute = self.duration * MIN_IN_HOUR
        spent_calories = ((coeff_calorie_1 * training.get_mean_speed() -
                           coeff_calorie_2) * self.weight /
                          M_IN_KM * duration_minute)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 2
        coeff_calorie_3 = 0.029
        duration_minute = self.duration * MIN_IN_HOUR
        spent_calories = (((training.get_mean_speed() ** coeff_calorie_2 //
                           self.height) * coeff_calorie_3 * self.weight +
                          coeff_calorie_1 * self.weight) * duration_minute)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 LEN_STEP: float = 1.38,
                 ) -> None:
        super().__init__(action, duration, weight, LEN_STEP)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool / M_IN_KM /
                      self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        spent_calories = ((training.get_mean_speed() + coeff_calorie_1) *
                          coeff_calorie_2 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_workout_type = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    return dict_workout_type.get(workout_type)(*data)


def main(training: Training) -> None:
    """Главная функция."""
    temp = training.show_training_info()
    info = InfoMessage(temp)
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
print('Конец')
