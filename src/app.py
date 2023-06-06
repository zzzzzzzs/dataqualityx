import yaml
import os
import DateUtil
import argparse
import AlterUtil
import DbUtil


def print_color_text(text, color):
    """
    打印指定颜色的文本

    :param text: 要打印的文本
    :param color: 要设置的文本颜色，可选值为'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white'
    """
    colors = {
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'purple': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
    }
    end_color = '\033[0m'
    if color in colors:
        print(colors[color] + text + end_color)
    else:
        print(text)


# 处理符号
def operator(expected):
    # 处理后的期望数据
    exps = []
    # 目前只支持对比数字
    for row in expected:
        row = row['row']
        if len(row.split(' ')) < 2:
            raise Exception(f'请检查 expected: {row}')
        exps.append((row.split(' ')[0], row.split(' ')[1]))
    return exps


# 符号处理，结果返回 bool
# =、>、>=、<、<=、!=
def symbol_proc(x, y):
    if y[0] == '=':
        return x == int(y[1])
    elif y[0] == '>':
        return x > int(y[1])
    elif y[0] == '>=':
        return x >= int(y[1])
    elif y[0] == '<':
        return x < int(y[1])
    elif y[0] == '<=':
        return x <= int(y[1])
    elif y[0] == '!=':
        return x != int(y[1])
    else:
        raise Exception(f'无法处理符号 {int(y[1])}')


# 对比结果
def compareResult(actual, file_name, sql, task, args):
    if len(actual) != len(task['expected']):
        raise Exception(f'{file_name} 中的 {task["sql"]} 期望是 {len(task["expected"])} 行，但实际是 {len(actual)} 行')
    exps = operator(task['expected'])
    if exps is None:
        raise Exception(f'期望值不应该为 None')
    for x, y in zip(actual, exps):
        if len(x) > 1:
            raise Exception(f'目前只支持校验一个字段值，文件: {file_name}')
        calc_res = symbol_proc(x[0], y)
        if calc_res == False:
            err_info = f'错误xxx: 文件:{file_name} 中的 {sql} 计算出问题了, 实际结果是 {actual}, 但期望是 {task["expected"]}'
            print_color_text(err_info, 'red')
            if 'none' in args.alerts: continue
            if task['alerts'] is not None:
                for alert in task['alerts']:
                    alert = alert['alert']
                    AlterUtil.alter(alert['type'], err_info, alert['url'])
        else:
            print(f'文件:{file_name} 中的 {sql} 与期望值相同')
        print('--------------------------------------------')


# 读取 yaml 中的数据
def read_yaml(args):
    current_path = os.path.abspath(".")
    yaml_path = os.path.join(current_path, "../task")
    infos = []
    for filename in os.listdir(yaml_path):
        # 支持命令行指定文件,如果不写就是全部
        if args.files is None or filename in args.files:
            if filename.endswith('.yaml'):
                with open(os.path.join(yaml_path, filename), encoding='utf-8') as f:
                    yaml_data = yaml.safe_load(f)
                    yaml_data['file_name'] = filename
                    infos.append(yaml_data)
    return infos


# 处理 sql 变量
def handle_sql(sql, vars):
    for var in vars:
        var1 = var['var'].split('=')[0].strip()
        var2 = var['var'].split('=')[1].strip()
        sql = sql.replace(var1, DateUtil.dateTemplateParse(var2))
    return sql


# 处理 yaml 逻辑
def process(infos, args):
    # infos -> 多个文件
    for info in infos:
        if info['db'] is None:
            raise Exception(f'文件 {info["file_name"]} 中的数据库没有配置')
        # 创建数据库连接
        cur = DbUtil.db(info['db'])
        for task in info['tasks']:
            task = task['task']
            if task['sql'] is None or task['sql'] == '':
                raise Exception(f'{info["file_name"]} 中 sql 部分不能为空')
            sql = handle_sql(task['sql'], info['vars'])
            actualRes = DbUtil.query(cur, sql)
            compareResult(actualRes, info["file_name"], sql, task, args)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', dest='files', nargs='+', help='YAML files to process')
    parser.add_argument('--alerts', dest='alerts', nargs='+', help='YAML alerts to process')
    args = parser.parse_args()
    yaml_infos = read_yaml(args)
    process(yaml_infos, args)


if __name__ == '__main__':
    main()
