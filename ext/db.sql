-- phpMyAdmin SQL Dump
-- version 4.6.6deb5ubuntu0.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 16, 2021 at 11:54 AM
-- Server version: 10.1.48-MariaDB-0ubuntu0.18.04.1
-- PHP Version: 7.2.24-0ubuntu0.18.04.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `asahi`
--

-- --------------------------------------------------------

--
-- Table structure for table `achievements`
--

CREATE TABLE `achievements` (
                                `id` int(11) NOT NULL,
                                `image` text NOT NULL,
                                `name` text NOT NULL,
                                `descr` text NOT NULL,
                                `cond` text NOT NULL,
                                `custom` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `channels`
--

CREATE TABLE `channels` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `descr` text NOT NULL,
  `auto` int(11) NOT NULL DEFAULT '1',
  `perm` int(11) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `clans`
--

CREATE TABLE `clans` (
  `id` int(11) NOT NULL,
  `name` varchar(16) NOT NULL,
  `tag` text NOT NULL,
  `owner` int(11) NOT NULL,
  `score` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `friends`
--

CREATE TABLE `friends` (
  `user1` int(11) NOT NULL,
  `user2` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `maps`
--

CREATE TABLE `maps` (
  `id` bigint(20) NOT NULL,
  `sid` bigint(20) NOT NULL,
  `md5` char(32) NOT NULL,
  `bpm` float NOT NULL,
  `cs` float NOT NULL,
  `ar` float NOT NULL,
  `od` float NOT NULL,
  `hp` float NOT NULL,
  `sr` float NOT NULL,
  `mode` int(11) NOT NULL,
  `artist` text NOT NULL,
  `title` text NOT NULL,
  `diff` text NOT NULL,
  `mapper` text NOT NULL,
  `status` int(11) NOT NULL,
  `frozen` int(11) NOT NULL,
  `update` bigint(20) NOT NULL,
  `nc` bigint(20) NOT NULL DEFAULT '0',
  `plays` int(11) NOT NULL DEFAULT '0',
  `passes` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `punishments`
--

CREATE TABLE `punishments` (
  `id` int(11) NOT NULL,
  `type` text NOT NULL,
  `reason` text NOT NULL,
  `target` int(11) NOT NULL,
  `from` int(11) NOT NULL,
  `time` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `requests`
--

CREATE TABLE `requests` (
  `id` int(11) NOT NULL,
  `requester` text NOT NULL,
  `map` bigint(20) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `scores`
--

CREATE TABLE `scores` (
  `id` int(11) NOT NULL,
  `md5` char(32) NOT NULL,
  `score` bigint(20) NOT NULL,
  `acc` float NOT NULL,
  `pp` float NOT NULL,
  `combo` int(11) NOT NULL,
  `mods` int(11) NOT NULL,
  `n300` int(11) NOT NULL,
  `geki` int(11) NOT NULL,
  `n100` int(11) NOT NULL,
  `katu` int(11) NOT NULL,
  `n50` int(11) NOT NULL,
  `miss` int(11) NOT NULL,
  `grade` char(1) NOT NULL DEFAULT 'F',
  `status` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `time` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  `readable_mods` text NOT NULL,
  `fc` int(11) NOT NULL,
  `osuver` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `scores_ap`
--

CREATE TABLE `scores_ap` (
  `id` int(11) NOT NULL,
  `md5` char(32) NOT NULL,
  `score` bigint(20) NOT NULL,
  `acc` float NOT NULL,
  `pp` float NOT NULL,
  `combo` int(11) NOT NULL,
  `mods` int(11) NOT NULL,
  `n300` int(11) NOT NULL,
  `geki` int(11) NOT NULL,
  `n100` int(11) NOT NULL,
  `katu` int(11) NOT NULL,
  `n50` int(11) NOT NULL,
  `miss` int(11) NOT NULL,
  `grade` char(1) NOT NULL DEFAULT 'F',
  `status` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `time` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  `readable_mods` text NOT NULL,
  `fc` int(11) NOT NULL,
  `osuver` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `scores_rx`
--

CREATE TABLE `scores_rx` (
  `id` int(11) NOT NULL,
  `md5` char(32) NOT NULL,
  `score` bigint(20) NOT NULL,
  `acc` float NOT NULL,
  `pp` float NOT NULL,
  `combo` int(11) NOT NULL,
  `mods` int(11) NOT NULL,
  `n300` int(11) NOT NULL,
  `geki` int(11) NOT NULL,
  `n100` int(11) NOT NULL,
  `katu` int(11) NOT NULL,
  `n50` int(11) NOT NULL,
  `miss` int(11) NOT NULL,
  `grade` char(1) NOT NULL DEFAULT 'F',
  `status` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `time` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  `readable_mods` text NOT NULL,
  `fc` int(11) NOT NULL,
  `osuver` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `stats`
--

CREATE TABLE `stats` (
  `id` bigint(20) NOT NULL,
  `rscore_std` bigint(20) NOT NULL DEFAULT '0',
  `acc_std` double NOT NULL DEFAULT '0',
  `pc_std` bigint(20) NOT NULL DEFAULT '0',
  `tscore_std` bigint(20) NOT NULL DEFAULT '0',
  `pp_std` bigint(20) NOT NULL DEFAULT '0',
  `rscore_mania` bigint(20) NOT NULL DEFAULT '0',
  `acc_mania` double NOT NULL DEFAULT '0',
  `pc_mania` bigint(20) NOT NULL DEFAULT '0',
  `tscore_mania` bigint(20) NOT NULL DEFAULT '0',
  `rscore_catch` bigint(20) NOT NULL DEFAULT '0',
  `acc_catch` double NOT NULL DEFAULT '0',
  `pc_catch` bigint(20) NOT NULL DEFAULT '0',
  `tscore_catch` bigint(20) NOT NULL DEFAULT '0',
  `rscore_taiko` bigint(20) NOT NULL DEFAULT '0',
  `acc_taiko` double NOT NULL DEFAULT '0',
  `pc_taiko` bigint(20) NOT NULL DEFAULT '0',
  `tscore_taiko` bigint(20) NOT NULL DEFAULT '0',
  `pp_taiko` bigint(20) NOT NULL DEFAULT '0',
  `pp_catch` bigint(20) NOT NULL DEFAULT '0',
  `pp_mania` bigint(20) NOT NULL DEFAULT '0',
  `rscore_catch_rx` bigint(20) NOT NULL DEFAULT '0',
  `acc_catch_rx` double NOT NULL DEFAULT '0',
  `pc_catch_rx` bigint(20) NOT NULL DEFAULT '0',
  `tscore_catch_rx` bigint(20) NOT NULL DEFAULT '0',
  `rscore_taiko_rx` bigint(20) NOT NULL DEFAULT '0',
  `acc_taiko_rx` double NOT NULL DEFAULT '0',
  `pc_taiko_rx` bigint(20) NOT NULL DEFAULT '0',
  `tscore_taiko_rx` bigint(20) NOT NULL DEFAULT '0',
  `rscore_std_ap` bigint(20) NOT NULL DEFAULT '0',
  `acc_std_ap` double NOT NULL DEFAULT '0',
  `pc_std_ap` bigint(20) NOT NULL DEFAULT '0',
  `tscore_std_ap` bigint(20) NOT NULL DEFAULT '0',
  `rscore_std_rx` bigint(20) NOT NULL DEFAULT '0',
  `acc_std_rx` double NOT NULL DEFAULT '0',
  `pc_std_rx` bigint(20) NOT NULL DEFAULT '0',
  `tscore_std_rx` bigint(20) NOT NULL DEFAULT '0',
  `pp_std_rx` bigint(20) NOT NULL DEFAULT '0',
  `pp_std_ap` bigint(20) NOT NULL DEFAULT '0',
  `pp_taiko_rx` bigint(20) NOT NULL DEFAULT '0',
  `pp_catch_rx` bigint(20) NOT NULL DEFAULT '0',
  `mc_std` bigint(20) NOT NULL DEFAULT '0',
  `mc_std_rx` bigint(20) NOT NULL DEFAULT '0',
  `mc_std_ap` bigint(20) NOT NULL DEFAULT '0',
  `mc_taiko` bigint(20) NOT NULL DEFAULT '0',
  `mc_taiko_rx` bigint(20) NOT NULL DEFAULT '0',
  `mc_catch` bigint(20) NOT NULL DEFAULT '0',
  `mc_catch_rx` bigint(20) NOT NULL DEFAULT '0',
  `mc_mania` bigint(20) NOT NULL DEFAULT '0',
  `pt_std` bigint(20) NOT NULL DEFAULT '0',
  `pt_std_rx` bigint(20) NOT NULL DEFAULT '0',
  `pt_std_ap` bigint(20) NOT NULL DEFAULT '0',
  `pt_taiko` bigint(20) NOT NULL DEFAULT '0',
  `pt_taiko_rx` bigint(20) NOT NULL DEFAULT '0',
  `pt_catch` bigint(20) NOT NULL DEFAULT '0',
  `pt_catch_rx` bigint(20) NOT NULL DEFAULT '0',
  `pt_mania` bigint(20) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(16) NOT NULL,
  `email` varchar(32) NOT NULL,
  `pw` text NOT NULL,
  `country` char(2) NOT NULL DEFAULT 'xx',
  `priv` int(11) NOT NULL DEFAULT '1',
  `safe_name` varchar(16) NOT NULL,
  `clan` int(11) NOT NULL DEFAULT '0',
  `freeze_timer` bigint(20) NOT NULL DEFAULT '0',
  `registered_at` bigint(20) NOT NULL,
  `silence_end` bigint(20) NOT NULL DEFAULT '0',
  `donor_end` bigint(20) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user_achievements`
--

CREATE TABLE `user_achievements` (
  `id` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  `ach` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user_hashes`
--

CREATE TABLE `user_hashes` (
  `uid` int(11) NOT NULL,
  `mac_address` varchar(32) NOT NULL,
  `uninstall_id` varchar(32) NOT NULL,
  `disk_serial` varchar(32) NOT NULL,
  `ip` varchar(32) NOT NULL,
  `occurrences` bigint(20) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `achievements`
--
ALTER TABLE `achievements`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `channels`
--
ALTER TABLE `channels`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `clans`
--
ALTER TABLE `clans`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `friends`
--
ALTER TABLE `friends`
  ADD PRIMARY KEY (`user1`,`user2`);

--
-- Indexes for table `maps`
--
ALTER TABLE `maps`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `md5` (`md5`);

--
-- Indexes for table `punishments`
--
ALTER TABLE `punishments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `requests`
--
ALTER TABLE `requests`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `scores`
--
ALTER TABLE `scores`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `scores_ap`
--
ALTER TABLE `scores_ap`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `scores_rx`
--
ALTER TABLE `scores_rx`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `stats`
--
ALTER TABLE `stats`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_achievements`
--
ALTER TABLE `user_achievements`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uid` (`uid`,`ach`);

--
-- Indexes for table `user_hashes`
--
ALTER TABLE `user_hashes`
  ADD UNIQUE KEY `uid` (`uid`,`mac_address`,`uninstall_id`,`disk_serial`,`ip`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `achievements`
--
ALTER TABLE `achievements`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `channels`
--
ALTER TABLE `channels`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `clans`
--
ALTER TABLE `clans`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `punishments`
--
ALTER TABLE `punishments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `requests`
--
ALTER TABLE `requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `scores`
--
ALTER TABLE `scores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `scores_ap`
--
ALTER TABLE `scores_ap`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `scores_rx`
--
ALTER TABLE `scores_rx`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `stats`
--
ALTER TABLE `stats`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `user_achievements`
--
ALTER TABLE `user_achievements`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
