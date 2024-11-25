drop table if exists tbl_xwlb;
create table tbl_xwlb (
    id int comment '新闻联播',
    date varchar(25) comment '序号',
    image_url varchar(255) comment '日期',
    tags varchar(255) comment '图像 url',
    abstract varchar(255) comment '内容标签，用空格分隔',
    content text comment '摘要',
    video_url varchar(255) comment '详细内容',
    index date_index(date)
) comment '新闻联播';

drop table if exists tbl_jdft;
create table tbl_jdft
(
    date      varchar(25) comment '焦点访谈',
    title     varchar(255) comment '日期',
    tags      varchar(255) comment '标题',
    image_url varchar(255) comment '图片地址',
    content   text comment '详细内容',
    video_url varchar(255) comment '视频完整url',
    guid      varchar(255) comment '内容 id',
    primary key (date)
) comment '焦点访谈';


drop table if exists tbl_jrsf;
create table tbl_jrsf
(
    date      varchar(25) comment '今日说法',
    title     varchar(255) comment '日期',
    tags      varchar(255) comment '标题',
    image_url varchar(255) comment '图片地址',
    content   text comment '详细内容',
    video_url varchar(255) comment '视频完整url',
    guid      varchar(255) comment '内容 id',
    primary key (date)
) comment '今日说法';

