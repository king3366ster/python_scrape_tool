DROP TABLE IF EXISTS `op_corpinfo`;
CREATE TABLE `op_corpinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `cid` bigint(20) NOT NULL COMMENT '企业id',
  `nim_corp_name` varchar(128) NOT NULL COMMENT '公司名',
  `nim_corp_fullname` varchar(256) DEFAULT '' COMMENT '公司全称',
  `corp_name` varchar(128) NOT NULL COMMENT '公司名',
  `corp_fullname` varchar(256) DEFAULT '' COMMENT '公司全称',
  `similarity` double(18,14) DEFAULT 0 COMMENT '匹配相似度',
  `web_from` varchar(128) DEFAULT '' COMMENT '信息来源',
  `corp_id` varchar(128) DEFAULT '' COMMENT '信息来源记录的corp_id',
  `corp_type` varchar(128) DEFAULT '' COMMENT '公司行业',
  `corp_process` varchar(128) DEFAULT '' COMMENT '公司阶段/类型',
  `corp_number` varchar(128) DEFAULT '' COMMENT '公司规模',
  `corp_address` varchar(1024) DEFAULT '' COMMENT '公司地址',
  `corp_content` longtext DEFAULT '' COMMENT '公司详情',
  `corp_products` varchar(1024) DEFAULT '' COMMENT '公司旗下产品',
  `corp_link` varchar(256) DEFAULT '' COMMENT '公司阶段/类型',
  `corp_contact` varchar(1024) DEFAULT '' COMMENT '公司阶段/类型',
  `created_at` timestamp NOT NULL DEFAULT '2016-01-01 00:00:00',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`cid`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COMMENT='公司信息表';
