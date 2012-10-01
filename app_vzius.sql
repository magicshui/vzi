-- phpMyAdmin SQL Dump
-- version 3.3.8.1
-- http://www.phpmyadmin.net
--
-- 主机: w.rdc.sae.sina.com.cn:3307
-- 生成日期: 2012 年 10 月 01 日 17:10
-- 服务器版本: 5.5.23
-- PHP 版本: 5.2.9

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `app_vzius`
--

-- --------------------------------------------------------

--
-- 表的结构 `lines_list`
--

CREATE TABLE IF NOT EXISTS `lines_list` (
  `id` varchar(20) NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `crt_time` datetime DEFAULT NULL,
  `content` text,
  `movie_id` varchar(20) DEFAULT NULL,
  `cut` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `movie_list`
--

CREATE TABLE IF NOT EXISTS `movie_list` (
  `id` varchar(20) NOT NULL,
  `title` varchar(30) DEFAULT NULL,
  `alt_title` varchar(30) DEFAULT NULL,
  `image` varchar(200) DEFAULT NULL,
  `alt` varchar(200) DEFAULT NULL,
  `summary` text,
  `source_data` text,
  `back` varchar(200) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `sys_list`
--

CREATE TABLE IF NOT EXISTS `sys_list` (
  `crt_time` datetime NOT NULL,
  `douban` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`crt_time`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `user_list`
--

CREATE TABLE IF NOT EXISTS `user_list` (
  `name` varchar(30) DEFAULT NULL,
  `come` varchar(30) DEFAULT NULL,
  `id` varchar(30) NOT NULL,
  `crt_time` datetime DEFAULT NULL,
  `avatar` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
