from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    STRING: ClassVar[str] = ('Тип тренировки: {training_type}; '
                             'Длительность: {duration:.3f} ч.; '
                             'Дистанция: {distance:.3f} км; '
                             'Ср. скорость: {speed:.3f} км/ч; '
                             'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.STRING.format(**asdict(self))


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
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Redefine method get_spent_calories() in '
                                  + self.__class__.__name__)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info: InfoMessage = InfoMessage(self.__class__.__name__,
                                        self.duration,
                                        self.get_distance(),
                                        self.get_mean_speed(),
                                        self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        run_coeff_1: int = 18
        run_coeff_2: int = 20
        run_spent_calories: float = ((run_coeff_1 * self.get_mean_speed()
                                     - run_coeff_2) * self.weight
                                     / self.M_IN_KM
                                     * self.duration * self.MIN_IN_HOUR)
        return run_spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        walk_coeff_calorie_1: float = 0.035
        walk_coeff_calorie_2: float = 0.029
        walk_spent_calories: float = (((walk_coeff_calorie_1
                                      * self.weight
                                      + (super().get_mean_speed()**2
                                       // self.height)
                                      * walk_coeff_calorie_2
                                      * self.weight) * self.duration)
                                      * self.MIN_IN_HOUR)
        return walk_spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        swim_mean_speed: float = (self.length_pool
                                  * self.count_pool
                                  / super().M_IN_KM
                                  / self.duration)
        return swim_mean_speed

    def get_spent_calories(self) -> float:
        swim_coeff_calorie_1: float = 1.1
        swim_coeff_calorie_2: int = 2
        swim_spent_calories: float = ((self.get_mean_speed()
                                      + swim_coeff_calorie_1)
                                      * swim_coeff_calorie_2
                                      * self.weight)
        return swim_spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict: dict[str, Training] = {'SWM': Swimming,
                                          'RUN': Running,
                                          'WLK': SportsWalking}
    if workout_type not in training_dict:
        raise Exception('Sorry, no such type of training')
    train: Training = training_dict[workout_type](*data)
    return train


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
