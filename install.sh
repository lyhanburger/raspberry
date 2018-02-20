DevInstall(){
	echo "DevInstall..."
	sudo apt-get update
	sudo apt-get purge -y postgres*
	sudo apt-get install -y python3-pyqt5* libperl-dev python3-dev
	sudo apt-get install python3-psycopg2
	sudo pip3 install numpy
}
PgsqlDownload(){
	echo "PgsqlDownload..."
	if [ ! -f "/home/pi/postgresql-9.6.2.tar.bz2" ]; then
		wget ftp://lihao2333.com/postgresql-9.6.2.tar.bz2
	else
		echo "there has been a file named postgresql9.6.2.tar.bz2, it won't be download again"
	fi
}
PgsqlInstall(){
	echo "PgsqlInstall..."
	if [ -d  "/usr/local/pgsql" ]; then
		echo "you have installed the pgsql"
		return
	fi
	rm -rf postgresql-9.6.2
	tar xf postgresql-9.6.2.tar.bz2
	cd postgresql-9.6.2
	./configure --prefix=/usr/local/pgsql9.6.2 --with-python --with-perl --without-readline
	make
	sudo make install
	sudo ln -sf /usr/local/pgsql9.6.2 /usr/local/pgsql
}
PgsqlSetup(){
	echo "PgsqlSetup..."
	echo $LD_LIBRARY_PATH
	if [ -d "/home/pi/pgdata" ]; then
		echo "you have already inited the db"
		return
	fi
	rm -rf /home/pi/pgdata
	initdb -D /home/pi/pgdata
}
PgsqlStart(){
	pg_ctl -D /home/pi/pgdata -l /home/pi/pgdata/logfile restart
	sleep 2s
}
PgsqlInit(){
	echo "PgsqlInit..."
	echo $PATH
	psql -U pi -d postgres -c "alter user pi with password 'raspberry'"
	psql -U pi -d postgres -c "drop database if exists raspberry "
	psql -U pi -d postgres -c "create database  raspberry owner pi"
}
RaspberryDownload(){
	if [ -f "raspberry.tar" ]; then
		echo "there has been a file named raspberry.tar, it wouldn't be download again"
	else 
		wget ftp://lihao2333.com/raspberry.tar
	fi
}
RaspberryInstall(){
	echo "RaspberryInstall..."
	if [ -d "/home/pi/raspberry" ]; then
		echo "there has already a dir /home/pi/raspberry ,skip"
		return
	fi
	tar xf raspberry.tar
	sudo chown -R pi raspberry
	sudo chmod -R 775 raspberry
}
RaspberryInit(){
	python3 raspberry/communication/configDB.py
	python3 raspberry/communication/login.py
	python3 raspberry/communication/register.py
	python3 raspberry/communication/exam.py
	python3 raspberry/communication/speech.py
	python3 raspberry/communication/configFTP.py
}
#Notation:将该文件放在/home/pi中,赋予可执行权限,然后以用户pi的身份运行即可.
####set enverment
export PATH=/usr/local/pgsql/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/pgsql/lib:$LD_LIBRARY_PATH
DevInstall
PgsqlDownload #if already downloaded, then skip
PgsqlInstall #if exists /usr/local/pgsql then skip 
PgsqlSetup	#create database cluster anyway
PgsqlStart
PgsqlInit	#alter user pi and create database raspberry
RaspberryDownload	#if exists /home/pi/raspberry.tar then skip
RaspberryInstall	#if exists /home/pi/raspberry then skip
RaspberryInit 	#create table and preload data
