COPY pub4me_pub
TO 'E:/data_out.csv'
WITH
	DELIMITER ';'	
	CSV QUOTE '"'; 
	
/* plik wejściowy musi być w kodowaniu UTF8 (po wyjściu z pająka jest zakodowany w cp1250) */
COPY pub4me_pub
FROM 'E:/python/dmoz_tutorial/knajpy.krakow_do_importu.csv'
WITH
	DELIMITER ';';


delete from pub4me_pub;


select * from pub4me_pub;