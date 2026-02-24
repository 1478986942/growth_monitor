/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80012 (8.0.12)
 Source Host           : localhost:3306
 Source Schema         : growth_monitor1

 Target Server Type    : MySQL
 Target Server Version : 80012 (8.0.12)
 File Encoding         : 65001

 Date: 24/02/2026 13:47:01
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for children
-- ----------------------------
DROP TABLE IF EXISTS `children`;
CREATE TABLE `children`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `gender` enum('male','female') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `birth_date` date NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of children
-- ----------------------------
INSERT INTO `children` VALUES (1, 2, '小明', 'male', '2020-01-01', '2026-02-22 15:29:42');
INSERT INTO `children` VALUES (2, 2, '测试儿童', 'male', '2020-01-01', '2026-02-22 15:51:48');
INSERT INTO `children` VALUES (3, 2, '测试儿童', 'male', '2020-01-01', '2026-02-22 15:52:41');
INSERT INTO `children` VALUES (4, 2, '测试儿童', 'male', '2020-01-01', '2026-02-22 15:53:45');
INSERT INTO `children` VALUES (5, 2, '测试儿童', 'male', '2020-01-01', '2026-02-22 15:54:56');
INSERT INTO `children` VALUES (6, 6, '小明', 'male', '2020-01-15', '2026-02-23 00:11:12');
INSERT INTO `children` VALUES (7, 6, '小红', 'female', '2021-05-20', '2026-02-23 00:11:12');
INSERT INTO `children` VALUES (8, 7, '小刚', 'male', '2019-08-10', '2026-02-23 00:11:12');
INSERT INTO `children` VALUES (9, 8, '小美', 'female', '2020-03-25', '2026-02-23 00:11:12');

-- ----------------------------
-- Table structure for growth_records
-- ----------------------------
DROP TABLE IF EXISTS `growth_records`;
CREATE TABLE `growth_records`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `child_id` int(11) NOT NULL,
  `record_date` date NOT NULL,
  `height` decimal(5, 2) NULL DEFAULT NULL COMMENT '单位cm',
  `weight` decimal(5, 2) NULL DEFAULT NULL COMMENT '单位kg',
  `bmi` decimal(4, 2) GENERATED ALWAYS AS ((`weight` / ((`height` / 100) * (`height` / 100)))) STORED NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `child_id`(`child_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 69 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Fixed;

-- ----------------------------
-- Records of growth_records
-- ----------------------------
INSERT INTO `growth_records` VALUES (1, 1, '2024-01-01', 100.50, 15.20, DEFAULT, '2026-02-22 15:32:50');
INSERT INTO `growth_records` VALUES (2, 1, '2024-01-01', 100.50, 15.20, DEFAULT, '2026-02-22 15:51:50');
INSERT INTO `growth_records` VALUES (3, 1, '2024-01-01', 100.50, 15.20, DEFAULT, '2026-02-22 15:52:43');
INSERT INTO `growth_records` VALUES (4, 1, '2024-01-01', 100.50, 15.20, DEFAULT, '2026-02-22 15:53:47');
INSERT INTO `growth_records` VALUES (5, 1, '2024-01-01', 100.50, 15.20, DEFAULT, '2026-02-22 15:54:58');
INSERT INTO `growth_records` VALUES (6, 1, '2020-06-29', 72.40, 9.70, DEFAULT, '2026-02-23 00:26:25');
INSERT INTO `growth_records` VALUES (7, 1, '2020-12-26', 81.40, 12.80, DEFAULT, '2026-02-23 00:26:25');
INSERT INTO `growth_records` VALUES (8, 1, '2021-06-24', 80.90, 11.00, DEFAULT, '2026-02-23 00:26:25');
INSERT INTO `growth_records` VALUES (9, 1, '2021-12-21', 90.70, 12.40, DEFAULT, '2026-02-23 00:26:25');
INSERT INTO `growth_records` VALUES (10, 1, '2022-12-16', 96.80, 14.10, DEFAULT, '2026-02-23 00:26:25');
INSERT INTO `growth_records` VALUES (11, 1, '2023-12-11', 106.20, 15.10, DEFAULT, '2026-02-23 00:26:25');
INSERT INTO `growth_records` VALUES (12, 1, '2024-12-05', 115.30, 18.10, DEFAULT, '2026-02-23 00:26:25');
INSERT INTO `growth_records` VALUES (13, 2, '2020-06-29', 75.90, 10.40, DEFAULT, '2026-02-23 00:26:25');
INSERT INTO `growth_records` VALUES (14, 2, '2020-12-26', 83.50, 12.60, DEFAULT, '2026-02-23 00:26:25');
INSERT INTO `growth_records` VALUES (15, 2, '2021-06-24', 82.10, 10.70, DEFAULT, '2026-02-23 00:26:25');
INSERT INTO `growth_records` VALUES (16, 2, '2021-12-21', 88.80, 13.00, DEFAULT, '2026-02-23 00:26:25');
INSERT INTO `growth_records` VALUES (17, 2, '2022-12-16', 97.40, 13.60, DEFAULT, '2026-02-23 00:26:25');
INSERT INTO `growth_records` VALUES (18, 2, '2023-12-11', 106.00, 15.10, DEFAULT, '2026-02-23 00:26:25');
INSERT INTO `growth_records` VALUES (19, 2, '2024-12-05', 112.70, 17.90, DEFAULT, '2026-02-23 00:26:25');
INSERT INTO `growth_records` VALUES (20, 3, '2020-06-29', 73.40, 9.70, DEFAULT, '2026-02-23 00:26:25');
INSERT INTO `growth_records` VALUES (21, 3, '2020-12-26', 83.60, 12.60, DEFAULT, '2026-02-23 00:26:25');
INSERT INTO `growth_records` VALUES (22, 3, '2021-06-24', 84.00, 11.20, DEFAULT, '2026-02-23 00:26:25');
INSERT INTO `growth_records` VALUES (23, 3, '2021-12-21', 91.00, 12.60, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (24, 3, '2022-12-16', 98.50, 13.70, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (25, 3, '2023-12-11', 103.50, 15.70, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (26, 3, '2024-12-05', 112.20, 17.90, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (27, 4, '2020-06-29', 72.00, 10.10, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (28, 4, '2020-12-26', 82.10, 12.90, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (29, 4, '2021-06-24', 82.80, 11.10, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (30, 4, '2021-12-21', 88.20, 12.70, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (31, 4, '2022-12-16', 97.00, 14.20, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (32, 4, '2023-12-11', 106.30, 15.00, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (33, 4, '2024-12-05', 114.00, 18.10, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (34, 5, '2020-06-29', 73.00, 9.60, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (35, 5, '2020-12-26', 81.70, 13.10, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (36, 5, '2021-06-24', 82.40, 10.50, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (37, 5, '2021-12-21', 90.40, 12.80, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (38, 5, '2022-12-16', 95.20, 14.40, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (39, 5, '2023-12-11', 104.30, 15.70, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (40, 5, '2024-12-05', 112.80, 18.20, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (41, 6, '2020-07-13', 73.10, 10.50, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (42, 6, '2021-01-09', 83.90, 13.00, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (43, 6, '2021-07-08', 81.30, 10.40, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (44, 6, '2022-01-04', 88.70, 12.70, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (45, 6, '2022-12-30', 95.10, 13.60, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (46, 6, '2023-12-25', 102.80, 15.90, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (47, 6, '2024-12-19', 113.10, 18.00, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (48, 7, '2021-11-16', 72.20, 8.70, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (49, 7, '2022-05-15', 80.70, 12.20, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (50, 7, '2022-11-11', 81.10, 10.20, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (51, 7, '2023-05-10', 84.30, 11.60, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (52, 7, '2024-05-04', 93.90, 13.70, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (53, 7, '2025-04-29', 100.10, 14.20, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (54, 7, '2026-04-24', 108.00, 16.50, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (55, 8, '2020-02-06', 75.60, 9.90, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (56, 8, '2020-08-04', 81.20, 12.60, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (57, 8, '2021-01-31', 81.90, 11.20, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (58, 8, '2021-07-30', 88.10, 12.20, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (59, 8, '2022-07-25', 96.60, 14.40, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (60, 8, '2023-07-20', 104.20, 15.30, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (61, 8, '2024-07-14', 114.50, 17.90, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (62, 9, '2020-09-21', 72.30, 9.20, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (63, 9, '2021-03-20', 78.80, 12.30, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (64, 9, '2021-09-16', 78.90, 10.10, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (65, 9, '2022-03-15', 87.70, 12.30, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (66, 9, '2023-03-10', 95.70, 13.40, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (67, 9, '2024-03-04', 100.60, 14.50, DEFAULT, '2026-02-23 00:26:26');
INSERT INTO `growth_records` VALUES (68, 9, '2025-02-27', 108.30, 16.50, DEFAULT, '2026-02-23 00:26:26');

-- ----------------------------
-- Table structure for hospitals
-- ----------------------------
DROP TABLE IF EXISTS `hospitals`;
CREATE TABLE `hospitals`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `department` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of hospitals
-- ----------------------------
INSERT INTO `hospitals` VALUES (1, '测试医院', '儿科', '测试地址', '12345678901', '测试描述');
INSERT INTO `hospitals` VALUES (2, '测试医院', '儿科', '测试地址', '12345678901', '测试描述');
INSERT INTO `hospitals` VALUES (3, '测试医院', '儿科', '测试地址', '12345678901', '测试描述');
INSERT INTO `hospitals` VALUES (4, '测试医院', '儿科', '测试地址', '12345678901', '测试描述');
INSERT INTO `hospitals` VALUES (5, '北京儿童医院', '生长发育科', '北京市西城区南礼士路56号', '010-59612345', '全国知名的三级甲等儿童专科医院，拥有专业的生长发育诊疗团队。');
INSERT INTO `hospitals` VALUES (6, '上海儿童医学中心', '内分泌科', '上海市浦东新区东方路1678号', '021-38626161', '国内领先的儿童医学中心，内分泌科实力雄厚。');
INSERT INTO `hospitals` VALUES (7, '广州市妇女儿童医疗中心', '儿童保健科', '广州市天河区金穗路9号', '020-81886388', '华南地区最大的妇女儿童医疗中心，儿童保健科经验丰富。');
INSERT INTO `hospitals` VALUES (8, '深圳市儿童医院', '生长发育门诊', '深圳市福田区益田路7019号', '0755-83008300', '深圳市唯一的三级甲等儿童医院，生长发育门诊专业规范。');
INSERT INTO `hospitals` VALUES (9, '浙江大学医学院附属儿童医院', '内分泌科', '杭州市下城区竹竿巷57号', '0571-87061007', '浙江省最大的儿童专科医院，内分泌科国内领先。');

-- ----------------------------
-- Table structure for interventions
-- ----------------------------
DROP TABLE IF EXISTS `interventions`;
CREATE TABLE `interventions`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `child_id` int(11) NOT NULL,
  `assessment_id` int(11) NULL DEFAULT NULL,
  `plan_title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `plan_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `start_date` date NULL DEFAULT NULL,
  `end_date` date NULL DEFAULT NULL,
  `status` enum('pending','ongoing','completed') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'pending',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `child_id`(`child_id`) USING BTREE,
  INDEX `assessment_id`(`assessment_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 20 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of interventions
-- ----------------------------
INSERT INTO `interventions` VALUES (1, 1, 1, '基于风险评估的个性化干预方案 - 2026-02-22', '【LOW - prevention】保持健康生活方式\n继续保持均衡饮食、规律作息和适量运动，定期监测生长发育情况。', '2026-02-22', '2026-05-23', 'pending', '2026-02-22 15:35:23');
INSERT INTO `interventions` VALUES (2, 1, 1, '基于风险评估的个性化干预方案 - 2026-02-22', '【LOW - prevention】保持健康生活方式\n继续保持均衡饮食、规律作息和适量运动，定期监测生长发育情况。', '2026-02-22', '2026-05-23', 'pending', '2026-02-22 15:51:56');
INSERT INTO `interventions` VALUES (3, 1, 1, '基于风险评估的个性化干预方案 - 2026-02-22', '【LOW - prevention】保持健康生活方式\n继续保持均衡饮食、规律作息和适量运动，定期监测生长发育情况。', '2026-02-22', '2026-05-23', 'pending', '2026-02-22 15:52:49');
INSERT INTO `interventions` VALUES (4, 1, 1, '基于风险评估的个性化干预方案 - 2026-02-22', '【LOW - prevention】保持健康生活方式\n继续保持均衡饮食、规律作息和适量运动，定期监测生长发育情况。', '2026-02-22', '2026-05-23', 'pending', '2026-02-22 15:53:53');
INSERT INTO `interventions` VALUES (5, 1, 1, '基于风险评估的个性化干预方案 - 2026-02-22', '【LOW - prevention】保持健康生活方式\n继续保持均衡饮食、规律作息和适量运动，定期监测生长发育情况。', '2026-02-22', '2026-05-23', 'pending', '2026-02-22 15:55:04');
INSERT INTO `interventions` VALUES (6, 1, 5, '基于风险评估的个性化干预方案 - 2026-02-23', '【HIGH - 营养干预】增加蛋白质摄入\n每日增加优质蛋白质摄入，如鸡蛋、牛奶、瘦肉等，建议每日蛋白质摄入量达到推荐标准的120%。\n\n【HIGH - 运动干预】增加户外活动\n每日保证2小时以上的户外活动，促进维生素D合成，有助于骨骼发育。\n\n【HIGH - 饮食控制】控制热量摄入\n减少高糖、高脂食物摄入，增加蔬菜水果比例，控制每日总热量摄入。\n\n【MEDIUM - 运动干预】增加有氧运动\n每日进行30-60分钟中等强度有氧运动，如游泳、跑步、骑自行车等。', '2026-02-23', '2026-05-24', 'pending', '2026-02-23 00:41:51');
INSERT INTO `interventions` VALUES (7, 2, 6, '基于风险评估的个性化干预方案 - 2026-02-23', '【LOW - 健康维护】保持健康生活方式\n继续保持良好的饮食和运动习惯，定期监测生长发育情况。', '2026-02-23', '2026-05-24', 'pending', '2026-02-23 00:41:51');
INSERT INTO `interventions` VALUES (8, 3, 7, '基于风险评估的个性化干预方案 - 2026-02-23', '【MEDIUM - 营养干预】均衡饮食\n保证每日三餐营养均衡，不挑食不偏食，适量补充维生素和矿物质。', '2026-02-23', '2026-05-24', 'pending', '2026-02-23 00:41:51');
INSERT INTO `interventions` VALUES (9, 4, 8, '基于风险评估的个性化干预方案 - 2026-02-23', '【HIGH - 营养干预】增加蛋白质摄入\n每日增加优质蛋白质摄入，如鸡蛋、牛奶、瘦肉等，建议每日蛋白质摄入量达到推荐标准的120%。\n\n【HIGH - 运动干预】增加户外活动\n每日保证2小时以上的户外活动，促进维生素D合成，有助于骨骼发育。', '2026-02-23', '2026-05-24', 'pending', '2026-02-23 00:41:51');
INSERT INTO `interventions` VALUES (10, 5, 9, '基于风险评估的个性化干预方案 - 2026-02-23', '【MEDIUM - 营养干预】均衡饮食\n保证每日三餐营养均衡，不挑食不偏食，适量补充维生素和矿物质。', '2026-02-23', '2026-05-24', 'pending', '2026-02-23 00:41:51');
INSERT INTO `interventions` VALUES (11, 6, 10, '基于风险评估的个性化干预方案 - 2026-02-23', '【MEDIUM - 营养干预】均衡饮食\n保证每日三餐营养均衡，不挑食不偏食，适量补充维生素和矿物质。', '2026-02-23', '2026-05-24', 'completed', '2026-02-23 00:41:51');
INSERT INTO `interventions` VALUES (12, 7, 11, '基于风险评估的个性化干预方案 - 2026-02-23', '【MEDIUM - 营养干预】均衡饮食\n保证每日三餐营养均衡，不挑食不偏食，适量补充维生素和矿物质。', '2026-02-23', '2026-05-24', 'pending', '2026-02-23 00:41:51');
INSERT INTO `interventions` VALUES (13, 8, 12, '基于风险评估的个性化干预方案 - 2026-02-23', '【LOW - 健康维护】保持健康生活方式\n继续保持良好的饮食和运动习惯，定期监测生长发育情况。', '2026-02-23', '2026-05-24', 'pending', '2026-02-23 00:41:51');
INSERT INTO `interventions` VALUES (14, 9, 13, '基于风险评估的个性化干预方案 - 2026-02-23', '【LOW - 健康维护】保持健康生活方式\n继续保持良好的饮食和运动习惯，定期监测生长发育情况。', '2026-02-23', '2026-05-24', 'pending', '2026-02-23 00:41:51');
INSERT INTO `interventions` VALUES (15, 1, 5, '基于风险评估的个性化干预方案 - 2026-02-24', '【LOW - prevention】保持健康生活方式\n继续保持均衡饮食、规律作息和适量运动，定期监测生长发育情况。', '2026-02-24', '2026-05-25', 'pending', '2026-02-24 05:16:04');
INSERT INTO `interventions` VALUES (16, 1, 5, '基于风险评估的个性化干预方案 - 2026-02-24', '【LOW - prevention】保持健康生活方式\n继续保持均衡饮食、规律作息和适量运动，定期监测生长发育情况。', '2026-02-24', '2026-05-25', 'pending', '2026-02-24 05:16:06');
INSERT INTO `interventions` VALUES (17, 1, 5, '基于风险评估的个性化干预方案 - 2026-02-24', '【LOW - prevention】保持健康生活方式\n继续保持均衡饮食、规律作息和适量运动，定期监测生长发育情况。', '2026-02-24', '2026-05-25', 'pending', '2026-02-24 05:16:08');
INSERT INTO `interventions` VALUES (18, 1, 5, '基于风险评估的个性化干预方案 - 2026-02-24', '【LOW - prevention】保持健康生活方式\n继续保持均衡饮食、规律作息和适量运动，定期监测生长发育情况。', '2026-02-24', '2026-05-25', 'pending', '2026-02-24 05:16:18');
INSERT INTO `interventions` VALUES (19, 3, 7, '基于风险评估的个性化干预方案 - 2026-02-24', '【LOW - prevention】保持健康生活方式\n继续保持均衡饮食、规律作息和适量运动，定期监测生长发育情况。', '2026-02-24', '2026-05-25', 'pending', '2026-02-24 05:16:23');

-- ----------------------------
-- Table structure for resources
-- ----------------------------
DROP TABLE IF EXISTS `resources`;
CREATE TABLE `resources`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` enum('nutrition','growth','health','psychology','parenting','medical','emergency','development') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `link` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 33 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of resources
-- ----------------------------
INSERT INTO `resources` VALUES (1, '0-12个月婴儿喂养指南', 'nutrition', '详细介绍婴儿从出生到12个月的喂养要点，包括母乳/配方奶喂养、辅食添加的时间和顺序、常见喂养问题的解决方法等。强调6个月内纯母乳喂养的重要性，以及如何判断婴儿是否吃饱。', 'https://www.example.com/infant-feeding', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (2, '幼儿均衡饮食金字塔', 'nutrition', '为1-3岁幼儿设计的饮食金字塔，展示各类食物的推荐摄入量。包括谷物、蔬菜、水果、蛋白质食物、奶制品的合理搭配，以及如何培养良好的饮食习惯，避免挑食偏食。', 'https://www.example.com/toddler-pyramid', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (3, '儿童零食选择指南', 'nutrition', '帮助家长选择健康的儿童零食，区分哪些是营养零食，哪些是垃圾食品。推荐适合不同年龄段的健康零食选项，以及如何控制零食摄入量，避免影响正餐食欲。', 'https://www.example.com/healthy-snacks', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (4, '生长发育期营养补充指南', 'nutrition', '介绍儿童生长发育关键期的营养需求，包括钙、维生素D、蛋白质等重要营养素的作用和食物来源。解释何时需要额外补充营养素，以及如何科学补充，避免过度补充的危害。', 'https://www.example.com/growth-nutrition', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (5, '儿童身高体重标准曲线解读', 'growth', '详细解读WHO和中国儿童生长标准曲线的使用方法，帮助家长正确评估孩子的生长状况。解释百分位的含义，以及何时需要关注孩子的生长速度异常。', 'https://www.example.com/growth-charts', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (6, '青春期生长发育指南', 'growth', '介绍男孩和女孩青春期的生长发育特点，包括身高突增期、第二性征出现的顺序和时间。解释青春期生长激素的分泌规律，以及如何通过饮食、运动和睡眠促进青春期健康成长。', 'https://www.example.com/puberty-growth', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (7, '生长激素缺乏症的早期识别', 'growth', '介绍生长激素缺乏症的常见症状和早期信号，包括生长速度缓慢、娃娃脸、脂肪堆积等。解释如何通过生长曲线监测发现异常，以及何时需要就医检查。', 'https://www.example.com/growth-hormone', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (8, '睡眠与生长发育的关系', 'growth', '详细阐述睡眠对儿童生长发育的重要性，特别是生长激素在深度睡眠中的分泌规律。提供不同年龄段儿童的推荐睡眠时间，以及如何培养良好的睡眠习惯，创造有利于生长的睡眠环境。', 'https://www.example.com/sleep-growth', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (9, '儿童常见传染病预防手册', 'health', '介绍儿童常见传染病的传播途径、症状和预防措施，包括手足口病、水痘、流感、麻疹等。强调疫苗接种的重要性，以及日常卫生习惯的培养。', 'https://www.example.com/infectious-diseases', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (10, '儿童视力保护指南', 'health', '详细介绍如何保护儿童视力，包括正确的读写姿势、电子产品使用时间控制、户外活动的重要性等。解释不同年龄段儿童的视力发育特点，以及何时需要进行视力检查。', 'https://www.example.com/eye-care', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (11, '儿童口腔健康管理', 'health', '从乳牙萌出开始的口腔护理指南，包括正确的刷牙方法、牙膏选择、定期口腔检查的重要性。介绍窝沟封闭等预防龋齿的措施，以及如何培养良好的口腔卫生习惯。', 'https://www.example.com/oral-health', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (12, '儿童过敏管理指南', 'health', '介绍儿童常见过敏原和过敏症状，包括食物过敏、花粉过敏、尘螨过敏等。提供过敏原检测的相关信息，以及如何通过环境控制和饮食管理减少过敏反应。', 'https://www.example.com/allergies', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (13, '儿童情绪管理指南', 'psychology', '帮助家长理解儿童情绪发展的特点，学习如何引导孩子认识和表达情绪。提供应对孩子发脾气、焦虑等情绪问题的有效方法，培养孩子的情绪调节能力。', 'https://www.example.com/emotion-management', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (14, '培养儿童自信心', 'psychology', '介绍如何通过积极的教育方式培养儿童的自信心，包括合理的表扬和鼓励、适当的挑战和成功体验、培养孩子的兴趣爱好等。解释过度保护和过度批评对儿童自信心的负面影响。', 'https://www.example.com/self-esteem', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (15, '儿童社交能力培养', 'psychology', '提供培养儿童社交能力的具体方法，包括如何教会孩子分享、合作、解决冲突等。介绍不同年龄段儿童的社交发展特点，以及如何帮助害羞的孩子建立社交自信。', 'https://www.example.com/social-skills', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (16, '留守儿童心理健康关怀', 'psychology', '关注留守儿童的心理健康问题，提供远程亲子沟通的有效方法，以及如何通过学校和社区支持减少留守儿童的心理问题。强调情感连接对留守儿童心理健康的重要性。', 'https://www.example.com/left-behind', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (17, '正面管教方法指南', 'parenting', '介绍正面管教的核心理念和具体方法，包括如何设定合理的规则和界限、如何使用自然后果和逻辑后果、如何进行有效的沟通等。强调尊重和理解在育儿中的重要性。', 'https://www.example.com/positive-discipline', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (18, '隔代教育的优势与挑战', 'parenting', '分析隔代教育的优势和可能存在的问题，提供祖辈和父母之间如何有效沟通和合作的建议。强调在隔代教育中保持教育一致性的重要性。', 'https://www.example.com/grandparenting', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (19, '多子女家庭的平衡之道', 'parenting', '提供在多子女家庭中如何平衡关注和资源的方法，减少兄弟姐妹之间的竞争和冲突。介绍如何培养兄弟姐妹之间的亲情和合作精神。', 'https://www.example.com/multiple-children', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (20, '数字时代的育儿挑战', 'parenting', '探讨数字时代儿童面临的挑战，包括屏幕时间管理、网络安全、数字成瘾等问题。提供建立家庭数字使用规则的具体建议，以及如何利用数字工具促进儿童学习。', 'https://www.example.com/digital-parenting', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (21, '儿童发热的正确处理', 'medical', '详细介绍儿童发热的原因、体温测量方法、何时需要使用退烧药、何时需要就医等。解释发热对儿童的保护作用，以及如何区分普通发热和需要紧急处理的发热情况。', 'https://www.example.com/fever-management', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (22, '儿童用药安全指南', 'medical', '强调儿童用药的注意事项，包括剂量计算、药物选择、副作用监测等。提供常见儿童用药的使用方法和注意事项，以及如何避免药物误用。', 'https://www.example.com/medication-safety', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (23, '儿童常见腹痛原因分析', 'medical', '介绍儿童常见腹痛的原因，包括功能性腹痛、肠系膜淋巴结炎、蛔虫病等。提供腹痛的观察要点和何时需要就医的指导，以及家庭护理建议。', 'https://www.example.com/abdominal-pain', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (24, '儿童疫苗接种全攻略', 'medical', '提供详细的儿童疫苗接种时间表，包括一类疫苗和二类疫苗的接种建议。解释疫苗的作用原理、接种后的常见反应及处理方法，以及疫苗接种的注意事项。', 'https://www.example.com/vaccination-guide', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (25, '儿童心肺复苏术', 'emergency', '详细介绍儿童心肺复苏的操作步骤和注意事项，包括判断意识、开放气道、人工呼吸、胸外按压的正确方法。提供不同年龄段儿童的CPR操作差异，以及自动体外除颤器(AED)的使用方法。', 'https://www.example.com/cpr-for-children', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (26, '儿童异物卡喉急救', 'emergency', '介绍儿童异物卡喉的识别方法和海姆立克急救法的正确操作。提供针对不同年龄段儿童的急救措施，以及如何预防异物卡喉的发生。', 'https://www.example.com/choking-first-aid', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (27, '儿童烧烫伤急救处理', 'emergency', '详细介绍儿童烧烫伤的急救步骤，包括冲、脱、泡、盖、送的五字原则。解释不同程度烧烫伤的判断标准，以及何时需要紧急就医。', 'https://www.example.com/burn-first-aid', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (28, '儿童溺水急救指南', 'emergency', '介绍儿童溺水的急救方法，包括现场救援、控水、心肺复苏等。提供溺水后的观察要点，以及如何预防儿童溺水事故的发生。', 'https://www.example.com/drowning-first-aid', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (29, '0-3岁儿童早期教育指南', 'development', '基于儿童发展里程碑，提供0-3岁儿童早期教育的具体建议，包括语言、运动、认知、社交等方面的发展促进方法。强调游戏在早期教育中的重要性。', 'https://www.example.com/early-education', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (30, '培养儿童专注力', 'development', '介绍如何通过科学的方法培养儿童的专注力，包括创造有利于专注的环境、选择适合儿童年龄的任务、使用番茄工作法等。解释电子产品对儿童专注力的影响，以及如何合理使用。', 'https://www.example.com/attention-span', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (31, '儿童创造力开发', 'development', '提供培养儿童创造力的具体方法，包括鼓励儿童表达自己的想法、提供开放性的材料和活动、引导儿童进行想象和探索等。解释过度指导对儿童创造力的负面影响。', 'https://www.example.com/creativity', '2026-02-24 12:30:28');
INSERT INTO `resources` VALUES (32, '儿童学习能力培养', 'development', '介绍如何培养儿童的学习兴趣和学习能力，包括建立良好的学习习惯、使用有效的学习方法、创造积极的学习环境等。提供针对不同学习风格儿童的教育建议。', 'https://www.example.com/learning-ability', '2026-02-24 12:30:28');

-- ----------------------------
-- Table structure for risk_assessments
-- ----------------------------
DROP TABLE IF EXISTS `risk_assessments`;
CREATE TABLE `risk_assessments`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `child_id` int(11) NOT NULL,
  `assessment_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `stunting_risk` decimal(5, 2) NULL DEFAULT NULL COMMENT '矮小症风险概率%',
  `obesity_risk` decimal(5, 2) NULL DEFAULT NULL COMMENT '肥胖风险概率%',
  `details` json NULL COMMENT '详细风险因子',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `child_id`(`child_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of risk_assessments
-- ----------------------------
INSERT INTO `risk_assessments` VALUES (1, 1, '2026-02-22 15:33:07', 5.00, 25.49, '{\"obesity\": {\"bmi\": 15.05, \"risk\": 26.0, \"status\": \"normal\", \"age_months\": 48, \"percentile\": 20}, \"stunting\": {\"risk\": 5, \"height\": 100.5, \"status\": \"normal\", \"age_months\": 48, \"percentile\": 100}, \"risk_factors\": []}');
INSERT INTO `risk_assessments` VALUES (2, 1, '2026-02-22 15:51:54', 5.00, 25.49, '{\"obesity\": {\"bmi\": 15.05, \"risk\": 26.0, \"status\": \"normal\", \"age_months\": 48, \"percentile\": 20}, \"stunting\": {\"risk\": 5, \"height\": 100.5, \"status\": \"normal\", \"age_months\": 48, \"percentile\": 100}, \"risk_factors\": []}');
INSERT INTO `risk_assessments` VALUES (3, 1, '2026-02-22 15:52:47', 5.00, 25.49, '{\"obesity\": {\"bmi\": 15.05, \"risk\": 26.0, \"status\": \"normal\", \"age_months\": 48, \"percentile\": 20}, \"stunting\": {\"risk\": 5, \"height\": 100.5, \"status\": \"normal\", \"age_months\": 48, \"percentile\": 100}, \"risk_factors\": []}');
INSERT INTO `risk_assessments` VALUES (4, 1, '2026-02-22 15:53:51', 5.00, 25.49, '{\"obesity\": {\"bmi\": 15.05, \"risk\": 26.0, \"status\": \"normal\", \"age_months\": 48, \"percentile\": 20}, \"stunting\": {\"risk\": 5, \"height\": 100.5, \"status\": \"normal\", \"age_months\": 48, \"percentile\": 100}, \"risk_factors\": []}');
INSERT INTO `risk_assessments` VALUES (5, 1, '2026-02-22 15:55:02', 5.00, 25.49, '{\"obesity\": {\"bmi\": 15.05, \"risk\": 26.0, \"status\": \"normal\", \"age_months\": 48, \"percentile\": 20}, \"stunting\": {\"risk\": 5, \"height\": 100.5, \"status\": \"normal\", \"age_months\": 48, \"percentile\": 100}, \"risk_factors\": []}');
INSERT INTO `risk_assessments` VALUES (6, 2, '2026-02-23 00:39:15', 0.17, 0.29, '{\"bmi\": 14.09, \"height\": 112.7, \"weight\": 17.9, \"age_months\": 60, \"recommendation\": \"建议定期监测生长发育情况，保持均衡饮食和适量运动\"}');
INSERT INTO `risk_assessments` VALUES (7, 3, '2026-02-23 00:39:15', 0.24, 0.27, '{\"bmi\": 14.22, \"height\": 112.2, \"weight\": 17.9, \"age_months\": 60, \"recommendation\": \"建议定期监测生长发育情况，保持均衡饮食和适量运动\"}');
INSERT INTO `risk_assessments` VALUES (8, 4, '2026-02-23 00:39:15', 0.31, 0.15, '{\"bmi\": 13.93, \"height\": 114.0, \"weight\": 18.1, \"age_months\": 60, \"recommendation\": \"建议定期监测生长发育情况，保持均衡饮食和适量运动\"}');
INSERT INTO `risk_assessments` VALUES (9, 5, '2026-02-23 00:39:15', 0.24, 0.28, '{\"bmi\": 14.3, \"height\": 112.8, \"weight\": 18.2, \"age_months\": 60, \"recommendation\": \"建议定期监测生长发育情况，保持均衡饮食和适量运动\"}');
INSERT INTO `risk_assessments` VALUES (10, 6, '2026-02-23 00:39:15', 0.27, 0.30, '{\"bmi\": 14.07, \"height\": 113.1, \"weight\": 18.0, \"age_months\": 60, \"recommendation\": \"建议定期监测生长发育情况，保持均衡饮食和适量运动\"}');
INSERT INTO `risk_assessments` VALUES (11, 7, '2026-02-23 00:39:15', 0.30, 0.19, '{\"bmi\": 14.15, \"height\": 108.0, \"weight\": 16.5, \"age_months\": 60, \"recommendation\": \"建议定期监测生长发育情况，保持均衡饮食和适量运动\"}');
INSERT INTO `risk_assessments` VALUES (12, 8, '2026-02-23 00:39:15', 0.16, 0.25, '{\"bmi\": 13.65, \"height\": 114.5, \"weight\": 17.9, \"age_months\": 60, \"recommendation\": \"建议定期监测生长发育情况，保持均衡饮食和适量运动\"}');
INSERT INTO `risk_assessments` VALUES (13, 9, '2026-02-23 00:39:15', 0.14, 0.20, '{\"bmi\": 14.07, \"height\": 108.3, \"weight\": 16.5, \"age_months\": 60, \"recommendation\": \"建议定期监测生长发育情况，保持均衡饮食和适量运动\"}');
INSERT INTO `risk_assessments` VALUES (14, 1, '2026-02-24 05:22:14', 5.00, 27.55, '{\"obesity\": {\"bmi\": 13.62, \"risk\": 28.0, \"status\": \"normal\", \"age_months\": 59, \"percentile\": 10}, \"stunting\": {\"risk\": 5, \"height\": 115.3, \"status\": \"normal\", \"age_months\": 59, \"percentile\": 100}, \"risk_factors\": []}');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'parent',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE,
  UNIQUE INDEX `phone`(`phone`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'testuser', 'scrypt:32768:8:1$6OAKWctuTQXKwXdq$f8796560013d441bca64b87f0476e0620923f8affb3c6aee072cd09b9028f67d62810b45e78801bef35f09319e8984b3589ad42c200b9c928b42eb13aa3638b0', 'test@example.com', NULL, 'parent', '2026-02-22 13:13:34');
INSERT INTO `users` VALUES (2, 'admin', 'scrypt:32768:8:1$t3XC5da34bHHPyk6$36db64228fae1c827afb982483037d7dee4b85e14112b443e5b50a9cfa2fb150f2635b7431402f4f231d0b37d1ecc41e9666355388c285501625860a29496c6a', 'admin@example.com', NULL, 'admin', '2026-02-22 21:23:08');
INSERT INTO `users` VALUES (3, 'doctor1', 'scrypt:32768:8:1$NFlA1QlK3juHpVYr$22951adb790ad3ba0ed7f0da00f92882480405ef012b73ec051e01ca8e7a7fd6df870e6af00d0f971ee9f3c608dce9625ab33c36714efafc5cb332a9cb99aea8', 'doctor1@example.com', '13800138000', 'doctor', '2026-02-22 13:23:48');
INSERT INTO `users` VALUES (4, 'doctor2', 'scrypt:32768:8:1$CfNBt6QzviHMpx3v$cb835a1bfaaf6db31ccac57954ccdd4264663464627f88ecb256868065fdb94f8f2f6a9b966c5900fcc93c441d860388fe626e4c76b09b0e31c0499099512340', 'doctor2@example.com', '13800001002', 'doctor', '2026-02-23 00:09:44');
INSERT INTO `users` VALUES (5, 'doctor3', 'scrypt:32768:8:1$BFhMi8pHmNJKx2re$da879b111f9b4e40275231c2a29c70d1203603cbe935fca7c344d4c9ddd1066876f8ce7502605dfcd61798e6e925140491bbf94b12de6bab59226777889ada6b', 'doctor3@example.com', '13800001003', 'doctor', '2026-02-23 00:09:44');
INSERT INTO `users` VALUES (6, 'parent1', 'scrypt:32768:8:1$CfNBt6QzviHMpx3v$cb835a1bfaaf6db31ccac57954ccdd4264663464627f88ecb256868065fdb94f8f2f6a9b966c5900fcc93c441d860388fe626e4c76b09b0e31c0499099512340', 'parent1@example.com', '13800002001', 'parent', '2026-02-23 00:09:44');
INSERT INTO `users` VALUES (7, 'parent2', 'scrypt:32768:8:1$CfNBt6QzviHMpx3v$cb835a1bfaaf6db31ccac57954ccdd4264663464627f88ecb256868065fdb94f8f2f6a9b966c5900fcc93c441d860388fe626e4c76b09b0e31c0499099512340', 'parent2@example.com', '13800002002', 'parent', '2026-02-23 00:09:44');
INSERT INTO `users` VALUES (8, 'parent3', 'scrypt:32768:8:1$CfNBt6QzviHMpx3v$cb835a1bfaaf6db31ccac57954ccdd4264663464627f88ecb256868065fdb94f8f2f6a9b966c5900fcc93c441d860388fe626e4c76b09b0e31c0499099512340', 'parent3@example.com', '13800002003', 'parent', '2026-02-23 00:09:44');
INSERT INTO `users` VALUES (9, 'msd', 'scrypt:32768:8:1$koKiEE0bnhbh9gzn$887df0d3e7f043fc9c20d045417eb2bb6af8d76db5a61d1cd0830149c99838c1614823c70b81941052480e6b5556d75a402b6a077a76b5252680df42e41bd6cc', '1478986942@qq.com', '19167637459', 'parent', '2026-02-24 05:02:53');

-- ----------------------------
-- Table structure for verification_codes
-- ----------------------------
DROP TABLE IF EXISTS `verification_codes`;
CREATE TABLE `verification_codes`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `code` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `expires_at` timestamp NOT NULL,
  `used` tinyint(1) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of verification_codes
-- ----------------------------
INSERT INTO `verification_codes` VALUES (1, 'test@example.com', '998340', '2026-02-22 15:26:12', '2026-02-22 15:31:12', 0);
INSERT INTO `verification_codes` VALUES (2, 'test@example.com', '541829', '2026-02-22 15:27:21', '2026-02-22 15:32:21', 0);
INSERT INTO `verification_codes` VALUES (3, 'test@example.com', '950141', '2026-02-22 15:28:15', '2026-02-22 15:33:15', 0);
INSERT INTO `verification_codes` VALUES (4, '1478986942@qq.com', '215158', '2026-02-24 05:02:11', '2026-02-24 05:07:11', 1);

SET FOREIGN_KEY_CHECKS = 1;
