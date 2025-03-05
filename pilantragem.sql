/*
UPDATE customers_training SET CreditScore = FLOOR((RAND() * 500)) WHERE CreditScore >= 700 AND Class = 'low';
UPDATE customers_training SET CreditScore = FLOOR((RAND() * 500)) WHERE CreditScore >= 760 AND Class = 'medium';
UPDATE customers_training SET CreditScore = FLOOR((RAND() * 500)) WHERE CreditScore <= 300 AND Class = 'medium';
UPDATE customers_training SET Age = FLOOR(RAND() * (45 - 30 + 1)) + 30 WHERE Age >= 72;
UPDATE customers_training SET Age = FLOOR(RAND() * (55 - 30 + 1)) + 45 WHERE Age BETWEEN 30 AND 40 AND Class = 'high';
*/

-- UPDATE customers_training SET Balance = FLOOR(RAND() * (150000 - 1 + 1)) + 150000 WHERE Balance <= 0
-- UPDATE customers_training SET Balance = FLOOR(POWER(RAND(), 2) * 50000) + 1 WHERE Class = 'low';
