import re
import pendulum

DATE_PARSE_PATTERN = re.compile(r"\$\[([^\$\]]+)]")
DATE_START_PATTERN = re.compile(r"^[0-9]")


def calc_time(key, date):
    if "+" in key:
        index = key.rfind('+')

        if key[index + 1:].isdigit():
            add_expr = key[index + 1:]
            date_format = key[:index]
            return date.add(days=int(add_expr)).format(date_format.upper())
    elif "-" in key:
        index = key.rfind('-')
        if key[index + 1:].isdigit():
            add_expr = key[index + 1:]
            date_format = key[:index]
            return date.subtract(days=int(add_expr)).format(date_format.upper())
        return date.format(key.upper())
    else:
        raise Exception(f'无法解析 {key}')


def dateTemplateParse(templateStr):
    match = DATE_PARSE_PATTERN.match(templateStr)
    if match:
        key = match.group(1)
        date = pendulum.now()
        return calc_time(key, date)

if __name__ == '__main__':
    print(dateTemplateParse('$[yyyy-MM-dd]'))