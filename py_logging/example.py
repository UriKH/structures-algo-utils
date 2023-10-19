from logger import Level, Logger


def main():
    logger = Logger('DEFAULT', new_file=False)
    logger.set_level(Level('MSG', '>', '<', 'blue', 'yellow', show_pref_time=True, show_time=True, simplified=True))

    @logger.log_func(detailed=True)
    def sigma(x: float):
        val = sum(range(x))
        logger.log(f'sum is:\n\t{val}')
        return val
    
    print(logger)
    sigma(1000)
    

if __name__ == '__main__':
    main()