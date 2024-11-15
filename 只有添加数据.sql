INSERT INTO `attractions_province` (name, zh_name) VALUES 
('Anhui', '安徽省'),
('Beijing', '北京市'),
('Chongqing', '重庆市'),
('Fujian', '福建省'),
('Gansu', '甘肃省'),
('Guangdong', '广东省'),
('Guangxi', '广西壮族自治区'),
('Guizhou', '贵州省'),
('Hainan', '海南省'),
('Hebei', '河北省'),
('Heilongjiang', '黑龙江省'),
('Henan', '河南省'),
('Hubei', '湖北省'),
('Hunan', '湖南省'),
('Inner Mongolia', '内蒙古自治区'),
('Jiangsu', '江苏省'),
('Jiangxi', '江西省'),
('Jilin', '吉林省'),
('Liaoning', '辽宁省'),
('Ningxia', '宁夏回族自治区'),
('Qinghai', '青海省'),
('Shaanxi', '陕西省'),
('Shandong', '山东省'),
('Shanghai', '上海市'),
('Shanxi', '山西省'),
('Sichuan', '四川省'),
('Tianjin', '天津市'),
('Tibet', '西藏自治区'),
('Xinjiang', '新疆维吾尔自治区'),
('Yunnan', '云南省'),
('Zhejiang', '浙江省'),
('Hong Kong', '香港特别行政区'),
('Macau', '澳门特别行政区'),
('Taiwan', '台湾省');

INSERT INTO `users_user` (id,password,last_login,is_superuser,username,email,is_staff,is_active,date_joined,gender,phone,role) VALUES (1,'pbkdf2_sha256$150000$LzEedeeU2y4S$PZwFU3qlsMT9hW5PHmPwKXQxaLY5Ot/T4Wc7kKIzZcs=','2024-11-08 14:53:30.773456',1,'fool','123456@qq.com',0,1,'2024-11-08 14:53:28.355002','male','fool','super_admin'),
 (2,'pbkdf2_sha256$150000$pFtuGnTXUFrk$fQRRtjQ/PV4bP/fO/Clha6sxS1TMNGZOJJ4SujpuGRY=','2024-11-11 15:04:24.249249',1,'fool2','123456@qq.com',0,1,'2024-11-08 14:54:11.774271','male','fool','attraction_manager'),
 (3,'pbkdf2_sha256$150000$2XdlDgj7zw1o$jN73gqMmcj6pp8W8TxMZyRf50E2kmCjMwGVhgzuhex0=','2024-11-11 15:04:43.077159',1,'fool3','123456@qq.com',1,1,'2024-11-08 14:54:35.734965','male','fool2','user'),
 (4,'123456','2024-11-11 16:57:28',0,'fool4','28900@qq.com',1,1,'2024-11-11 16:57:18','male','12345345678','user');
 
 
INSERT INTO `attractions_attraction` (id,name,description,location,image,total_price,manager_id,province_name_id) VALUES (1,'天柱山','安徽名山','安徽省安庆市','http://tzs.com.cn/uploads/17/image/public/202009/20200930093350_mqxylbr6tm.png',20,2,'Anhui'),
 (2,'武功山','江西名山','江西省萍乡市','https://img1.baidu.com/it/u=3585732271,2353197828&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=1148',15,2,'Jiangxi'),
 (3,'黄山','中国著名风景名胜区，以奇松、怪石、云海、温泉、冬雪“五绝”著称于世。','安徽省黄山市','https://tse3-mm.cn.bing.net/th/id/OIP-C.xjjIrwAicqmU1Wdv_1Dl1AHaE8?w=298&h=199&c=7&r=0&o=5&dpr=1.5&pid=1.7',80,2,'Anhui'),
 (4,'九寨沟','世界自然遗产，以绝美的湖泊、瀑布群、雪山和原始森林闻名。','四川省阿坝藏族羌族自治州九寨沟县','https://tse1-mm.cn.bing.net/th/id/OIP-C.J_E-jUg7p7RHQrAyqPyVagHaE8?w=272&h=181&c=7&r=0&o=5&dpr=1.5&pid=1.7',120,2,'Sichuan'),
 (5,'张家界国家森林公园','中国第一个国家森林公园，以独特的砂岩峰林地貌著称。','湖南省张家界市','https://tse3-mm.cn.bing.net/th/id/OIP-C.c4-o6Ly385hokpRmGVurIAHaEK?w=324&h=182&c=7&r=0&o=5&dpr=1.5&pid=1.7',100,2,'Hunan'),
 (6,'泰山','中国五岳之首，世界文化与自然双重遗产。','山东省泰安市','https://tse4-mm.cn.bing.net/th/id/OIP-C.qGnBE7grgaIOt2iJ4JVY3AHaE8?w=286&h=191&c=7&r=0&o=5&dpr=1.5&pid=1.7',90,2,'Shandong'),
 (7,'华山','中国五岳之一，以险峻著称。','陕西省渭南市华阴市','https://tse4-mm.cn.bing.net/th/id/OIP-C.zv6tBBEF-mHzGwj_9bw2gAHaE7?w=270&h=180&c=7&r=0&o=5&dpr=1.5&pid=1.7',110,2,'Shaanxi'),
 (8,'西湖','世界文化遗产，中国十大风景名胜之一。','浙江省杭州市','https://tse4-mm.cn.bing.net/th/id/OIP-C.Tp2kbJHgdieQM-VufV0lqAHaEK?w=271&h=180&c=7&r=0&o=5&dpr=1.5&pid=1.7',60,2,'Zhejiang'),
 (9,'丽江古城','世界文化遗产，拥有独特的纳西族文化和美丽的自然风光。','云南省丽江市','https://tse1-mm.cn.bing.net/th/id/OIP-C.7O8wmbDCEI0AnDTwKDejXwHaE8?w=279&h=186&c=7&r=0&o=5&dpr=1.5&pid=1.7',75,2,'Yunnan'),
 (10,'鼓浪屿','中国最美五大城区之首，拥有众多历史建筑和美丽的海景。','福建省厦门市','https://tse2-mm.cn.bing.net/th/id/OIP-C.fu9Y3q4c_Ti749PUrzF9xAHaEZ?w=267&h=180&c=7&r=0&o=5&dpr=1.5&pid=1.7',50,2,'Fujian'),
 (11,'井冈山','井冈山烈士陵园井冈山革命烈士陵园是茨坪中心景区新辟的主要革命人文景观。它位于茨坪北面的北岩峰上。陵园于1987年始建,同年10月建成并开放参观游览。
add-超级美','江西省赣州市','attractions/f11f3a292df5e0febeb5d7e45a6034a85fdf72a1.webp',15,2,'Jiangxi');


INSERT INTO `attractions_reservation` (id, date, time, num_people, total_price, contact_name, contact_phone, note, created_at, attraction_id, user_id, is_paid, payment_date, status) 
VALUES (1, '2024-11-16', '08:32:00', 2, 30, '123345678', '123456788', 'now', '2024-11-10 00:29:56.987991', 2, 3, 1, '2024-11-11 01:09:42.335458+00:00', 'reject'),
    (2, '2024-11-16', '08:32:00', 2, 30, '123345678', '123456788', 'now', '2024-11-10 00:33:24.744228', 2, 3, 1, '2024-11-11 01:09:42.335458+00:00', 'approve'),
    (3, '2024-11-16', '08:32:00', 2, 30, '123345678', '123456788', 'now', '2024-11-10 01:20:25.221898', 2, 3, 0, NULL, Null),
    (4, '2024-11-14', '09:28:00', 1, 90, '1234567', '1234567', 'nio', '2024-11-10 01:25:19.372644', 6, 3, 0, NULL,Null );

INSERT INTO `attractions_reservation` (id,date,time,num_people,total_price,contact_name,contact_phone,note,created_at,is_paid,payment_date,status,attraction_id,user_id) VALUES (1,'2024-11-16','08:32:00',2,30,'123345678','123456788','now','2024-11-10 00:29:56.987991',1,'2024-11-11 01:09:42.335458+00:00','approve',2,3),
 (2,'2024-11-16','08:32:00',2,30,'123345678','123456788','now','2024-11-10 00:33:24.744228',1,'2024-11-11 01:09:42.335458+00:00',NULL,2,3),
 (3,'2024-11-16','08:32:00',2,30,'123345678','123456788','now','2024-11-10 01:20:25.221898',0,NULL,NULL,2,3),
 (4,'2024-11-14','09:28:00',1,90,'1234567','1234567','nio','2024-11-10 01:25:19.372644',0,NULL,NULL,6,3),
 (5,'2024-11-18','16:50:00',5,100,'李华','1234567','我希望有一个愉快的旅行','2024-11-11 16:51:34.173465',1,'2024-11-11 16:51:28','approved',1,1);
 
 
 
 
 