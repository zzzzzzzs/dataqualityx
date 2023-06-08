# DataQuality
[![Total Lines](https://tokei.rs/b1/github/zzzzzzzs/DataQuality?category=lines)](https://github.com/zzzzzzzs/DataQuality)

## 快速开始
```shell
pip install dataqualityx
```
多文件任务
```shell
dataqualityx --files C:\warehouse\user\task
```
单文件任务
```shell
dataqualityx --files C:\warehouse\user\task\dws_test.yaml
```

## 脚本编写
```yaml
db:
  type: doris
  host: "127.0.0.1"
  port: 9030
  user: "admin"
  pw: "xxx"
  db: "ods"
vars:
  - var: "${dt} = $[yyyy-MM-dd-1]"
tasks:
    - task:
      sql: |
        -- 校验 dws_test 表中前一天的数据是否存在
        select count(1) from dws.dws_test
        where dt = '${dt}'
      expected:
        - row: "> 0"
      alert:
    - task:
      sql: |
        -- 校验 dws_test 表中4种类型是否存在数据
        select count(1)
        from dws.dws_test
        where dt = '${dt}'
        group by type
        order by type
      expected:
        - row: "> 0"
        - row: "> 0"
        - row: "> 0"
        - row: "> 0"
      alert:
```

## 支持命令
- `--files /home/users/xxx` : 支持指定文件路径 (必填)
- `--alerts none` : 支持全局禁止报警

## 支持数据库
- [x] mysql
- [x] doris
- [ ] hive
- [ ] clickhouse
- [ ] clickhouse
- [ ] postgresql

