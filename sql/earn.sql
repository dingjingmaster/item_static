alter database item_earn default character set utf8;

use item_earn;

CREATE TABLE IF NOT EXISTS `item_earn` (
    `id` VARCHAR(320) NOT NULL                      COMMENT '主键,app-valuetype-timestamp',
    `app` INT(12) DEFAULT 0 NOT NULL                COMMENT '1.宜搜　2.微卷',
    `value_type` INT(12) DEFAULT 0 NOT NULL         COMMENT '1.总收益　2.人均收益',
    `value` VARCHAR(32) DEFAULT 0 NOT NULL          COMMENT '值',
    `time_stamp` INT(12) DEFAULT 0 NOT NULL         COMMENT '时间戳'
);


