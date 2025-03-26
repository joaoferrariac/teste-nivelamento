-- Importar operadoras (MySQL)
LOAD DATA INFILE 'data/operadoras_ativas.csv'
INTO TABLE operadoras
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'data/demonstracoes_contabeis.csv'
INTO TABLE demonstracoes
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(registro_ans, data, conta, descricao, valor);
