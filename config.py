from sshtunnel import SSHTunnelForwarder
import pymysql


# SSH
server = SSHTunnelForwarder(
    ssh_address_or_host=('linux.cs.ncl.ac.uk', 22),
    ssh_username="C0038359",
    ssh_password="AboutNameSum19082002",
    remote_bind_address=('cs-db.ncl.ac.uk', 3306)
)
server.start()

# Database connection config
connection = pymysql.connect(
    host='127.0.0.1',
    port=server.local_bind_port,
    user='csc2033_team51',
    passwd='BarnBedsSitu',
    db='csc2033_team51'
)

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://csc2033_team51:BarnBedsSitu@localhost:{server.local_bind_port}/csc2033_team51'


def shutdown():
    connection.close()
    server.close()