CREATE DATABASE `qq_group_spider` DEFAULT CHARACTER SET = `utf8mb4`;

USE qq_group_spider;

DROP TABLE IF EXISTS `original_messages`;

CREATE TABLE `original_messages` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '消息id',
  `group_name` varchar(100) NOT NULL DEFAULT '' COMMENT 'QQ群名称（包含QQ群号码）',
  `sender_name` varchar(100) NOT NULL DEFAULT '' COMMENT '用户昵称',
  `qq_number` varchar(100) NOT NULL DEFAULT '' COMMENT 'QQ号',
  `content` text NOT NULL DEFAULT '' COMMENT '消息内容',
  `send_time` timestamp NOT NULL COMMENT '消息发布时间',
  `md5` varchar(32) NOT NULL DEFAULT '' COMMENT '每条消息的md5值',
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后一次更新时间',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `md5` (`md5`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='原始消息记录表';

DROP TABLE IF EXISTS `first_filter_keys`;

CREATE TABLE `first_filter_keys` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `key_name` varchar(100) NOT NULL DEFAULT '' COMMENT '关键词名称',
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后一次更新时间',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_name` (`key_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='一次过滤关键词表';

DROP TABLE IF EXISTS `first_filter_messages`;

CREATE TABLE `first_filter_messages` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '消息id',
  `group_name` varchar(100) NOT NULL DEFAULT '' COMMENT 'QQ群名称（包含QQ群号码）',
  `sender_name` varchar(100) NOT NULL DEFAULT '' COMMENT '用户昵称',
  `qq_number` varchar(100) NOT NULL DEFAULT '' COMMENT 'QQ号',
  `content` text NOT NULL DEFAULT '' COMMENT '消息内容',
  `send_time` timestamp NOT NULL COMMENT '消息发布时间',
  `md5` varchar(32) NOT NULL DEFAULT '' COMMENT '每条消息的md5值',
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后一次更新时间',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `md5` (`md5`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='一次过滤消息记录表';

DROP TABLE IF EXISTS `second_filter_qqnumber`;

CREATE TABLE `second_filter_qqnumber` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `qq_number` varchar(100) NOT NULL DEFAULT '' COMMENT 'QQ号码',
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后一次更新时间',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `qq_number` (`qq_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='二次过滤QQ号表';

DROP TABLE IF EXISTS `second_filter_groupnumber`;

CREATE TABLE `second_filter_groupnumber` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `group_number` varchar(100) NOT NULL DEFAULT '' COMMENT '群号码',
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后一次更新时间',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_number` (`group_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='二次过滤群号码表';

DROP TABLE IF EXISTS `second_filter_messages`;

CREATE TABLE `second_filter_messages` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '消息id',
  `group_name` varchar(100) NOT NULL DEFAULT '' COMMENT 'QQ群名称（包含QQ群号码）',
  `sender_name` varchar(100) NOT NULL DEFAULT '' COMMENT '用户昵称',
  `qq_number` varchar(100) NOT NULL DEFAULT '' COMMENT 'QQ号',
  `content` text NOT NULL DEFAULT '' COMMENT '消息内容',
  `send_time` timestamp NOT NULL COMMENT '消息发布时间',
  `md5` varchar(32) NOT NULL DEFAULT '' COMMENT '每条消息的md5值',
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后一次更新时间',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `md5` (`md5`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='二次过滤消息记录表';

DROP TABLE IF EXISTS `messages`;

CREATE TABLE `messages` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '消息id',
  `group_number` varchar(100) NOT NULL DEFAULT '' COMMENT 'QQ群号码',
  `sender_name` varchar(100) NOT NULL DEFAULT '' COMMENT '用户昵称',
  `qq_number` varchar(100) NOT NULL DEFAULT '' COMMENT 'QQ号',
  `content` text NOT NULL DEFAULT '' COMMENT '消息内容',
  `send_time` timestamp NOT NULL COMMENT '消息发布时间',
  `md5` varchar(32) NOT NULL DEFAULT '' COMMENT '每条消息的md5值',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '1：已跟进 0：待跟进 -1 已忽略',
  `operator` varchar(100) NOT NULL DEFAULT 'system' COMMENT '操作者',
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后一次更新时间',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `md5` (`md5`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='消息记录表';

