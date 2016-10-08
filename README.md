#### DEV:
1. Install vagrant: 
  `sudo apt-get install virtualbox`
  `sudo apt-get install vagrant`
2. Сlone project from git: `git@github.com:knowledge-point/scheduling_1_8.git`
3. In DIR: scheduling/ run: `vagrant up`
4. Enter in box: `vagrant ssh`
5. Set All **env** variables : { 
                                    RUN_ENV=DEV, 
                                    RABBITMQ_DEFAULT_USER=...,
                                    RABBITMQ_DEFAULT_PASS=...,
                                }

6. In vagrant box run: 
 - `cd /vagrant`
 - `sh redeploy.sh`
7. Create volume for DB:
 - `docker exec -it scheduling_postgres_dev_1 /bin/bash`
 - `su postgres`
 - `psql`
 - `CREATE DATABASE scheduling_dev;`
 - `CREATE USER scheduling_dev PASSWORD 'scheduling_dev';`
 - `GRANT ALL PRIVILEGES ON DATABASE scheduling_dev TO scheduling_dev;`
 - `\q`
 - `exit`
 - `exit`
 - `sh redeploy.sh`
8. In browser open http://127.0.0.1/

#### PROD:
1. Install docker & docker-compose: 
 - `sudo -i`
 - `echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections`
 - `curl -sSL https://get.docker.com/ | sh`
 - `usermod -aG docker ubuntu`
 - ``curl -L https://github.com/docker/compose/releases/download/1.5.1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose``
 - `chmod +x /usr/local/bin/docker-compose`

2. Сlone project from git: `git clone https://github.com/knowledge-point/scheduling_1_8.git`
3. Set All **env** variables on server: { 
                                            RUN_ENV=PROD, 
                                            DB_HOST=..., 
                                            SCHEDUL_DB_PASS=..., 
                                            SCHEDUL_DB_HOST=..., 
                                            SCHEDUL_SENTRY_URL=...,
                                            RABBITMQ_DEFAULT_USER=...,
                                            RABBITMQ_DEFAULT_PASS=...,
                                            RABBITMQ_HOST=...,
                                        }
4. In DIR: /project run: `sh redeploy.sh`

#### STAGE | TEST:
1. Install docker & docker-compose: 
 - `sudo -i`
 - `echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections`
 - `curl -sSL https://get.docker.com/ | sh`
 - `usermod -aG docker ubuntu`
 - ``curl -L https://github.com/docker/compose/releases/download/1.5.1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose``
 - `chmod +x /usr/local/bin/docker-compose`

2. Сlone project from git: `git clone https://github.com/knowledge-point/scheduling_1_8.git`
3. Set All **env** variables on server: { 
                                            RUN_ENV=STAGE | TEST(choose one), 
                                            SCHEDUL_SENTRY_URL=...,
                                            RABBITMQ_DEFAULT_USER=...,
                                            RABBITMQ_DEFAULT_PASS=...,
                                        }
4. In DIR: /project run: 
 - `sh redeploy.sh [stage|test]` (choose one)
5. Create volume for DB:
 - `docker exec -it scheduling_postgres_[stage|test]_1 /bin/bash` (choose one)
 - `su postgres`
 - `psql`
 - `CREATE DATABASE scheduling_[stage|test];` (choose one)
 - `CREATE USER scheduling_[stage|test] PASSWORD 'scheduling_[stage|test]';` (choose one)
 - `GRANT ALL PRIVILEGES ON DATABASE scheduling_[stage|test] TO scheduling_[stage|test];` (choose one)
 - `\q`
 - `exit`
 - `exit`
 - `sh redeploy.sh`
 - `sh redeploy.sh [stage|test]` (choose one)


#### API REST (need import to Postman):
 - [DEV](https://github.com/knowledge-point/scheduling_1_8/blob/master/postman_dev.json "DEV API for Postman")
 - [PROD](https://github.com/knowledge-point/scheduling_1_8/blob/master/postman_prod.json "PROD API for Postman")
 - [TEST](https://github.com/knowledge-point/scheduling_1_8/blob/master/postman_test.json "TEST API for Postman")
 - [STAGE](https://github.com/knowledge-point/scheduling_1_8/blob/master/postman_stage.json "STAGE API for Postman")