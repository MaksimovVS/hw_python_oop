class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
    
   

    def get_message(self) -> str:
        """Возвращает строку сообщения с данными о тренировке."""

        duration = rounding(self.duration)
        #duration = 15.0.rounding()
        distance = rounding(self.distance)
        speed = rounding(self.speed)
        calories = rounding(self.calories)
        message = (f"Тип тренировки: {self.training_type}; Длительность: "
                   f"{duration} ч.; Дистанция: {distance} км; Ср. скорость: "
                   f"{speed} км/ч; Потрачено ккал: {calories}.")
        return message


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        workout_type = type(self).__name__
        return InfoMessage(workout_type, self.duration, self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1 = 18
    COEFF_CALORIE_2 = 20

    def get_spent_calories(self) -> float:
        duration_minute = self.duration * self.MIN_IN_HOUR
        spent_calories = ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                           - self.COEFF_CALORIE_2) * self.weight
                          / self.M_IN_KM * duration_minute)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_1 = 0.035
    COEFF_CALORIE_2 = 0.029
    QUADRATIC_SPEED_FACTOR = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        duration_minute = self.duration * self.MIN_IN_HOUR
        spent_calories = (((self.get_mean_speed()
                            ** self.QUADRATIC_SPEED_FACTOR // self.height)
                           * self.COEFF_CALORIE_2 * self.weight
                           + self.COEFF_CALORIE_1 * self.weight)
                          * duration_minute)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    COEFF_CALORIE_1 = 1.1
    COEFF_CALORIE_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight,)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        mean_speed = (self.length_pool * self.count_pool / self.M_IN_KM
                      / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        spent_calories = ((self.get_mean_speed() + self.COEFF_CALORIE_1)
                          * self.COEFF_CALORIE_2 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков, проверить валидность
    данных."""

    dict_workout_type = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    
    if workout_type not in dict_workout_type:
        raise ValueError("The unexpected importance of a sport:",
        workout_type)
    for value in data:
        value_str = str(value)
        if not value_str.isdigit():
            raise ValueError("Unexpected readings from sensors")

    return (dict_workout_type.get(workout_type)(*data))


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


def rounding(numeric: float, digit: int = 3) -> str:
    """Округляет значение до определенного знака после запятой."""

    return f"{numeric:.{digit}f}"


if __name__ == "__main__":
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)


''' #@staticmethod
    def rounding(numeric: float, digit: int = 3) -> str:
        """Округляет значение до определенного знака после запятой."""
        return f"{numeric:.{digit}f}"'''