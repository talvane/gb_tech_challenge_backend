# Executando a Solução:
- git clone
- --> Crie o arquivo .env com base no .env_example <--
- Preencher com os valores:
```
SECRET_KEY='django-insecure-c&dan$80wrkybh57gl)(ghai)l%zyif4*e1g8r0e*bo6pkzo!*'
DEBUG=True
ALLOWED_HOSTS=127.0.0.1, .localhost
API_TOT_CASHBACK=https://mdaqk8ek5j.execute-api.us-east-1.amazonaws.com
API_TOKEN=ZXPURQOARHiMc6Y0flhRC1LVlZQVFRnm
DATABASE_URL=postgres://postgres:123456@api-db:5432/gb_tech
```
- docker-compose up --build
- http://127.0.0.1:8000/api/swagger/ -> Documentação e Testes da API
- Login: admin@test.com
- Senha: gy49y6.

#
- A solução também encontra-se hospeda em: ``` https://challenge-gb-tech.herokuapp.com/api/swagger/ ```
- Login: admin@test.com
- Senha: 123456