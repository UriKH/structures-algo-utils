from logger import Level, Logger


def main():
    logger = Logger('DEBUG')
    logger.set_level(Level('MSG', '>>>', '<<<', 'red', 'yellow', True))

    @logger.time()
    def func():
        sum = 0
        for i in range(10000):
            sum += i
        logger.log(f'sum is: {sum}')

    print(logger)
    print(repr(logger))
    func()


if __name__ == '__main__':
    main()