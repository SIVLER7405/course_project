SELECT * FROM client
WHERE client_contract_sign_date = (
SELECT max(client_contract_sign_date)
FROM client
WHERE client_contract_sign_date BETWEEN "$param1" AND "$param2"
);