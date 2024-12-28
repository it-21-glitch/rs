-- 用户
CREATE TABLE IF NOT EXISTS user
(
    id     INTEGER PRIMARY KEY,
    name   TEXT    NOT NULL,
    passwd INTEGER NOT NULL
)

-- 材质
CREATE TABLE IF NOT EXISTS material
(
    id            INTEGER PRIMARY KEY,
    material_name TEXT NOT NULL
)
-- 工序
CREATE TABLE IF NOT EXISTS process
(
    id           INTEGER PRIMARY KEY,
    process_name TEXT    NOT NULL,
    material_id  INTEGER NOT NULL,
    FOREIGN KEY (material_id) REFERENCES material (id) ON DELETE CASCADE ON UPDATE NO ACTION
)
-- 设备
CREATE TABLE IF NOT EXISTS equipment
(
    id                      INTEGER PRIMARY KEY,
    process_id              INTEGER NOT NULL, -- 关联字段

    equipment_name          TEXT    NOT NULL, -- 设备名称

    equipment_number        INTEGER NOT NULL, -- 设备数量 3
    max_people_number       INTEGER NOT NULL, -- 最大人数 常备人数 4
    min_people_number       INTEGER NOT NULL, -- 最小人数 饱和人数 6

    classes_capacity_big    INTEGER NOT NULL, --  班次最大规格产能
    classes_capacity_middle INTEGER NOT NULL, --  班次中等规格产能
    classes_capacity_small  INTEGER NOT NULL, --  班次最小规格产能

    day_classes_frequency   INTEGER NOT NULL, -- 最大班次
    classes_man_hour        INTEGER NOT NULL, -- 每个班次工时
    day_classes_man_hour    INTEGER NOT NULL, -- 班次  * 工时 = 当天的工时


    day_capacity_big        INTEGER NOT NULL, -- 日产大号 = 班次大号产能 * 最大班次
    day_capacity_middle     INTEGER NOT NULL, -- 日产中号
    day_capacity_small      INTEGER NOT NULL, -- 日产小号

    FOREIGN KEY (process_id) REFERENCES process (id) ON DELETE CASCADE ON UPDATE NO ACTION
)
-- 记录表,不链表设置
CREATE TABLE IF NOT EXISTS record_sheet
(
    id                 INTEGER PRIMARY KEY,
    entry_time         TEXT    NOT NULL,            -- 记录时间
    po                 TEXT    NOT NULL,            -- po号
    item               TEXT    NOT NULL,            -- item号
    specification_name TEXT    NOT NULL,            -- 规格
    material_name      TEXT    NOT NULL,            -- 材质id
    process_name       TEXT    NOT NULL,            -- 工序
    equipment_name     TEXT    NOT NULL,            -- 设备
    people_number      INTEGER NOT NULL,            -- 人数
    output_number      INTEGER NOT NULL,            -- 数量
    examine_status     INTEGER NOT NULL DEFAULT 0,  -- 审核状态 1 通过 0 拒绝
    examine_time       TEXT             DEFAULT '', -- 审核时间
    attendance_picture TEXT    NOT NULL,            -- 考勤图片
)

-- 工厂用户表 要求需要进行自定义添加
CREATE TABLE IF NOT EXISTS factory_user
(
    id        INTEGER PRIMARY KEY,
    user_name TEXT    NOT NULL,
    user_age  INTEGER NOT NULL,
)
-- 考勤记录表
CREATE TABLE IF NOT EXISTS factory_attendance_user
(
    id              INTEGER PRIMARY KEY,
    user_id         INTEGER NOT NULL,
    record_sheet_id INTEGER NOT NULL,
    start_time      TEXT    NOT NULL,
    end_time        TEXT    NOT NULL,
    user_pay        INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES factory_user (id) ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY (record_sheet_id) REFERENCES record_sheet (id) ON DELETE CASCADE ON UPDATE NO ACTION,
)