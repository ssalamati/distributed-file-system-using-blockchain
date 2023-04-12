from console_application import ConsoleApp
from db_manager import DBManager
from sdfs import SDFS

if __name__ == '__main__':
    db = DBManager.setup('SDFS')
    sdfs = SDFS(db)
    sdfs.run_server()
    console = ConsoleApp(sdfs, db)
    console.run()


