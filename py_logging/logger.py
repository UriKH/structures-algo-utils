import time
import os
import traceback
from termcolor import colored


class Level:
    def __init__(self, name: str, prefix: str = None, suffix: str = '', color: str = 'white', background_color: str = None, show_time: bool = True):
        self.name = name
        self.prefix = f'[{self.name}] ' if prefix is None else prefix
        self.suffix = suffix
        self.color = color
        self.background_color = f'on_{background_color}' if background_color else None
        self.show_time = show_time

class Logger(Level):
    logging = {
        'DEBUG': Level('DEBUG', color='red'),
        'DEFAULT': Level('DEFAULT', prefix='')
    }
    
    def __init__(self, level: str | Level, file: str = ''):
        self.file = file

        if isinstance(level, Level):
            self.add_level(level)
            self.level = level.name
        else:
            self.level = level

    def __str__(self) -> str:
        return f'Logger level: {self.level}, to file: {self.file if self.file else 'standard output'}'
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}<{self.level}, {self.file if self.file else None}>'

    def add_level(self, level: Level):
        if level.name in Logger.logging:
            raise ValueError('Level name already exists')
        self.logging[level.name] = level
    
    def set_level(self, level: str | Level):
        if isinstance(level, Level):
            self.add_level(level)
            self.level = level.name
        else:
            self.level = level
    
    def write_to_file(self, file, text):
        if not os.path.exists(file):
            raise FileExistsError(f'File {file} does not exists')
        with open(file, 'a+') as fd:
            fd.write(text)

    def format_log(self, msg: str, color: bool = True) -> str:
        level = self.logging.get(self.level, None)
        if level:
            try:
                if color:
                    return colored(f'{level.prefix} {msg} {level.suffix}', level.color, level.background_color)
                return f'{level.prefix} {msg} {level.suffix}'
            except KeyError:
                raise ValueError(f'Color: {level.color}, or background color: {level.background_color} is undefined')
        raise ValueError('Level not defined')

    def time(self, file: str = ''):
        file = file if file else self.file

        def decorator(func):
            def wrapper(*args, **kwargs):
                strt = time.time()
                value = func(*args, **kwargs)
                end = time.time()

                if not self.logging[self.level].show_time:
                    return value

                msg = f'{func.__name__} time: {end - strt:.5f} seconds'

                try:
                    self.log(msg, file)
                    return value
                except:
                    traceback.print_exc()
            return wrapper
        return decorator
    
    def log(self, msg: str, file: str = None):
        if file:
            self.write_to_file(file, self.format_log(msg, color=False))
        else:
            print(self.format_log(msg))