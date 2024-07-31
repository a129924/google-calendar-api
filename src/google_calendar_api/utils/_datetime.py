from datetime import datetime


def get_date_string(
    date_format: str,
    datetime: datetime = datetime.now(),
) -> str:
    """
    以指定的格式返回日期字符串。

    Args:
        date_format (str): 日期格式字符串，使用 `strftime` 格式代碼。
            以下是一些常用的格式代碼：
                %Y: 4位數字表示的年份，例如 2024
                %m: 2位數字表示的月份，01-12
                %d: 2位數字表示的日期，01-31
                %H: 2位數字表示的24小時制的時，00-23
                %I: 2位數字表示的12小時制的時，01-12
                %M: 2位數字表示的分鐘，00-59
                %S: 2位數字表示的秒，00-59
                %f: 微秒，000000-999999
                %p: AM 或 PM
                %z: 時區偏移，+HHMM 或 -HHMM
                %Z: 時區名稱
                %a: 簡化星期名稱，例如 Mon
                %A: 完整星期名稱，例如 Monday
                %b: 簡化月份名稱，例如 Jan
                %B: 完整月份名稱，例如 January
                %c: 本地化日期和時間表示，例如 Tue Aug 16 21:30:00 1988
                %x: 本地化的日期表示，例如 08/16/88 (沒有時間部分)
                %X: 本地化的時間表示，例如 21:30:00 (沒有日期部分)
        datetime (datetime, optional): 要格式化的 datetime 對象，默認為當前時間。

    Returns:
        str: 以指定格式返回的日期字符串。

    Examples:
        >>> get_date_string("%Y-%m-%d %H:%M:%S")
        '2024-07-15 14:35:22'

        >>> get_date_string("%A, %B %d, %Y")
        'Monday, July 15, 2024'
    """
    return datetime.strftime(date_format)
