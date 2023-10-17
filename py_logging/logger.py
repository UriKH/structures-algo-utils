import time
import os
import traceback
from termcolor import colored
from datetime import datetime


class Level:
    def __init__(self, name: str, prefix: str = None, suffix: str = '', color: str = 'white',
                 background_color: str = None, show_time: bool = True, show_pref_time: bool = True):
        """
        Construct a Logging Level representation
        :param name: the level name
        :param prefix: level's message prefix
        :param suffix: level's message suffix
        :param color: color of the text
        :param background_color: color of the message's background
        :param show_time: log the time of the logging
        :param show_pref_time: log the preformance time of chosen functions
        """
        self.__name = name
        self.__prefix = f'[{self.__name}] ' if prefix is None else prefix
        self.__suffix = suffix
        self.__color = color
        self.__background_color = f'on_{background_color}' if background_color else None
        self.__show_time = show_time
        self.__show_pref_time = show_pref_time
    
    @property
    def name(self):
        return self.__name
    
    @property
    def prefix(self):
        return self.__prefix
    
    @property
    def suffix(self):
        return self.__suffix
    
    @property
    def color(self):
        return self.__color
    
    @property
    def background_color(self):
        return self.__background_color
    
    @property
    def show_time(self):
        return self.__show_time
    
    @property
    def show_pref_time(self):
        return self.__show_pref_time


class Logger:
    __logging = {
        'DEBUG': Level('DEBUG', color='red'),
        'DEFAULT': Level('DEFAULT', prefix='')
    }
    
    def __init__(self, level: str | Level, file: str = ''):
        """
        Construct a Logger representation
        :param level: the logging level
        :param file: file to output logging messages into
        """
        self.__file = file

        if isinstance(level, Level):
            self.add_level(level)
            self.__level = level.name
        else:
            self.__level = level

    def __str__(self) -> str:
        return f'Logger level: {self.__level}, to file: {self.__file if self.__file else 'standard output'}'
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(level={self.__level}, file={self.__file if self.__file else None})'

    def __format_log(self, msg: str, color: bool = True) -> str:
        """
        Format the logging message according to the relevant logging level
        :param msg: the message to log
        :param color: if True, add color to the message
        :return: the formatted message
        """
        level = Logger.__logging.get(self.__level, None)
        if level:
            try:
                if level.show_time:
                    msg = f'[{datetime.now().strftime("%H:%M:%S")}] ' + msg 
                if color:
                    return colored(f'{level.prefix} {msg} {level.suffix}', level.color, level.background_color)
                return f'{level.prefix} {msg} {level.suffix}'
            except KeyError:
                raise ValueError(f'Color: {level.color}, or background color: {level.background_color} is undefined')
        raise ValueError('Level not defined')

    @staticmethod
    def __write_to_file(file: str, text: str):
        """
        Write logging message to a file
        :param file: the path to the file
        :param text: the logging message
        """
        if not os.path.exists(file):
            raise FileExistsError(f'File {file} does not exists')
        with open(file, 'a+') as fd:
            fd.write(text)

    @staticmethod
    def add_level(level: Level):
        """
        Add a new logging level
        :param level: a new level object
        """
        if level.name in Logger.__logging:
            raise ValueError('Level name already exists')
        Logger.__logging[level.name] = level
    
    def set_level(self, level: str | Level):
        """
        Set the logging level to an existing or new level
        :param level: the logging level
        """
        if isinstance(level, Level):
            self.add_level(level)
            self.__level = level.name
        else:
            self.__level = level

    def time(self, file: str = ''):
        """
        Function timer decorator
        :param file: the name of the file to print to
        :return: the decorated function
        """
        file = file if file else self.__file

        def decorator(func):
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                value = func(*args, **kwargs)
                end = time.perf_counter()

                if not Logger.__logging[self.__level].show_pref_time:
                    return value

                msg = f'PREF TIME: {func.__name__}: {end - start:.5f} sec(s)'

                try:
                    self.log(msg, file)
                    return value
                except:
                    traceback.print_exc()
            return wrapper
        return decorator
    
    def log(self, msg: str, file: str = None):
        """
        Log a message to the given output (standard output / file)
        :param msg: message to log
        :param file: path to a file to log to
        """
        if file:
            self.__write_to_file(file, self.__format_log(msg, color=False))
        else:
            print(self.__format_log(msg))
