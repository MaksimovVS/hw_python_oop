from dataclasses import dataclass
from typing import Dict, Type, List, Tuple


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Возвращает строку сообщения с данными о тренировке."""

        duration: str = InfoMessage.rounding(self.duration)
        distance: str = InfoMessage.rounding(self.distance)
        speed: str = InfoMessage.rounding(self.speed)
        calories: str = InfoMessage.rounding(self.calories)
        message: str = (f"Тип тренировки: {self.training_type}; Длительность:"
                        f" {duration} ч.; Дистанция: {distance} км; Ср. "
                        f"скорость: {speed} км/ч; Потрачено ккал: {calories}.")
        return message

    @staticmethod
    def rounding(numeric: float, digit: int = 3) -> str:
        """Округляет значение до определенного знака после запятой."""
        return f"{numeric:.{digit}f}"


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        workout_type: str = type(self).__name__
        return InfoMessage(workout_type, self.duration, self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        duration_minute = self.duration * self.MIN_IN_HOUR
        spent_calories = ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                           - self.COEFF_CALORIE_2) * self.weight
                          / self.M_IN_KM * duration_minute)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029
    QUADRATIC_SPEED_FACTOR: int = 2

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

        duration_minute: float = self.duration * self.MIN_IN_HOUR
        spent_calories: float = (((self.get_mean_speed()
                                   ** self.QUADRATIC_SPEED_FACTOR
                                   // self.height) * self.COEFF_CALORIE_2
                                  * self.weight + self.COEFF_CALORIE_1
                                  * self.weight) * duration_minute)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: int = 2

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

        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.COEFF_CALORIE_1)
                * self.COEFF_CALORIE_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков, проверить валидность
    данных."""

    valid_workout_type: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    try:
        valid_workout_type[workout_type](*data)
    except KeyError:
        print(f"The unexpected importance of a sport: '{workout_type}'\n"
              f"Expected values {valid_workout_type.keys()}")

    for value in data:
        if not isinstance(value, int):
            print("\nUnexpected readings from sensors\n")
        elif value < 0:
            raise ValueError("Unexpected readings from sensors"
                             "\nValue cannot be negative")

    return (valid_workout_type[workout_type](*data))


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages: List[Tuple[str, List[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
