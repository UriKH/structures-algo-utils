from logger import Level, Logger


def main():
    logger = Logger('DEBUG')
    logger.set_level(Level('MSG', '>>> ', '<<<', 'red', 'yellow', show_pref_time=True, show_time=True, simplified=False))

    @logger.log_func(detailed=True)
    def sigma(x: float):
        val = sum(range(x))
        logger.log(f'sum is: {val}')
        return val
    
    print(logger)
    sigma(1000)
    

if __name__ == '__main__':
    main()