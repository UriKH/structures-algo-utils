import time
import os
import sys
import traceback
import re
from termcolor import colored
from datetime import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class Level:
    """
    Representation of a Logging Level
    :param name: the level name
    :param prefix: level's message prefix
    :param suffix: level's message suffix
    :param color: color of the text
    :param background_color: color of the message's background
    :param show_time: log the time of the logging
    :param show_pref_time: log the preformance time of chosen functions
    :param simplified: flag for simplified logging
    :param seperators
    :param begin_msg
    """
    name: str
    prefix: str = ''
    suffix: str = ''
    color: str = 'white'
    background_color: str | None = None
    show_time: bool  = True
    show_pref_time: bool = True
    simplified: bool = False


class Logger:
    __logging = {
        'DEBUG': Level('DEBUG', color='red'),
        'DEFAULT': Level('DEFAULT')
    }
    
    def __init__(self, level: str | Level, file: str = '', new_file: bool = True):
        """
        Construct a Logger representation
        :param level: the logging level
        :param file: file to output logging messages into
        :param new_file: create new file in path
        """
        self.__file = file
        self.__new_file = new_file
        self.__file_created = False
        
        if isinstance(level, Level):
            self.add_level(level)
            self.__level = level.name
        else:
            if level not in Logger.__logging.keys():
                raise ValueError(f'Level {level} is undefined')
            self.__level = level 
        
    def __str__(self) -> str:
        return f'Logger level: {self.__level}, to file: {self.__file if self.__file else 'standard output'}'
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(level={self.__level}, file={self.__file if self.__file else None}, new_file={self.__new_file})'

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
                    msg = self.__get_foramted_time()[0] + msg
                msg = ' ' + msg
                if msg[-1] != '\n':
                    msg += ' '
                if not level.suffix and msg[-1] == '\n':
                    msg = msg[:-1]
                if color:
                    return colored(Logger.__remove_ws_chars(level.prefix) + msg + Logger.__remove_ws_chars(level.suffix), 
                                   level.color, level.background_color if not level.background_color else 'on_' + level.background_color)
                return Logger.__remove_ws_chars(level.prefix) + msg + Logger.__remove_ws_chars(level.suffix)
            except KeyError:
                raise ValueError(f'Color: {level.color}, or background color: {level.background_color} is undefined')
        raise ValueError(f'Level {level} is undefined')

    def __write_to_file(self, file: str, text: str):
        """
        Write logging message to a file
        :param file: the path to the file
        :param text: the logging message
        """
        if self.__new_file and os.path.exists(file) and not self.__file_created:
            raise FileExistsError(f'File {file} already exists')
        with open(file, 'a') as fd:
            self.__file_created = True
            fd.write(f'{text}\n')

    def __indent_msg(self, msg: str) -> str:
        """
        Indent a message according to the time string representation and the level's prefix
        :return: the indented message
        """
        if '\n' not in msg:
            return msg
        level = Logger.__logging[self.__level]
        buff = len(level.prefix) + 1
        if level.show_time:
            buff += self.__get_foramted_time()[1]
        return '\n'.join([(msg := msg.replace('\t', '    ')).split('\n')[0]] + [' ' * buff + line for line in msg.split('\n')[1:]])    

    def __get_foramted_time(self) -> (str, int):
        """
        Create a string representation of the current time
        :return: the time string representation and its length
        """
        time_str = f'[{datetime.now().strftime("%H:%M:%S")}] '
        return time_str, len(time_str) 

    @staticmethod
    def __remove_ws_chars(s: str) -> str:
        """
        Removes all white space characters from the string except ' '
        :return: the cleaned string
        """
        return re.sub(r'[\t\n\r]', ' ', s)
    
    @staticmethod
    def __format_arg(arg) -> str:
        """
        Find the best string representation of a given object
        :return: the string representation
        """
        if isinstance(arg, str):
            return f'"{arg}"'
        elif hasattr(arg, '__str__'):
            return str(arg)
        elif hasattr(arg, '__repr__'):
            return repr(arg)
        else:
            return f'{arg.__class__.__name__} unrepresentable object'

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

    def pref(self, *, file: str = ''):
        """
        Function preformance decorator
        :param file: the name of the file to print to
        :return: the decorated function
        """
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

    def log_func(self, *, file: str = '', detailed: bool = False):
        """
        Function logging decorator
        :param file: the name of the file to print to
        :return: the decorated function
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                value = func(*args, **kwargs)
                end = time.perf_counter()

                args = ' ,'.join([self.__format_arg(arg) for arg in args])
                kwargs = ' ,'.join([f'{k}: {self.__format_arg(v)}' for k, v in kwargs.items()])
                msg = f'FUNCTION: {func.__name__} => {value}'
                if Logger.__logging[self.__level].show_pref_time or detailed:
                    msg += f' | in {end - start:.5f} sec(s)'
                if not Logger.__logging[self.__level].simplified or detailed:
                    msg += f'\nINFO: args   = [{args}]\n      kwargs = {{{fr"{kwargs}"}}}'
                    msg = self.__indent_msg(msg)
                    msg += '\n'
                try:
                    self.log(msg, file, indent=False)
                    return value
                except:
                    traceback.print_exc()
            return wrapper
        return decorator

    def log(self, msg: str, file: str = '', *, indent: bool = True):
        """
        Log a message to the given output (standard output / file)
        :param msg: message to log
        :param file: path to a file to log to
        :param indent: indent the message
        """
        if indent:
            msg = self.__indent_msg(msg)
        if (file := file if file else self.__file):
            self.__write_to_file(file, self.__format_log(msg, color=False))
        else:
            print(self.__format_log(msg))