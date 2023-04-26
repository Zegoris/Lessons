from requests import post, get, delete

print(get('http://localhost:8888/api/v2/jobs').json())

print(get('http://localhost:8888/api/v2/jobs/1').json())

print(get('http://localhost:8888/api/v2/jobs/999').json())

print(get('http://localhost:8888/api/v2/jobs/q').json())

print(delete('http://localhost:8888/api/v2/jobs/999').json())

print(delete('http://localhost:8888/api/v2/jobs/1').json())


print(post('http://localhost:8888/api/v2/jobs',
           json={}).json())

print(post('http://localhost:8888/api/v2/jobs',
           json={'team_leader': 1,
                 'job': 'admin',
                 'work_size': 15,
                 'collaborators': '2, 3',
                 'hazard': 1,
                 'is_finished': False}).json())

print(post('http://localhost:8888/api/v2/jobs',
           json={'team_leader': 'q',
                 'job': 'admin',
                 'work_size': 15,
                 'collaborators': '2, 3',
                 'hazard': 1,
                 'is_finished': False}).json())


print(post('http://localhost:8888/api/v2/jobs',
           json={'team_leader': 1,
                 'job': 'admin',
                 'work_size': 15,
                 'collaborators': '2, 3',
                 'hazard': 1,
                 'is_finished': False}).json())

print(get('http://localhost:8888/api/v2/jobs').json())


print(get('http://localhost:8888/api/v2/users').json())

print(get('http://localhost:8888/api/v2/users/1').json())

print(get('http://localhost:8888/api/v2/users/999').json())

print(get('http://localhost:8888/api/v2/users/q').json())

print(delete('http://localhost:8888/api/v2/users/999').json())

print(delete('http://localhost:8888/api/v2/users/1').json())


print(post('http://localhost:8888/api/v2/users',
           json={}).json())

print(post('http://localhost:8888/api/v2/users',
           json={'surname': 'admin',
                 'name': 'admin',
                 'age': '15',
                 'position': 'admin',
                 'speciality': 'admin',
                 'address': 'module_admin',
                 'city_from': 'минеральные воды',
                 'email': 'admin@gmail.com',
                 'password': 'QAZwsx1234'}).json())

print(post('http://localhost:8888/api/v2/users',
           json={'surname': 'admin',
                 'name': 'admin',
                 'age': 15,
                 'position': 'admin',
                 'speciality': 'admin',
                 'address': 'module_admin',
                 'city_from': 'минеральные воды',
                 'email': 'admin@gmail.com',
                 'password': 'QAZwsx1234'}).json())

print(get('http://localhost:8888/api/v2/users').json())