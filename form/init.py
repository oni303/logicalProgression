from jinja2 import Template
import yaml
import subprocess

with open('/docker-compose.yml') as dockerConfigFile:
    dockerConfig = yaml.load(dockerConfigFile)
    rootPW = dockerConfig['services']['logicalDB']['environment']['MYSQL_ROOT_PASSWORD']
    print(rootPW)
    with open('/config/config.yaml') as configFile:
        config = yaml.load(configFile)
        with open('logicalProgression.mysql_schema.sql.template') as sqlSchemaFile:
            template = Template(sqlSchemaFile.read())
            t = template.render(dbName = config['dbName'])
            schema = open('/tmp/schema.sql', 'w+')
            schema.write(t)
            schema.close()
            subprocess.Popen('mysql -h '+config['dbServer']+' -P 3306 --password='+rootPW+' '+ config['dbName'] +' < /tmp/schema.sql ', shell=True)

        with open('addUser.mysql_schema.sql.template') as sqlSchemaFile:
            template = Template(sqlSchemaFile.read())
            t = template.render(dbName = config['dbName'],user = config['dbUser'],password = config['dbPw'])
            schema = open('/tmp/useradd.sql', 'w+')
            schema.write(t)
            schema.close()
            subprocess.Popen('mysql -h '+config['dbServer']+' -P 3306 --password='+rootPW+' '+ config['dbName'] +' < /tmp/useradd.sql ', shell=True)

        
    
