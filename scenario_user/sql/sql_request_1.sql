SELECT month(call_sign_date), id_call, service_name, count(call_sign_date), count(call_unsign_date)
FROM course_work.call
LEFT JOIN service
ON course_work.call.id_call = service.id_service
WHERE year(call_sign_date) = "$param"
GROUP BY id_call;