DROP TABLE IF EXISTS `sp_lagou`;
CREATE TABLE `sp_lagou` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `corp_id` varchar(128) NOT NULL COMMENT '原网站id',
  `corp_name` varchar(128) NOT NULL COMMENT '公司名',
  `corp_fullname` varchar(128) DEFAULT '' COMMENT '公司全称',
  `corp_type` varchar(128) DEFAULT '' COMMENT '公司行业',
  `corp_process` varchar(128) DEFAULT '' COMMENT '公司阶段/类型',
  `corp_number` varchar(128) DEFAULT '' COMMENT '公司规模',
  `corp_address` varchar(1024) DEFAULT '' COMMENT '公司地址',
  `corp_content` longtext DEFAULT '' COMMENT '公司详情',
  `corp_products` varchar(1024) DEFAULT '' COMMENT '公司旗下产品',
  `corp_link` varchar(256) DEFAULT '' COMMENT '公司阶段/类型',
  `corp_contact` varchar(1024) DEFAULT '' COMMENT '公司阶段/类型',
  `created_at` datetime NOT NULL DEFAULT '2016-01-01 00:00:00',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`corp_id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COMMENT='公司信息表';

DROP TABLE IF EXISTS `sp_itjuzi`;
CREATE TABLE `sp_itjuzi` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `corp_id` varchar(128) NOT NULL COMMENT '原网站id',
  `corp_name` varchar(128) NOT NULL COMMENT '公司名',
  `corp_fullname` varchar(128) DEFAULT '' COMMENT '公司全称',
  `corp_type` varchar(128) DEFAULT '' COMMENT '公司行业',
  `corp_process` varchar(128) DEFAULT '' COMMENT '公司阶段/类型',
  `corp_number` varchar(128) DEFAULT '' COMMENT '公司规模',
  `corp_address` varchar(1024) DEFAULT '' COMMENT '公司地址',
  `corp_content` longtext DEFAULT '' COMMENT '公司详情',
  `corp_products` varchar(1024) DEFAULT '' COMMENT '公司旗下产品',
  `corp_link` varchar(256) DEFAULT '' COMMENT '公司阶段/类型',
  `corp_contact` varchar(1024) DEFAULT '' COMMENT '公司阶段/类型',
  `created_at` datetime NOT NULL DEFAULT '2016-01-01 00:00:00',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`corp_id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COMMENT='公司信息表';

DROP TABLE IF EXISTS `sp_51job`;
CREATE TABLE `sp_51job` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `corp_id` varchar(128) NOT NULL COMMENT '原网站id',
  `corp_name` varchar(128) NOT NULL COMMENT '公司名',
  `corp_fullname` varchar(128) DEFAULT '' COMMENT '公司全称',
  `corp_type` varchar(128) DEFAULT '' COMMENT '公司行业',
  `corp_process` varchar(128) DEFAULT '' COMMENT '公司阶段/类型',
  `corp_number` varchar(128) DEFAULT '' COMMENT '公司规模',
  `corp_address` varchar(1024) DEFAULT '' COMMENT '公司地址',
  `corp_content` longtext DEFAULT '' COMMENT '公司详情',
  `corp_products` varchar(1024) DEFAULT '' COMMENT '公司旗下产品',
  `corp_link` varchar(256) DEFAULT '' COMMENT '公司阶段/类型',
  `corp_contact` varchar(1024) DEFAULT '' COMMENT '公司阶段/类型',
  `created_at` datetime NOT NULL DEFAULT '2016-01-01 00:00:00',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`corp_id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COMMENT='公司信息表';

DROP TABLE IF EXISTS `sp_58tc`;
CREATE TABLE `sp_58tc` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `corp_id` varchar(128) NOT NULL COMMENT '原网站id',
  `corp_name` varchar(128) NOT NULL COMMENT '公司名',
  `corp_fullname` varchar(128) DEFAULT '' COMMENT '公司全称',
  `corp_type` varchar(128) DEFAULT '' COMMENT '公司行业',
  `corp_process` varchar(128) DEFAULT '' COMMENT '公司阶段/类型',
  `corp_number` varchar(128) DEFAULT '' COMMENT '公司规模',
  `corp_address` varchar(1024) DEFAULT '' COMMENT '公司地址',
  `corp_content` longtext DEFAULT '' COMMENT '公司详情',
  `corp_products` varchar(1024) DEFAULT '' COMMENT '公司旗下产品',
  `corp_link` varchar(256) DEFAULT '' COMMENT '公司阶段/类型',
  `corp_contact` varchar(1024) DEFAULT '' COMMENT '公司阶段/类型',
  `created_at` datetime NOT NULL DEFAULT '2016-01-01 00:00:00',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`corp_id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COMMENT='公司信息表';

DROP TABLE IF EXISTS `sp_zhaopin`;
CREATE TABLE `sp_zhaopin` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `corp_id` varchar(128) NOT NULL COMMENT '原网站id',
  `corp_name` varchar(128) NOT NULL COMMENT '公司名',
  `corp_fullname` varchar(128) DEFAULT '' COMMENT '公司全称',
  `corp_type` varchar(128) DEFAULT '' COMMENT '公司行业',
  `corp_process` varchar(128) DEFAULT '' COMMENT '公司阶段/类型',
  `corp_number` varchar(128) DEFAULT '' COMMENT '公司规模',
  `corp_address` varchar(1024) DEFAULT '' COMMENT '公司地址',
  `corp_content` longtext DEFAULT '' COMMENT '公司详情',
  `corp_products` varchar(1024) DEFAULT '' COMMENT '公司旗下产品',
  `corp_link` varchar(256) DEFAULT '' COMMENT '公司阶段/类型',
  `corp_contact` varchar(1024) DEFAULT '' COMMENT '公司阶段/类型',
  `created_at` datetime NOT NULL DEFAULT '2016-01-01 00:00:00',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`corp_id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COMMENT='公司信息表';
