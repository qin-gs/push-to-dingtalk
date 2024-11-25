drop table if exists tbl_xwlb;
create table tbl_xwlb (
    id int,
    date varchar(25),
    image_url varchar(255),
    tags varchar(255),
    abstract varchar(255),
    content text,
    video_url varchar(255)
);

alter table tbl_xwlb modify column id com

-- 添加注释
comment on table tbl_xwlb is '新闻联播';
comment on column tbl_xwlb.id is '序号';
comment on column tbl_xwlb.date is '日期';
comment on column tbl_xwlb.image_url is '图像 url';
comment on column tbl_xwlb.tags is '内容标签，用空格分隔';
comment on column tbl_xwlb.abstract is '摘要';
comment on column tbl_xwlb.content is '详细内容';
comment on column tbl_xwlb.video_url is '视频完整url';

drop table if exists tbl_jdft;
create table tbl_jdft
(
    date      varchar(25),
    title     varchar(255),
    tags      varchar(255),
    image_url varchar(255),
    content   text,
    video_url varchar(255),
    guid      varchar(255),
    primary key (date)
);

-- 添加注释
comment on table tbl_jdft is '焦点访谈';
comment on column tbl_jdft.date is '日期';
comment on column tbl_jdft.title is '标题';
comment on column tbl_jdft.image_url is '图片地址';
comment on column tbl_jdft.content is '详细内容';
comment on column tbl_jdft.video_url is '视频完整url';
comment on column tbl_jdft.guid is '内容 id';
comment on column tbl_jdft.tags is '内容标签，用空格分隔';




drop table if exists tbl_jrsf;
create table tbl_jrsf
(
    date      varchar(25),
    title     varchar(255),
    tags      varchar(255),
    image_url varchar(255),
    content   text,
    video_url varchar(255),
    guid      varchar(255),
    primary key (date)
);

-- 添加注释
comment on table tbl_jrsf is '今日说法';
comment on column tbl_jrsf.date is '日期';
comment on column tbl_jrsf.title is '标题';
comment on column tbl_jrsf.image_url is '图片地址';
comment on column tbl_jrsf.content is '详细内容';
comment on column tbl_jrsf.video_url is '视频完整url';
comment on column tbl_jrsf.guid is '内容 id';
comment on column tbl_jrsf.tags is '内容标签，用空格分隔';

