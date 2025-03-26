-- 1. Top 10 operadoras com maiores despesas no último trimestre
SELECT 
    o.razao_social,
    SUM(d.valor) AS total_despesas
FROM 
    demonstracoes d
JOIN 
    operadoras o ON d.registro_ans = o.registro_ans
WHERE 
    d.descricao LIKE '%EVENTOS/%SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
    AND d.data >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH)
GROUP BY 
    o.razao_social
ORDER BY 
    total_despesas DESC
LIMIT 10;

-- 2. Top 10 operadoras com maiores despesas no último ano
SELECT 
    o.razao_social,
    SUM(d.valor) AS total_despesas
FROM 
    demonstracoes d
JOIN 
    operadoras o ON d.registro_ans = o.registro_ans
WHERE 
    d.descricao LIKE '%EVENTOS/%SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
    AND d.data >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR)
GROUP BY 
    o.razao_social
ORDER BY 
    total_despesas DESC
LIMIT 10;