ALTER TABLE `ENDURO_XTRAINER_300_2T_MY22` DROP `Unnamed: 0`,  DROP `Unnamed: 5`;
ALTER TABLE `ENDURO_XTRAINER_300_2T_MY22` ADD `pvp_sin_iva` DOUBLE NOT NULL AFTER `componente`;
ALTER TABLE `ENDURO_XTRAINER_300_2T_MY22`  ADD `enlace` VARCHAR(25) NOT NULL  AFTER `pvp_sin_iva`;
ALTER TABLE `ENDURO_XTRAINER_300_2T_MY22`  ADD `ref_sust` VARCHAR(50) NOT NULL  AFTER `enlace`,  ADD `existe` BOOLEAN NOT NULL DEFAULT FALSE  AFTER `ref_sust`;
UPDATE `ENDURO_XTRAINER_300_2T_MY22` SET `enlace`= replace(`Part Number`,'.','');
UPDATE `ENDURO_XTRAINER_300_2T_MY22` A SET `pvp_sin_iva` = (SELECT Preu FROM tarifa_beta B WHERE B.Article = A.`Part Number`);
UPDATE `ENDURO_XTRAINER_300_2T_MY22` A SET `Description` = (SELECT Descripcion FROM tarifa_beta B WHERE B.Article = A.`Part Number`);
UPDATE `ENDURO_XTRAINER_300_2T_MY22` A SET `pvp_sin_iva` = (SELECT Preu FROM tarifa_beta B WHERE B.cod = A.enlace) WHERE `Description` is NULL;
UPDATE `ENDURO_XTRAINER_300_2T_MY22` A SET `Description` = (SELECT Descripcion FROM tarifa_beta B WHERE B.cod = A.`enlace`) WHERE `Description` is NULL;
update `ENDURO_XTRAINER_300_2T_MY22` set `enlace` = replace(replace (`Description`,'#',''),'.','')  WHERE `Description` like '%#%';
update `ENDURO_XTRAINER_300_2T_MY22` SEt  ref_sust = replace (`Description`,'#','')  WHERE `Description` like '%#%';
UPDATE `ENDURO_XTRAINER_300_2T_MY22` A SET `pvp_sin_iva` = (SELECT Preu FROM tarifa_beta B WHERE B.Article = A.ref_sust) WHERE `Description` like '%#%';
UPDATE `ENDURO_XTRAINER_300_2T_MY22` A SET `Description` = (SELECT Descripcion FROM tarifa_beta B WHERE B.Article = A.ref_sust) WHERE `Description` like '%#%';

insert into BETA_2022 SELECT * FROM `ENDURO_RR_125_2T_MY22`;
insert into BETA_2022 SELECT * FROM `ENDURO_RR_200_2T_MY22`;
insert into BETA_2022 SELECT * FROM `ENDURO_RR_250_2T_MY22`;
insert into BETA_2022 SELECT * FROM `ENDURO_RR_300_2T_MY22`;
insert into BETA_2022 SELECT * FROM `ENDURO_RR_350_4T_MY22`;
insert into BETA_2022 SELECT * FROM `ENDURO_RR_390_4T_MY22`;
insert into BETA_2022 SELECT * FROM `ENDURO_RR_430_4T_MY22`;
insert into BETA_2022 SELECT * FROM `ENDURO_RR_480_4T_MY22`;
insert into BETA_2022 SELECT * FROM `ENDURO_XTRAINER_250_2T_MY22O`;
insert into BETA_2022 SELECT * FROM `ENDURO_XTRAINER_300_2T_MY22O`;


insert into BETA_2022 (`Ref.`,`Part Number`,`Description`,`Parts`,`componente`,`pvp_sin_iva`,`enlace`,`ref_sust`,`existe`) SELECT `Ref.`,`Part Number`,`Description`,`Parts`,`componente`,`pvp_sin_iva`,`enlace`,`ref_sust`,`existe` FROM `ENDURO_RR_125_2T_MY22`;
insert into BETA_2022 (`Ref.`,`Part Number`,`Description`,`Parts`,`componente`,`pvp_sin_iva`,`enlace`,`ref_sust`,`existe`) SELECT `Ref.`,`Part Number`,`Description`,`Parts`,`componente`,`pvp_sin_iva`,`enlace`,`ref_sust`,`existe` FROM `ENDURO_RR_200_2T_MY22`;
insert into BETA_2022 (`Ref.`,`Part Number`,`Description`,`Parts`,`componente`,`pvp_sin_iva`,`enlace`,`ref_sust`,`existe`) SELECT `Ref.`,`Part Number`,`Description`,`Parts`,`componente`,`pvp_sin_iva`,`enlace`,`ref_sust`,`existe` FROM `ENDURO_RR_250_2T_MY22`;
insert into BETA_2022 (`Ref.`,`Part Number`,`Description`,`Parts`,`componente`,`pvp_sin_iva`,`enlace`,`ref_sust`,`existe`) SELECT `Ref.`,`Part Number`,`Description`,`Parts`,`componente`,`pvp_sin_iva`,`enlace`,`ref_sust`,`existe` FROM `ENDURO_RR_300_2T_MY22`;
insert into BETA_2022 (`Ref.`,`Part Number`,`Description`,`Parts`,`componente`,`pvp_sin_iva`,`enlace`,`ref_sust`,`existe`) SELECT `Ref.`,`Part Number`,`Description`,`Parts`,`componente`,`pvp_sin_iva`,`enlace`,`ref_sust`,`existe` FROM `ENDURO_RR_350_4T_MY22`;
insert into BETA_2022 (`Ref.`,`Part Number`,`Description`,`Parts`,`componente`,`pvp_sin_iva`,`enlace`,`ref_sust`,`existe`) SELECT `Ref.`,`Part Number`,`Description`,`Parts`,`componente`,`pvp_sin_iva`,`enlace`,`ref_sust`,`existe` FROM `ENDURO_RR_390_4T_MY22`;
insert into BETA_2022 (`Ref.`,`Part Number`,`Description`,`Parts`,`componente`,`pvp_sin_iva`,`enlace`,`ref_sust`,`existe`) SELECT `Ref.`,`Part Number`,`Description`,`Parts`,`componente`,`pvp_sin_iva`,`enlace`,`ref_sust`,`existe` FROM `ENDURO_RR_430_4T_MY22`;
insert into BETA_2022 (`Ref.`,`Part Number`,`Description`,`Parts`,`componente`,`pvp_sin_iva`,`enlace`,`ref_sust`,`existe`) SELECT `Ref.`,`Part Number`,`Description`,`Parts`,`componente`,`pvp_sin_iva`,`enlace`,`ref_sust`,`existe` FROM `ENDURO_RR_480_4T_MY22`;
insert into BETA_2022 (`Ref.`,`Part Number`,`Description`,`Parts`,`componente`,`pvp_sin_iva`,`enlace`,`ref_sust`,`existe`) SELECT `Ref.`,`Part Number`,`Description`,`Parts`,`componente`,`pvp_sin_iva`,`enlace`,`ref_sust`,`existe` FROM `ENDURO_XTRAINER_250_2T_MY22O`;
insert into BETA_2022 (`Ref.`,`Part Number`,`Description`,`Parts`,`componente`,`pvp_sin_iva`,`enlace`,`ref_sust`,`existe`) SELECT `Ref.`,`Part Number`,`Description`,`Parts`,`componente`,`pvp_sin_iva`,`enlace`,`ref_sust`,`existe` FROM `ENDURO_XTRAINER_300_2T_MY22O`;


SELECT
    `price`,
    pvp_sin_iva,
    `reference`,
    enlace,
    id_category_default,
    categoria_eqv,
    componente,
	c.id_product,
	b.`Ref.`,
    substr(c.description,4,2),
    b.Description,
    c.description,
    c.name
FROM
   `web_product` AS a,
    BETA_2022 AS b,
    nuevaendurorecambios.ps_product_lang as c
WHERE
    a.reference = b.enlace AND `id_category_default` IN(
        '149253',
        '149254',
        '149255',
        '149256',
        '149257',
        '149258',
        '149259',
        '149260',
        '149261',
        '149262',
        '149263',
        '149264',
        '149265',
        '149266',
        '149267',
        '149268',
        '149269',
        '149270',
        '149271',
        '149272',
        '149273',
        '149274',
        '149275',
        '149276',
        '149277',
        '149278',
        '149279',
        '149280',
        '149281',
        '149282',
        '149283',
        '149377'
    )
    and b.componente like 'ENDURO_RR_125_2T_MY22%'
    and existe = 1
    and id_shop_default = 1
    and id_manufacturer = 13
    and a.id_product = c.id_product
    and id_category_default = `categoria_eqv`
    and id_lang = 1
    and b.`Ref.`= substr(c.description,4,2)


    UPDATE`BETA_2022` SET categoria_eqv = 149253 WHERE `componente` = 'ENDURO_RR_125_2T_MY22_1';
    UPDATE`BETA_2022` SET categoria_eqv = 149254 WHERE `componente` = 'ENDURO_RR_125_2T_MY22_2';
    UPDATE`BETA_2022` SET categoria_eqv = 149255 WHERE `componente` = 'ENDURO_RR_125_2T_MY22_3';
    UPDATE`BETA_2022` SET categoria_eqv = 149256 WHERE `componente` = 'ENDURO_RR_125_2T_MY22_4';
    UPDATE`BETA_2022` SET categoria_eqv = 149257 WHERE `componente` = 'ENDURO_RR_125_2T_MY22_5';
    UPDATE`BETA_2022` SET categoria_eqv = 149258 WHERE `componente` = 'ENDURO_RR_125_2T_MY22_6';
    UPDATE`BETA_2022` SET categoria_eqv = 149277 WHERE `componente` = 'ENDURO_RR_125_2T_MY22_7';
    UPDATE`BETA_2022` SET categoria_eqv = 149278 WHERE `componente` = 'ENDURO_RR_125_2T_MY22_8';
    UPDATE`BETA_2022` SET categoria_eqv = 149279 WHERE `componente` = 'ENDURO_RR_125_2T_MY22_9';
    UPDATE`BETA_2022` SET categoria_eqv = 149280 WHERE `componente` = 'ENDURO_RR_125_2T_MY22_10';
    UPDATE`BETA_2022` SET categoria_eqv = 149281 WHERE `componente` = 'ENDURO_RR_125_2T_MY22_11';
    UPDATE`BETA_2022` SET categoria_eqv = 149269 WHERE `componente` = 'ENDURO_RR_125_2T_MY22_12';
    UPDATE`BETA_2022` SET categoria_eqv = 149377 WHERE `componente` = 'ENDURO_RR_125_2T_MY22_13';
    UPDATE`BETA_2022` SET categoria_eqv = 149271 WHERE `componente` = 'ENDURO_RR_125_2T_MY22_14';
    UPDATE`BETA_2022` SET categoria_eqv = 149282 WHERE `componente` = 'ENDURO_RR_125_2T_MY22_15';

    SELECT b.id_product,b.reference,replace(replace(a.Descripcion,'.','') ,'#','') FROM Alim.`tarifa_beta` a, nuevaendurorecambios.ps_product b where Preu = 0 and Descripcion like '#%' and reference = cod and b.id_manufacturer = 13

    DROP TABLE `t_brp_product`, `t_change_price`, `t_match_brp_web`, `t_new_reference_subs`, `t_no_match_tarifa`, `t_no_match_web`, `t_referen_subs`;
