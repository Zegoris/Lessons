from requests import post, get, delete, put


print(delete('http://localhost:8888/api/jobs/999').json())

print(delete('http://localhost:8888/api/jobs/1').json())


print(put('http://localhost:8888/api/jobs/999',
          json={}).json())

print(put('http://localhost:8888/api/jobs/999',
          json={'team_leader': 1,
                'job': 'admin',
                'work_size': 15,
                'collaborators': '2, 3',
                'hazard': 1,
                'is_finished': False}).json())

print(put('http://localhost:8888/api/jobs/1',
          json={'team_leader': 'q',
                'job': 'admin',
                'work_size': 15,
                'collaborators': '2, 3',
                'hazard': 1,
                'is_finished': False}).json())


print(put('http://localhost:8888/api/jobs/1',
          json={'team_leader': 1,
                'job': 'admin',
                'work_size': 15,
                'collaborators': '2, 3',
                'hazard': 1,
                'is_finished': False}).json())


print(get('http://localhost:8888/api/jobs').json())

