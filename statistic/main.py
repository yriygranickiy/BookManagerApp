from app_statistic.controllers import controllers
from app_statistic.service import consumer_service


def main():
    consumer_service.get_message()


if __name__ == '__main__':
    main()