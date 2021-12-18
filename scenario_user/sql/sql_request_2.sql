SELECT id_client, client_name, client_surname, client_patronymic, client_balance FROM course_work.client
WHERE id_client BETWEEN "$param1" AND "$param2"
AND month(client_contract_sign_date) <= "$param3"
AND year(client_contract_sign_date) <= "$param4";