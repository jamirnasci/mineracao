import requests

res = requests.post('http://localhost:5000/', json={
    "balance": 80000,
    "estimated_salary": 30000
})

print(res.json())